"""Exercise the reviewed projection through native mGBA trainer scripts."""
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
from time import perf_counter_ns

here = Path(__file__).resolve().parent
fixture = here / "living_world_live_emulator.py"
source = fixture.read_text(encoding="utf-8").split("with TemporaryDirectory() as temporary:")[0]
exec(compile(source, str(fixture), "exec"), globals())

import native_projection

report = {}
with TemporaryDirectory() as tmp:
    root = Path(tmp)
    m.inject(b"\x23" + struct.pack("<I", (m.symbols["ScrCmd_givegiftmon"] | 1) + 0x2000000)
             + struct.pack("<BBHHI", 0, 6, 7, 100, 0) + b"\x7a" + struct.pack("<BBH", 0, 0, 57) + b"\x02")
    native("FlagSet", 0x827)  # Prepared party obeys in the combat fixture.
    native("FlagSet", 0x828)
    native("FlagSet", 0x829)  # The prepared save has received Pokédex access.
    warp("ViridianForest", 7, 23)
    if os.environ.get("WORLD_PROJECTION_FALLBACK"):
        trainer(104, "ViridianForest_EventScript_Sammy")
        assert raw("gBattleOutcome", 1)[0] == 1 and native("HasTrainerBeenFought", 104)
        print("PASS native Sammy battle and defeat flag without a companion")
        raise SystemExit(0)
    with closing(WorldStartup(root, ROOT / "pokefirered.gba", Path(os.environ["MGBA_CORE"]), catalog_path)) as startup:
        startup.poll(player, player.save_bytes())
        startup.task.wait(timeout=90)
        assert startup.task.returncode == 0
        startup.poll(player, player.save_bytes())
        with closing(Simulation(startup.database)) as sim:
            with sim._write():
                ecology.initialize(sim.db, catalog["ecology_protected"])
            manifest = json.loads(sim.db.execute("SELECT document FROM starting_manifest").fetchone()[0])
            for day in range(1, 121):
                sim.advance(24)
                with sim._write():
                    ecology.apply(sim.db, [(f"day:{day}", dict(day=day, trainer_phase=1))])
                state = companion_trainers.load(sim.db)
                party = native_projection.trainer_offer(manifest, state, day)
                if party and state["counters"].get("training") and any(state["mons"][row["id"]]["xp"] for row in party):
                    break
            assert party and state["counters"].get("capture") and state["counters"].get("training")
            ecology.replay(sim.db)

        with closing(LiveWorld(startup)) as live:
            m.run = run
            run(4)
            while live.queue or live.future:
                live.pump(drain=True)
            run(1)
            offer = live.ecology_monitor()["projection"]["offer"]
            assert offer and offer["party"] == party, live.ecology_monitor().get("projection")
            export_projection_demo(root)
            if os.environ.get("WORLD_PROJECTION_BAD_PACKET"):
                live.publish_projection = lambda _: None
                native_projection.publish(player, live.projection_address, dict(offer, seed=offer["seed"] ^ 1),
                                          live.reader.frame)
                trainer(104, "ViridianForest_EventScript_Sammy")
                while live.queue or live.future:
                    live.pump(drain=True)
                monitor = live.ecology_monitor()["projection"]
                assert not monitor["history"] and monitor["rejections"][0]["flags"] == 1
                assert raw("gBattleOutcome", 1)[0] == 1 and native("HasTrainerBeenFought", 104)
                print("PASS invalid native seed rejected; authored Sammy battle completed")
                raise SystemExit(0)
            started = perf_counter_ns()
            trainer(104, "ViridianForest_EventScript_Sammy")
            while live.queue or live.future:
                live.pump(drain=True)
            assert live.failure is None, live.failure
            report["battle_wall_ms"] = (perf_counter_ns() - started) / 1e6
            with closing(Simulation(startup.database, read_only=True)) as sim:
                matched = list(sim.db.execute("SELECT individual FROM projected_individuals ORDER BY slot"))
                assert [uid for uid, in matched] == [row["id"] for row in party]
                state = companion_trainers.load(sim.db)
                assert state["actors"]["sammy"]["last_native_battle"]["outcome"] == "won"
                assert state["actors"]["sammy"]["last_native_battle"]["members"][0][3]
                assert state["mons"][party[0]["id"]]["recover_until"] > day
                report.update(build=catalog["build"], mode=context["mode"], features=context["features"],
                              timing_samples=list(live.metrics), trainer_day=day, captures=state["counters"]["capture"],
                              training=state["counters"]["training"], offer=offer,
                              battle=state["actors"]["sammy"]["last_native_battle"])
                ecology.replay(sim.db)
            assert native("HasTrainerBeenFought", 104)
            flash = checkpoint()
        m.run = rom_run

        with closing(Simulation(continue_projection(root, flash), read_only=True)) as sim:
            assert companion_trainers.load(sim.db)["actors"]["sammy"]["last_native_battle"] == report["battle"]
            ecology.replay(sim.db)
        report["paired_replay"] = True

if output := os.environ.get("WORLD_PROJECTION_REPORT"):
    Path(output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print("PASS actual Sammy battle, existing capture identity, confirmed condition and paired restoration")
