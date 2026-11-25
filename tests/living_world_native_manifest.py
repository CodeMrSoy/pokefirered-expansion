"""Real New Game, replica resolution, gameplay parity and paired recovery."""
from contextlib import closing
import ctypes as c
import json
import os
from pathlib import Path
import sqlite3
import struct
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "experiments/living_world"
sys.path.insert(0, str(APP))
from native_world import read_context, snapshot
from simulation.engine import Simulation
from world_initialization import PairedCheckpoints, flash_identity, WorldStartup
from world_manifest import digest, import_world

# Drive the real menu and intro. The fixture's original Flash checks are covered
# explicitly after collecting the manifest, so the replica sees the first field.
fixture = ROOT / "tests/adventure_mode_menu_emulator.py"
source = fixture.read_text().split("helpers = (root / 'tests/rom_cleanup_migration_emulator.py')")[0]
disabled = os.environ.get("WORLD_TEST_NO_RANDOMIZER") == "1"
protect = os.environ.get("WORLD_TEST_PROTECT") == "1"
benchmark_trials = int(os.environ.get("WORLD_INIT_BENCHMARK_TRIALS", "0"))
full = bool(benchmark_trials and not disabled)
if disabled:
    source = source.replace("m.press(8); m.press(5); m.press(7); m.press(5); m.press(7)",
                            "m.press(5); m.press(5)")
    source = source.replace("== 23", "== 16").replace("== 87", "== 80")
    source = source.replace("87 if mode == 1 else 23", "80 if mode == 1 else 16")
    if benchmark_trials:
        source = source.replace("m.press(5); m.press(5); m.press(7)\n        assert",
                                "m.press(5); m.press(5); m.press(6)\n        assert")
        source = source.replace("== 80", "== 16").replace("80 if mode == 1 else 16", "16")
if protect:
    source = source.replace("m.press(5); m.press(5); m.press(7)\n        assert",
                            "m.press(5); m.press(5)\n        assert")
    source = source.replace("== 87", "== 23").replace("87 if mode == 1 else 23", "23")
if full:
    # Turn on field items as well. The Quantum case also enables Vidra Gyms.
    source = source.replace("m.press(5); m.press(5); m.press(7)\n        assert",
                            "m.press(5); m.press(7); m.press(5); m.press(7)\n        assert")
    source = source.replace("== 87", "== 119").replace("87 if mode == 1 else 23", "119")
    delay = int(os.environ["WORLD_INIT_SEED_DELAY"])
    source = source.replace("# Test independent category controls,",
                            f"m.run({delay})\n    # Test independent category controls,")
if options := os.environ.get("WORLD_TEST_RANDOMIZER_MASK"):
    if os.environ.get("ADVENTURE_TEST_MODE") != "0" or options not in {"1", "2", "4"} or disabled or full:
        raise ValueError("The individual randomizer fixtures use Classic mode")
    mask = int(options)
    presses = (["m.press(8)"] if mask & 1 else []) + ["m.press(5)"]
    presses += (["m.press(7)"] if mask & 2 else []) + ["m.press(5)"]
    presses += ["m.press(7)"] if mask & 4 else []
    source = source.replace("m.press(8); m.press(5); m.press(7); m.press(5); m.press(7)", "; ".join(presses))
    source = source.replace("== 23", f"== {16 | mask}").replace("else 23", f"else {16 | mask}")
if os.environ.get("WORLD_TEST_NUZLOCKE_OFF") == "1":
    source = source.replace("m.press(5); m.press(6); m.press(5); m.press(7)",
                            "m.press(5); m.press(6); m.press(5)")
    expected = {16: 0, 80: 64, 23: 7, 87: 71, 119: 103}
    import re

    source = re.sub(r"(?<= == )(16|80|23|87|119)(?=\n)|"
                    r"(?<= = )(16|80|23|87|119)(?= if mode == 1 else )|"
                    r"(?<=else )(16|80|23|87|119)(?=\n)",
                    lambda match: str(expected[int(match[0])]), source)
env = {"__file__": str(fixture)}
exec(compile(source, str(fixture), "exec"), env)
m = env["m"]
mode = env["mode"]
ptr = env["ptr"]

