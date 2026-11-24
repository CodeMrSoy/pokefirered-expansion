"""Measure and replay annual ecology projections for increasing world sizes."""
import argparse
from contextlib import closing
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
import platform
from statistics import median
import sys
from tempfile import TemporaryDirectory
from time import perf_counter, process_time

from living_world_ecology import scenario
from living_world_manifest import reseal
import ecology
from world_manifest import import_world


def scaled(manifest, copies):
    result = deepcopy(manifest)
    for copy in range(1, copies):
        def remap(key):
            return [key[0] + 256 * copy, key[1]]

        for row in manifest["maps"]:
            extra = deepcopy(row)
            extra["id"] = remap(row["id"])
            for link in extra["connections"]:
                link["target"] = remap(link["target"])
            result["maps"].append(extra)
        for row in manifest["encounters"]:
            extra = deepcopy(row)
            extra["table"]["map"] = remap(extra["table"]["map"])
            extra["table"]["header"] += 65536 * copy
            result["encounters"].append(extra)
        for row in manifest["static_encounters"]:
            result["static_encounters"].append({**row, "map": remap(row["map"])})
    return reseal(result)


def memory_reader():
    linux = Path("/proc/self/statm")
    if linux.exists():
        from os import sysconf
        page_size = sysconf("SC_PAGE_SIZE")
        return lambda: int(linux.read_text().split()[1]) * page_size
    if sys.platform == "win32":
        import ctypes as c
        from ctypes import wintypes as w

        class Counters(c.Structure):
            _fields_ = [("size", w.DWORD), ("faults", w.DWORD)] + [
                (field, c.c_size_t) for field in ("peak", "working", "peak_paged", "paged",
                                                 "peak_nonpaged", "nonpaged", "page", "peak_page")]

        get_process = c.windll.kernel32.GetCurrentProcess
        get_process.restype = w.HANDLE
        get_memory = c.windll.psapi.GetProcessMemoryInfo
        get_memory.argtypes = (w.HANDLE, c.POINTER(Counters), w.DWORD)

        def rss():
            values = Counters()
            values.size = c.sizeof(values)
            return values.working if get_memory(get_process(), c.byref(values), values.size) else None

        return rss
    return lambda: None


def run(manifest, copies, rss):
    manifest = scaled(manifest, copies)
    limits = ecology.Limits(notable_limit=64 * copies, transit_limit=128 * copies)
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "world.db"
        with closing(import_world(path, manifest)) as sim:
            with sim._write():
                ecology.initialize(sim.db, None, limits)
            start_size = path.stat().st_size
            baseline_memory = rss()
            peak = baseline_memory or 0
            durations = []
            stages = {}
            start, cpu = perf_counter(), process_time()
            for day in range(1, 366):
                now = perf_counter()
                with sim._write():
                    ecology.apply(sim.db, [(f"day:{day}", {"day": day})])
                durations.append((perf_counter() - now) * 1000)
                if day % 10 == 0 or day == 365:
                    peak = max(peak, rss() or 0)
                if day in (30, 90, 365):
                    wall = perf_counter() - start
                    used = process_time() - cpu
                    state = ecology.read_state(sim.db)
                    stages[day] = dict(wall_seconds=round(wall, 3), cpu_seconds=round(used, 3),
                        cpu_percent_of_one_core=round(100 * used / wall, 1),
                        median_update_ms=round(median(durations), 3), worst_update_ms=round(max(durations), 3),
                        db_bytes=path.stat().st_size, db_growth_bytes=path.stat().st_size-start_size,
                        rss_bytes=rss(), sampled_peak_rss_bytes=peak or None,
                        notable=len(state["individuals"]), in_transit=len(state["transit"]),
                        population=sum(ecology.totals(state).values()), sightings=len(state["sightings"]),
                        ecology_events=dict(state["event_counts"]))
            start = perf_counter()
            state = ecology.replay(sim.db)
            result = dict(copies=copies, limits=asdict(limits), habitats=len(state["habitats"]),
                          groups=sum(len(group) for layers in state["groups"].values() for group in layers.values()),
                          replay_seconds=round(perf_counter()-start, 3), deterministic=True,
                          projection_sha256=ecology.sha256(ecology.encoded(state).encode()).hexdigest(), stages=stages)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--manifest", type=Path, help="Full World Manifest from a native test")
    parser.add_argument("--copies", nargs="+", type=int, default=[1, 2, 4])
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_bytes()) if args.manifest else scenario()
    rss = memory_reader()
    cases = [run(manifest, copies, rss) for copies in args.copies]
    report = dict(os=platform.platform(), processor=platform.processor(), python=platform.python_version(),
                  manifest=manifest["manifest_sha256"], source="native_manifest" if args.manifest else "synthetic",
                  cases=cases)
    args.output.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print([(case["habitats"], case["groups"], case["stages"][365]) for case in cases])


if __name__ == "__main__":
    main()
