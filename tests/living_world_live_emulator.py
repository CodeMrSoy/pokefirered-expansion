"""Exercise the live native event stream with mGBA and real battle commands."""
from contextlib import closing
import ctypes as c
import json
import os
import shutil
import sqlite3
from pathlib import Path
from statistics import median
import struct
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter_ns

ROOT = Path(__file__).resolve().parents[1]
fixture = ROOT / "tests/living_world_native_manifest.py"
prefix = fixture.read_text().split("if benchmark_trials:\n    from living_world_init_benchmark")[0]
env = {"__file__": str(fixture)}
exec(compile(prefix, str(fixture), "exec"), env)
m, memory, catalog, catalog_path, context, Player = (env[key] for key in
    ("m", "memory", "catalog", "catalog_path", "context", "Player"))
from live_world import LiveWorld
from native_world import snapshot
from simulation.engine import Simulation
from world_initialization import WorldStartup

helpers = (ROOT / "tests/rom_cleanup_migration_emulator.py").read_text().split("old=(m.root")[0]
exec(compile(helpers.replace("import quantum_qol_emulator as m", ""), "live native save", "exec"), env)
native = env["native"]
port = catalog["ports"]["observation"]
history = []
poll_ms = []
frame_samples = int(os.environ.get("WORLD_LIVE_EXTENDED_FRAMES", "11000"))


class PlayerCore(Player):
    def save_bytes(self):
        return c.string_at(*memory(0))


player = PlayerCore()
video = m.VIDEO(lambda *args: None)
if not os.environ.get("WORLD_TEST_SCREEN"):
    m.lib.retro_set_video_refresh(video)
rom_run = m.run
child = None
live = None


def run(frames):
    for _ in range(frames):
        m.lib.retro_run()
        if live is not None:
            start = perf_counter_ns()
            live.poll(player)
            poll_ms.append((perf_counter_ns() - start) / 1e6)
            assert live.failure is None, live.failure


def restore(state):
    data = c.create_string_buffer(state)
    assert m.lib.retro_unserialize(data, len(state))


def raw(symbol, size, offset=0):
    return m.read(m.symbols[symbol] + offset, size)


def in_battle():
    return bool(raw("gMain", 1, 0x439)[0] & 2)


def warp(name, x, y):
    group, number = next(row["id"] for row in catalog["maps"] if row["name"] == name)
    m.inject(b"\x39" + struct.pack("<BBBhh", group, number, 255, x, y) + b"\x27\x6b\x02")
    run(48)
    return [group, number]


nm = subprocess.check_output([os.environ["ARM_NM"], str(ROOT / "pokefirered.elf")], text=True)
action = next(int(line.split()[0], 16) | 1 for line in nm.splitlines()
              if line.endswith(" HandleInputChooseAction")
              and 0 < int(line.split()[0], 16) - m.symbols["PlayerHandleChooseAction"] < 0x200)


def player_controller(function):
    controllers = struct.unpack("<4I", raw("gBattlerControllerFuncs", 16))
    return next((slot for slot in (0, 2) if controllers[slot] == function), None)


def ready_to_choose():
    return player_controller(action) is not None


def choose_when_ready():
    for frame in range(2200):
        if ready_to_choose():
            return True
        if not in_battle() and frame >= 320:
            return False
        # Advance printed battle text. Check after the individual pressed frame
        # so a new action prompt cannot consume a held confirmation.
        if frame % 90 == 0:
            m.keys.add(8)
        run(1)
        m.keys.clear()
    raise AssertionError("Native battle action menu timed out")


def select_ball(second):
    assert ready_to_choose()
    if not raw("gActionSelectionCursor", 1)[0] & 1:
        m.press(7, 20)
    m.press(8, 110)
    assert env["env"]["task"]("Task_BagMenu_HandleInput") is not None
    for _ in range(3):
        if int.from_bytes(raw("gBagPosition", 2, 6), "little") == 2:
            break
        m.press(7, 65)
    assert int.from_bytes(raw("gBagPosition", 2, 6), "little") == 2
    if second:
        m.press(5, 12)
    m.press(8, 65)
    m.press(8, 350)


def gameplay_bytes():
    return {key: raw(key, size).hex() for key, size in
            (("gRngValue", 16), ("gRng2Value", 16), ("gPlayerParty", 600), ("gBattleOutcome", 1),
             ("gPlayerPartyCount", 1))}


def wild_capture():
    warp("Route1", 10, 20)
    m.inject(b"\xb6" + struct.pack("<HBHHBH", 143, 30, 0, 0, 0, 0) + b"\xb7\x6b\x02")
    assert choose_when_ready(), "Wild battle failed to start"
    select_ball(False)
    assert choose_when_ready(), "Weak ball unexpectedly ended the fixture battle"
    select_ball(True)
    for _ in range(70):
        if not in_battle():
            break
        m.press(0, 45)
    assert not in_battle() and raw("gBattleOutcome", 1) == b"\x07"
    assert raw("gPlayerPartyCount", 1) == b"\x02"
    run(45)


