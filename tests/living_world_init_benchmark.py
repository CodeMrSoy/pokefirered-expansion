"""Repeat real native New Game, save pairing and Continue on the local platform."""
import argparse
from contextlib import closing
import ctypes as c
from hashlib import file_digest
import json
import os
from pathlib import Path
import platform
from statistics import median
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter_ns, sleep

ROOT = Path(__file__).resolve().parents[1]


def measure(rom, player, fixture, memory, catalog, catalog_path, context, trials, output):
    from native_world import read_context, snapshot
    from platform_io import atomic_write
    from simulation.engine import Simulation
    from world_initialization import WorldStartup, flash_identity

    new_game = snapshot(player.core)
    virgin_flash = c.string_at(*memory(0))
    assert fixture["native"]("TrySavingData", 0) == 1
    flash = c.string_at(*memory(0))
    assert flash_identity(flash, catalog["save"])["seed"] == context["seed"]
    player.core.retro_reset()
    rom.run(360)
    rom.press(3)
    fixture["wait"]("Task_HandleMenuInput")
    rom.press(8)
    rom.run(500)
    resumed = read_context(memory, catalog)
    assert resumed["origin"] == 2 and resumed["seed"] == context["seed"]
    continued = snapshot(player.core)
    rows = []

    def restore(data):
        buffer = c.create_string_buffer(data)
        assert player.core.retro_unserialize(buffer, len(data))

    def launcher(path):
        return WorldStartup(path, ROOT / "pokefirered.gba", Path(os.environ["MGBA_CORE"]), catalog_path)

    with TemporaryDirectory(prefix="quantum-world-benchmark-") as scratch:
        for trial in range(trials):
            restore(new_game)
            path = Path(scratch) / str(trial)
            with closing(launcher(path)) as startup:
                start = perf_counter_ns()
                startup.poll(player, virgin_flash)
                assert startup.task is not None
                # Keep the player core running at approximately its normal cadence.
                next_frame = start
                while startup.task.poll() is None:
                    now = perf_counter_ns()
                    if now - start > 90_000_000_000:
                        raise TimeoutError("World benchmark initialization timed out")
                    if now >= next_frame:
                        player.core.retro_run()
                        next_frame += 16_742_706
                    else:
                        sleep((next_frame - now) / 1e9)
                assert startup.task.returncode == 0
                startup.poll(player, virgin_flash)
                ready = perf_counter_ns()
                report = json.loads((path / "progress.json").read_bytes())
                assert report["stage"] == "ready"
                stages = dict(report["timings_ms"], new_game_ready=(ready - start) / 1e6)
                stages["launcher_overhead"] = stages["new_game_ready"] - sum(report["timings_ms"].values())
                assert all(value >= 0 for value in stages.values())
                start = perf_counter_ns()
                atomic_write(path / "benchmark.sav", flash)
                startup.record_save(flash)
                stages["save_association"] = (perf_counter_ns() - start) / 1e6
                world = startup.world_uuid
            restore(continued)
            with closing(launcher(path)) as resume:
                start = perf_counter_ns()
                resume.poll(player, flash)
                stages["continue_ready"] = (perf_counter_ns() - start) / 1e6
                assert resume.database is not None
                with closing(Simulation(resume.database, read_only=True)) as database:
                    assert database.state()["world_uuid"] == world
            rows.append(stages)
    output.write_text(json.dumps(dict(context=context, samples_ms=rows), indent=2), encoding="utf-8")


def summarize(samples):
    return {stage: dict(median=round(median(row[stage] for row in samples), 2),
                        worst=round(max(row[stage] for row in samples), 2)) for stage in samples[0]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path, help="Compiled world-catalog.json for the local ROM")
    parser.add_argument("output", type=Path, help="JSON report, including every measured sample")
    parser.add_argument("--trials", type=int, default=7)
    args = parser.parse_args()
    if args.trials < 2:
        parser.error("--trials must be at least 2")
    catalog_path = args.catalog.resolve()
    cases = []
    with TemporaryDirectory(prefix="quantum-world-cases-") as scratch:
        for name, delay in (("disabled", 0), ("full_a", 0), ("full_b", 37), ("full_c", 103)):
            path = Path(scratch) / f"{name}.json"
            environment = dict(os.environ, WORLD_CATALOG=str(catalog_path),
                               WORLD_INIT_CASE_RESULT=str(path), WORLD_INIT_BENCHMARK_TRIALS=str(args.trials),
                               WORLD_INIT_SEED_DELAY=str(delay), ADVENTURE_TEST_MODE="1",
                               WORLD_TEST_NO_RANDOMIZER="1" if name == "disabled" else "0",
                               WORLD_TEST_PROTECT="0", QUANTUM_QA_OUTPUT=str(Path(scratch) / name))
            subprocess.run([sys.executable, "-B", str(ROOT / "tests/living_world_native_manifest.py")],
                           cwd=ROOT, env=environment, check=True)
            result = json.loads(path.read_bytes())
            expected_features = 0 if name == "disabled" else 255
            assert result["context"]["features"] == expected_features
            cases.append(dict(name=name, **result, summary_ms=summarize(result["samples_ms"])))
            print(f"{name} seed={result['context']['seed']:08x}  "
                  f"New Game={cases[-1]['summary_ms']['new_game_ready']}  "
                  f"Continue={cases[-1]['summary_ms']['continue_ready']}", flush=True)
    assert len({case["context"]["seed"] for case in cases}) == len(cases), "Seeds must differ"
    cat = json.loads(catalog_path.read_bytes())
    cpu = platform.processor()
    cpuinfo = Path("/proc/cpuinfo")
    if not cpu and cpuinfo.is_file():
        cpu = next((line.split(":", 1)[1].strip() for line in cpuinfo.read_text().splitlines()
                    if line.startswith("model name")), "")
    with Path(os.environ["MGBA_CORE"]).open("rb") as core:
        core_sha256 = file_digest(core, "sha256").hexdigest()
    report = dict(system=platform.platform(), cpu=cpu, python=platform.python_version(),
                  trials_per_case=args.trials, timing_unit="milliseconds", rom=cat["build"],
                  mgba_core_sha256=core_sha256, cases=cases)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
