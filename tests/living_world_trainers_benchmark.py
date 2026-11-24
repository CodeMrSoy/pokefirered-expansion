"""Deterministic trainer scaling with optional native world and offline model trials."""
import argparse
from contextlib import closing
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3
from statistics import median
from tempfile import TemporaryDirectory
from time import perf_counter, process_time

from living_world_trainers import scenario, assert_accounting

import ecology
from inference import LocalModel
import trainers

HORIZONS = (30, 90, 365)


def rss():
    path = Path("/proc/self/statm")
    if path.exists():
        return int(path.read_text().split()[1]) * os.sysconf("SC_PAGE_SIZE")
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes

        class Counters(ctypes.Structure):
            _fields_ = [("size", wintypes.DWORD), ("faults", wintypes.DWORD),
                        ("peak", ctypes.c_size_t), ("working", ctypes.c_size_t)] + [
                            (f"extra{i}", ctypes.c_size_t) for i in range(6)]

        counters = Counters()
        counters.size = ctypes.sizeof(counters)
        handle = ctypes.windll.kernel32
        handle.GetCurrentProcess.restype = wintypes.HANDLE
        memory_info = ctypes.windll.psapi.GetProcessMemoryInfo
        memory_info.argtypes = (wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD)
        memory_info.restype = wintypes.BOOL
        if memory_info(handle.GetCurrentProcess(), ctypes.byref(counters), counters.size):
            return counters.working
    return None


def run(manifest, size, db, model=None):
    index = trainers.build_index(manifest, manifest.get("ecology_protected"))
    if not index["actors"]:
        raise ValueError("No eligible compiled trainer bindings")
    profiles = dict(index["actors"])
    if size:
        source = tuple(profiles.values())
        for i in range(size - len(profiles)):
            # Bench-only identities, deliberately competing for the same habitat resources.
            profiles[f"benchmark:{i:03}"] = dict(source[i % len(source)], native_roster=None)
    eco = ecology.initial_state(manifest, manifest.get("ecology_protected"), 0)
    state = trainers.start(index, eco, 0, profiles)
    metrics, snapshots, proposal, model_times = [], [], None, []
    model_failures = 0
    start, cpu = perf_counter(), process_time()
    memory = rss()
    max_rss = memory
    journal = sha256()
    replay_inputs = {}
    for day in range(1, HORIZONS[-1] + 1):
        tick = perf_counter()
        ecology.evolve_day(eco, day)
        before = sum(ecology.totals(eco).values())
        if proposal:
            replay_inputs[day] = proposal
        events = trainers.advance(state, eco, index, proposal)
        proposal = None
        assert before - sum(event["kind"] == "capture" for event in events) == sum(ecology.totals(eco).values())
        assert_accounting(state, eco)
        with db:
            trainers.write(db, state, events)
        metrics.append((perf_counter() - tick) * 1000)
        journal.update(ecology.encoded(events).encode("ascii"))
        if model and state["request"] and day < 90 and len(model_times) < 4:
            started = perf_counter()
            try:
                proposal = trainers.request_plan(model, state["request"])
            except (OSError, ValueError, RuntimeError):
                model_failures += 1
            model_times.append((perf_counter() - started) * 1000)
        if day % 30 == 0 or day in HORIZONS:
            current = rss()
            if current is not None:
                max_rss = max(max_rss or 0, current)
        if day in HORIZONS:
            levels = [mon["level"] for mon in state["mons"].values()]
            snapshots.append(dict(days=day, cpu_seconds=process_time()-cpu, wall_seconds=perf_counter()-start,
                                  median_update_ms=median(metrics), p99_update_ms=sorted(metrics)[int(.99*len(metrics))],
                                  rss_start=memory, rss_sample_peak=max_rss,
                                  database_bytes=db.execute("PRAGMA page_size").fetchone()[0] *
                                                 db.execute("PRAGMA page_count").fetchone()[0],
                                  counters=dict(state["counters"]), owned=len(levels), highest_level=max(levels, default=0),
                                  median_level=median(levels) if levels else None, conservation_checked=True,
                                  completed_model_calls=len(model_times), model_failures=model_failures,
                                  model_latency_ms=list(model_times), max_inflight_model_calls=1 if model_times else 0))
    final = ecology.encoded(state)
    assert trainers.load(db) == state
    replay = ecology.initial_state(manifest, manifest.get("ecology_protected"), 0)
    repeated = trainers.start(index, replay, 0, profiles)
    repeated_journal = sha256()
    for day in range(1, HORIZONS[-1] + 1):
        ecology.evolve_day(replay, day)
        events = trainers.advance(repeated, replay, index, replay_inputs.get(day))
        repeated_journal.update(ecology.encoded(events).encode("ascii"))
    assert journal.digest() == repeated_journal.digest()
    assert repeated == state and replay == eco
    return dict(profiles=len(profiles), production_profiles=sorted(index["actors"]), scenarios=snapshots,
                projection_sha256=sha256(final.encode("ascii") + journal.digest()).hexdigest(),
                journeys={key: dict(goal=row["goal"], journeys=row["journeys"], decisions=row["decisions"],
                                    party=len(row["party"]), storage=len(row["storage"]))
                          for key, row in state["actors"].items() if key in index["actors"]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--profiles", nargs="+", type=int, default=[10, 25, 50, 100, 250])
    parser.add_argument("--model-runtime", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_bytes()) if args.manifest else scenario()
    results = []
    with TemporaryDirectory() as tmp:
        path = Path(tmp)
        for size in args.profiles:
            with closing(sqlite3.connect(path / f"{size}.sqlite")) as db:
                if args.model_runtime:
                    with closing(LocalModel(args.model_runtime, {}, style="qwen3")) as model:
                        result = run(manifest, size, db, model)
                    assert result["scenarios"][-1]["counters"].get("model_plan_admitted", 0), result
                else:
                    result = run(manifest, size, db)
                results.append(result)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