def trainer(trainer_id):
    none = m.symbols["gText_EmptyString3"]
    script = b"\x5c" + struct.pack("<BBHIIIBHIIIIIH", 0x34, 0, trainer_id,
                                    0, none, 0, 0, 0, 0, 0, 0, 0, 0, 0) + b"\x02"
    m.inject(script)
    assert choose_when_ready(), f"Trainer {trainer_id} did not start"
    for _ in range(100):
        if not in_battle():
            break
        slot = player_controller(action)
        if slot is not None:
            cursor = raw("gActionSelectionCursor", 1, slot)[0]
            if cursor & 1:
                m.press(6, 15)
            if cursor & 2:
                m.press(4, 15)
            m.press(8, 45)
        elif any(player_controller(m.symbols[name] | 1) is not None for name in
                 ("HandleInputChooseMove", "HandleInputChooseTarget", "HandleInputShowTargets")):
            m.press(8, 90)
        else:
            m.press(0, 90)  # Advance text and decline optional switches.
    if in_battle() and os.environ.get("WORLD_TEST_SCREEN"):
        m.snap(f"trainer-stuck-{trainer_id}")
        print("battle-debug", raw("gBattleOutcome", 1).hex(), raw("gBattlerControllerFuncs", 16).hex())
    assert not in_battle(), f"Trainer battle {trainer_id} did not end"
    assert raw("gBattleOutcome", 1)[0] in (1, 2)
    run(75)


def play():
    wild_capture()
    wild = gameplay_bytes()
    native("FlagSet", 0x827)  # Fixture high-level party obeys after the eighth badge.
    native("HealPlayerParty")
    m.inject(b"\x7a" + struct.pack("<BBH", 1, 0, 323) + b"\x02")
    warp("PewterCity_Gym", 6, 6)
    trainer(751)  # Practice party is always protected.
    protected = gameplay_bytes()
    native("HealPlayerParty")
    m.inject(b"\x7a" + struct.pack("<BBH", 0, 0, 605) + b"\x02")
    warp("Havora_Gym", 10, 15)
    trainer(743)  # The native Vidra option decides whether this team is protected.
    return dict(wild=wild, protected_trainer=protected, havora_trainer=gameplay_bytes())


def checkpoint():
    assert native("TrySavingData", 0) == 1
    run(6)
    while live.queue or live.future is not None:
        live.pump(drain=True)
    return player.save_bytes()


