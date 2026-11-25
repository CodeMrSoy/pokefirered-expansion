"""Find a real migrated cohort and capture it through the native land path."""
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
from time import perf_counter_ns

os.environ.setdefault("WORLD_TEST_NUZLOCKE_OFF", "1")
fixture = Path(__file__).resolve().parent / "living_world_live_emulator.py"
source = fixture.read_text(encoding="utf-8").split("with TemporaryDirectory() as temporary:")[0]
exec(compile(source, str(fixture), "exec"), globals())

import native_projection


def drain():
    while live.future or live.queue:
        live.pump(drain=True)


def sqlite_projection(db):
    return db.execute("SELECT 1 FROM sqlite_master WHERE name='projected_battles'").fetchone()


def escape():
    assert ready_to_choose()
    # The four native action positions are Fight, Bag, Pokémon and Run.
    for direction in (7, 5):
        cursor = raw("gActionSelectionCursor", 1)[0]
        if not cursor & (1 if direction == 7 else 2):
            m.press(direction, 20)
    for _ in range(25):
        if not in_battle():
            break
        if ready_to_choose():
            m.press(8, 60)
        else:
            m.press(0, 60)
    assert not in_battle()
    run(20)


want_rare = os.environ.get("WORLD_TEST_RARE_PROJECTION") == "1"
with TemporaryDirectory() as tmp:
    root = Path(tmp)
    m.inject(b"\x23" + struct.pack("<I", (m.symbols["ScrCmd_givegiftmon"] | 1) + 0x2000000)
             + struct.pack("<BBHHI", 0, 6, 7, 100, 0) + b"\x7a" + struct.pack("<BBH", 0, 0, 57) + b"\x02")
    for item in (26, 4):
        assert native("AddBagItem", item, 8)
    native("FlagSet", 0x828)
    native("FlagSet", 0x829)
    location = warp("Route24", 4, 25)
    attributes = native("MapGridGetMetatileAttributeAt", 4 + 7, 25 + 7, 255)
    assert (attributes >> 24) & 7 == 1, "The native demo must start in grass"
    with closing(WorldStartup(root, ROOT / "pokefirered.gba", Path(os.environ["MGBA_CORE"]), catalog_path)) as startup:
        startup.poll(player, player.save_bytes())
        startup.task.wait(timeout=90)
        assert startup.task.returncode == 0
        startup.poll(player, player.save_bytes())
        with closing(Simulation(startup.database)) as sim:
            with sim._write():
                ecology.initialize(sim.db, catalog["ecology_protected"])
            manifest = json.loads(sim.db.execute("SELECT document FROM starting_manifest").fetchone()[0])
            simulated = ecology.read_state(sim.db)
            for day in range(1, 366):
                ecology.evolve_day(simulated, day)
                _, rows = native_projection.wild_offer(manifest, simulated, location)
                if want_rare:
                    _, species, _ = native_projection.land_support(simulated, location)
                    ready = bool(rows) and any(mon["location"] == "3:43" and mon["layer"] == "land"
                                               and str(mon["species"]) in species and mon["species"] != 201
                                               for mon in simulated["individuals"].values())
                else:
                    ready = any(row["migrant"] and row["weight"] >= 6 for row in rows)
                if ready:
                    break
            assert ready, "No eligible migrant or notable appeared in the simulated corridor"
            for remaining in range(day * 24, 0, -744):
                sim.advance(min(remaining, 744))
            with sim._write():
                ecology.apply(sim.db, [(f"day:{n}", dict(day=n)) for n in range(1, day + 1)])
            assert ecology.replay(sim.db) == simulated

        with closing(LiveWorld(startup)) as live:
            m.run = run
            run(4)
            drain()
            run(1)
            monitor = live.ecology_monitor()["projection"]
            assert monitor["offer"] and monitor["offer"]["kind"] == native_projection.LAND, monitor
            export_projection_demo(root)
            header = next(row["header"] for row in catalog["encounters"]
                          if row["map"] == location and row["kind"] == "land")
            started = perf_counter_ns()
            attempts = 0
            projections = 0
            if os.environ.get("WORLD_PROJECTION_DIAGNOSTIC"):
                print("offer", monitor["offer"], "native", raw("gWorldProjectPort", 24).hex(), flush=True)
            for _ in range(int(os.environ.get("WORLD_PROJECTION_RETRIES", "1400"))):
                if not native("TryStandardWildLandEncounter", header, attributes, attributes & 511):
                    continue
                attempts += 1
                assert choose_when_ready(), "Native land encounter did not start"
                drain()
                with closing(Simulation(startup.database, read_only=True)) as sim:
                    seq, payload = sim.db.execute(
                        "SELECT seq,event FROM native_events WHERE json_extract(event,'$.kind')='battle_start' "
                        "ORDER BY seq DESC LIMIT 1").fetchone()
                    match = sim.db.execute(
                        "SELECT p.document,b.selection FROM projected_battles b JOIN native_projections p "
                        "ON p.stream=b.stream AND p.revision=b.revision WHERE b.stream=? AND b.battle=?",
                        (live.stream, seq)).fetchone() if sqlite_projection(sim.db) else None
                if match:
                    projections += 1
                if attempts <= 2 and os.environ.get("WORLD_PROJECTION_DIAGNOSTIC"):
                    print("sample", json.loads(payload)["flags"], raw("gWorldProjectPort", 24).hex(),
                          raw("gDexNavSpecies", 2).hex(), match is not None, flush=True)
                if match:
                    candidate = json.loads(match[0])["party"][match[1]]
                    if ("id" in candidate if want_rare else candidate["migrant"]):
                        break
                escape()
            else:
                raise AssertionError(f"No target was selected, {attempts} battles and {projections} overlays")
            selected = json.loads(match[0])["party"][match[1]]
            select_ball(True)
            for _ in range(45):
                if not in_battle():
                    break
                m.press(0, 45)
            assert not in_battle() and raw("gBattleOutcome", 1) == b"\x07"
            drain()
            report = dict(build=catalog["build"], mode=context["mode"], features=context["features"],
                          timing_samples=list(live.metrics)[-48:], day=day, attempts=attempts, selected=selected,
                          wall_ms=(perf_counter_ns() - started) / 1e6)
            with closing(Simulation(startup.database, read_only=True)) as sim:
                state = ecology.replay(sim.db)
                capture = next(row for row in reversed(state["history"]) if row["kind"] == "capture")
                assert capture["species"] == selected["species"], capture
                if want_rare:
                    uid = selected["id"]
                    assert capture["persistent_individual"] == uid and uid not in state["individuals"]
                    assert "population_adjustment" not in capture
                    assert sim.db.execute("SELECT owner FROM observed_pokemon WHERE id=?", (uid,)).fetchone() == ("player",)
                else:
                    assert capture["population_adjustment"] == -1, capture
                report["capture"] = capture
            flash = checkpoint()
        m.run = rom_run
        with closing(Simulation(continue_projection(root, flash), read_only=True)) as sim:
            assert any(row == capture for row in ecology.replay(sim.db)["history"])
        report["paired_replay"] = True

if output := os.environ.get("WORLD_PROJECTION_REPORT"):
    Path(output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print("PASS native named individual or migrated cohort, native capture and paired restoration")