catalog_path = Path(os.environ["WORLD_CATALOG"]).resolve()
catalog = json.loads(catalog_path.read_bytes())
memory = lambda key: (m.lib.retro_get_memory_data(key), m.lib.retro_get_memory_size(key))
context = read_context(memory, catalog)
assert context["origin"] == 1 and context["mode"] == mode and context["starter_slot"] is None
assert context["seed"] == struct.unpack("<I", m.read(ptr("gSaveBlock2Ptr") + 3756, 4))[0]
assert (context["seed"] == 0) == disabled

# Test through the same process launcher as play.py.
class Player:
    core = m.lib

    def memory(self, key):
        return memory(key)[0]

    def memory_size(self, key):
        return memory(key)[1]

if benchmark_trials:
    from living_world_init_benchmark import measure

    helpers = (ROOT / "tests/rom_cleanup_migration_emulator.py").read_text().split("old=(m.root")[0]
    helpers = helpers.replace("import quantum_qol_emulator as m", "")
    exec(compile(helpers, "benchmark_native_save", "exec"), env)
    measure(m, Player(), env, memory, catalog, catalog_path, context, benchmark_trials,
            Path(os.environ["WORLD_INIT_CASE_RESULT"]))
    raise SystemExit(0)


with TemporaryDirectory() as tmp:
    directory = Path(tmp)
    player = Player()
    virgin_flash = c.string_at(*memory(0))
    before = snapshot(m.lib)
    startup = WorldStartup(directory, ROOT / "pokefirered.gba", Path(os.environ["MGBA_CORE"]), catalog_path)
    try:
        startup.poll(player, virgin_flash)
        assert startup.task is not None
        startup.task.wait(timeout=90)
        assert startup.task.returncode == 0
        startup.poll(player, virgin_flash)
        assert snapshot(m.lib) == before and c.string_at(*memory(0)) == virgin_flash
        report = json.loads((directory / "progress.json").read_bytes())
        assert report["stage"] == "ready"
        assert set(report["timings_ms"]) == {"replica_startup", "native_resolution", "manifest_assembly",
                                             "resolution_progress", "database_initialization"}
        assert all(value > 0 for value in report["timings_ms"].values())
        path = startup.database
        with closing(sqlite3.connect(path)) as db:
            manifest = json.loads(db.execute("SELECT document FROM starting_manifest").fetchone()[0])
        route = next(x for x in manifest["encounters"]
                     if x["table"]["map"] == [3, 19] and x["table"]["method"] == 0)
        original = route["slots"][0]["authored"]
        assert original == dict(slot=0, species=16, level=[3,3], weight=20, rod=None)
        if disabled:
            assert all(s["species"] == s["authored"]["species"]
                       for table in manifest["encounters"] for s in table["slots"])
            assert all(s["abilities"] == s["authored"]["abilities"]
                       and s["learnset"] == s["authored"]["learnset"] for s in manifest["species"] if s["status"] == "resolved")
        else:
            assert any(s["species"] != s["authored"]["species"] for s in route["slots"])
            assert any(s["learnset"] != s["authored"]["learnset"] for s in manifest["species"] if s["status"] == "resolved" and s["authored"]["learnset"])
            assert any(s["abilities"] != s["authored"]["abilities"] for s in manifest["species"] if s["status"] == "resolved")
        assert {table["table"]["kind"] for table in manifest["encounters"]} >= {"land","surf","fishing"}
        havora = [t for t in manifest["trainers"] if 743 <= t["id"] <= 750]
        assert len(havora) == 8
        assert all(t["protected"] == (mode == 0 or protect) for t in havora)
        if mode == 0 or protect:
            for team in havora:
                assert all(a["species"] == b["species"] and a["moves"] == b["moves"]
                           and a["ability"] == b["ability"] for a,b in zip(team["party"], team["authored"]["party"]))
        assert all(t["protected"] for t in manifest["trainers"] if t["id"] in (751,752))
        assert manifest["static_encounters"]
        with closing(import_world(path, manifest)) as sim:
            assert not sim.state()["pokemon"]
            sim.advance(8)
        with closing(import_world(path, manifest)) as sim:
            assert sim.state()["tick"] == 8
            sim.verify_replay()

        # Invoke the actual trainer builder through a fixture-only ARM thunk.
        # The exporter itself never uses a constructor.
        address = m.symbols["gDecompressionBuffer"] + 0x3000
        brock = next(t for t in catalog["trainers"] if t["id"] == 414)
        assembly = f""" .syntax unified
        .thumb
        .thumb_func
        push {{r4,lr}}
        sub sp,#8
        ldr r4,=414
        str r4,[sp]
        ldr r0,={m.symbols['gEnemyParty']}
        ldr r1,={brock['address']}
        movs r2,#1
        movs r3,#8
        ldr r4,={m.symbols['CreateNPCTrainerPartyFromTrainer'] | 1}
        bl invoke
        movs r0,#1
        add sp,#8
        pop {{r4,pc}}
        invoke: bx r4
        .ltorg
        """
        probe = directory / "trainer.s"
        probe.write_text(assembly, encoding="ascii")
        prefix = os.environ["ARM_NM"].removesuffix("nm")
        subprocess.run([prefix+"as", "-mthumb", "-mcpu=arm7tdmi", "-o", str(probe.with_suffix(".o")), str(probe)], check=True)
        subprocess.run([prefix+"objcopy", "-O", "binary", "-j", ".text", str(probe.with_suffix(".o")), str(probe.with_suffix(".bin"))], check=True)
        thunk = probe.with_suffix(".bin").read_bytes()

        def generated_parties():
            m.inject(b"\xb6" + struct.pack("<HBHHBH", 25, 11, 0, 0, 0, 0) + b"\x02")
            wild = m.read(m.symbols["gEnemyParty"], 100)
            m.write(address, thunk)
            m.inject(b"\x23" + struct.pack("<I", address | 1) + b"\x02")
            team = m.read(m.symbols["gEnemyParty"], 200)
            assert any(wild) and any(team) and wild != team[:100]
            return wild, team

        observed = generated_parties()
        buffer = c.create_string_buffer(before)
        assert m.lib.retro_unserialize(buffer, len(before))
        assert generated_parties() == observed
        assert m.lib.retro_unserialize(buffer, len(before))

        helpers = (ROOT / "tests/rom_cleanup_migration_emulator.py").read_text().split("old=(m.root")[0]
        helpers = helpers.replace("import quantum_qol_emulator as m", "")
        exec(compile(helpers, "manifest_native_save", "exec"), env)
        assert env["native"]("TrySavingData", 0) == 1
        flash = c.string_at(*memory(0))
        assert flash_identity(flash, catalog["save"])["seed"] == context["seed"]
        startup.record_save(flash)
        pair = directory / "checkpoints.sqlite3"
        assert pair.is_file()

        def interruption():
            raise RuntimeError("simulated process interruption before commit")
        with closing(PairedCheckpoints(pair)) as checkpoints:
            try:
                checkpoints.store(b"interrupted", path, before_commit=interruption)
            except RuntimeError as error:
                assert str(error).startswith("simulated")
            else:
                raise AssertionError("Expected write interruption")
            assert checkpoints.db.execute("SELECT count(*) FROM paired").fetchone() == (1,)

        m.lib.retro_reset()
        m.run(360)
        m.press(3)
        env["wait"]("Task_HandleMenuInput")
        m.press(8)
        m.run(500)
        continued = read_context(memory, catalog)
        assert continued["origin"] == 2 and continued["seed"] == context["seed"]
        # A fresh launcher session models app exit/restart.
        with closing(WorldStartup(directory, ROOT / "pokefirered.gba", Path(os.environ["MGBA_CORE"]), catalog_path)) as resume:
            resume.poll(player, flash)
            assert resume.database is not None
            with closing(Simulation(resume.database)) as sim:
                assert sim.state()["tick"] == 8 and sim.state()["world_uuid"] == manifest["world_uuid"]
                sim.verify_replay()

        if example := os.environ.get("WORLD_EXAMPLE"):
            Path(example).write_text(json.dumps(dict(
                version=1, rom=manifest["build"], context=context, world_uuid=manifest["world_uuid"],
                catalog_sha256=manifest["catalog_sha256"], manifest_sha256=manifest["manifest_sha256"],
                counts={key: len(manifest[key]) for key in ("maps","encounters","species","trainers","static_encounters")},
                route1=route, havora_captain=next(t for t in havora if t["id"]==745)),
                indent=2)+"\n", encoding="utf-8")
        print(f"PASS mode={mode} seed={context['seed']:08x} native manifest {manifest['manifest_sha256']}; "
              "frame and party parity, idempotent import, torn save rollback, Flash Continue")
    finally:
        startup.close()