with TemporaryDirectory() as temporary:
    path = Path(temporary)
    m.inject(b"\x23" + struct.pack("<I", (m.symbols["ScrCmd_givegiftmon"] | 1) + 0x2000000)
             + struct.pack("<BBHHI", 0, 6, 7, 100, 0) + b"\x7a" + struct.pack("<BBH", 0, 0, 57)
             + b"\x02")
    for item in (26, 4):
        assert native("AddBagItem", item, 8)
    opening = snapshot(m.lib)
    original_flash = player.save_bytes()
    with closing(WorldStartup(path / "interrupted", ROOT / "pokefirered.gba",
                              Path(os.environ["MGBA_CORE"]), catalog_path)) as interrupted:
        interrupted.poll(player, original_flash)
        assert interrupted.task is not None
        interrupted.task.kill()
        interrupted.task.wait(timeout=15)
        interrupted.poll(player, original_flash)
        assert interrupted.database is None
        assert snapshot(m.lib) == opening
    with closing(WorldStartup(path, ROOT / "pokefirered.gba", Path(os.environ["MGBA_CORE"]), catalog_path)) as startup:
        startup.poll(player, player.save_bytes())
        assert startup.task is not None
        startup.task.wait(timeout=90)
        assert startup.task.returncode == 0
        startup.poll(player, player.save_bytes())
        with closing(LiveWorld(startup)) as attached:
            live = attached
            m.run = run
            first = play()
            idle_state = snapshot(m.lib)
            rss_file = Path("/proc/self/statm")

            def rss():
                return int(rss_file.read_text().split()[1]) * os.sysconf("SC_PAGE_SIZE") if rss_file.exists() else None

            measurements = [rss()]
            run(frame_samples // 2)
            measurements.append(rss())
            run(frame_samples - frame_samples // 2)
            measurements.append(rss())
            flash = checkpoint()
            database = startup.database
            with closing(Simulation(database, read_only=True)) as sim:
                events = [json.loads(row[0]) for row in sim.db.execute(
                    "SELECT event FROM native_events ORDER BY seq")]
                assert sim.verify_replay() >= sim.state()["tick"]
                assert sim.state()["tick"] >= frame_samples // 3600
                event_count = len(events)
                assert events[-1]["kind"] == "save"
                assert sim.db.execute("SELECT ack FROM native_streams").fetchone() == (events[-1]["seq"],)
                assert len([event for event in events if event["kind"] == "capture"]) == 1
                assert any(event["kind"] == "ball_failed" for event in events)
                assert any(event["kind"] == "battle_end" and event["outcome"] == "caught" for event in events)
                trainers = {event["actor"] for event in events if event["kind"] == "battle_start"
                            and event["battle_kind"] == "trainer"}
                assert trainers == {743, 751}, trainers
                starting = json.loads(sim.db.execute("SELECT document FROM starting_manifest").fetchone()[0])
                for trainer_id in trainers:
                    definition = next(row for row in starting["trainers"] if row["id"] == trainer_id)
                    actual = [event["mon"] for event in events if event["kind"] == "battle_mon"
                              and event["actor"] == trainer_id]
                    assert len(actual) == len(definition["party"])
                    for mon, member in zip(actual, definition["party"], strict=True):
                        if member["status"] == "resolved":
                            assert [mon[field] for field in ("species", "ability", "moves", "level")] == [
                                member[field] for field in ("species", "ability", "moves", "level")]

                assert len([event for event in events if event["kind"] == "battle_end"]) == 3
                assert sim.db.execute("SELECT count(*) FROM observed_aliases").fetchone() == (1,)
                assert sim.db.execute("SELECT count(*) FROM observed_party").fetchone() == (2,)
                tick = sim.state()["tick"]
            restore(idle_state)
            attached.poll(player)
            assert attached.failure and "rolled back" in attached.failure
            live = None
            m.run = rom_run
            metrics = list(attached.metrics)

        def control(*, disable_native_recorder=False):
            c.memmove(memory(0)[0], original_flash, len(original_flash))
            restore(opening)
            if disable_native_recorder:
                m.write(port, b"\0\0\0\0")
            return play()

        second = control()
        assert second == first, {stage: [key for key in fields if fields[key] != second[stage][key]]
                                 for stage, fields in first.items()}
        recorder_bypass_differences = None
        if os.environ.get("WORLD_LIVE_DEBUG_NATIVE_OFF"):
            third = control(disable_native_recorder=True)
            recorder_bypass_differences = {stage: [key for key in fields if fields[key] != third[stage][key]]
                                           for stage, fields in first.items()}
            print("Recorder-off diagnostics", recorder_bypass_differences, flush=True)

    # Re-enter Continue from real Flash under a fresh host world instance.
    c.memmove(memory(0)[0], flash, len(flash))
    m.lib.retro_reset()
    m.run(360)
    m.press(3)
    env["env"]["wait"]("Task_HandleMenuInput")
    m.press(8)
    m.run(500)
    corrupt = path / "corrupt"
    corrupt.mkdir()
    shutil.copyfile(path / "checkpoints.sqlite3", corrupt / "checkpoints.sqlite3")
    with closing(sqlite3.connect(corrupt / "checkpoints.sqlite3")) as db, db:
        db.execute("UPDATE paired SET world=?", (b"corrupted world",))
    for root in (path, path / "missing", corrupt):
        with closing(WorldStartup(root, ROOT / "pokefirered.gba", Path(os.environ["MGBA_CORE"]), catalog_path)) as resumed:
            resumed.poll(player, flash)
            if root != path:
                assert resumed.database is None and resumed.context["origin"] == 2
                continue
            with closing(Simulation(resumed.database, read_only=True)) as sim:
                assert sim.state()["tick"] == tick
                assert sim.db.execute("SELECT count(*) FROM native_events").fetchone() == (event_count,)

    batches = {name: [ms for kind, _, ms in metrics if kind == name]
               for name in ("event_latency", "ingestion", "tick", "checkpoint")}
    performance = dict(frames=frame_samples, samples=len(poll_ms), rss_bytes=measurements,
                       poll_ms=dict(median=median(poll_ms), worst=max(poll_ms)),
                       **{f"{name}_ms": dict(median=median(values), worst=max(values), batches=len(values))
                          for name, values in batches.items() if values})
    report = dict(build=catalog["build"], seed=context["seed"], mode=context["mode"], features=context["features"],
                  events=events, performance=performance, host_attachment_parity=True,
                  recorder_bypass_differences=recorder_bypass_differences)
    if output := os.environ.get("WORLD_LIVE_REPORT"):
        Path(output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"PASS live capture, failed throw, trainer parties, maps, RNG parity, save/Continue and rollback: {performance}")
