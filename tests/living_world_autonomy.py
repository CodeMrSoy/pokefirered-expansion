"""Replay the Phase 13 policy and capture bounded, seed-dependent histories."""

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from autonomy import DESK, MUSEUM, OFFER, REPORT, SCOUTS
from bridge import validate
from world import WorldMemory


def play(seed, assist, chooser=lambda ticket: ticket.fallback):
    memory = WorldMemory(":memory:", "replay", seed.to_bytes(2, "little"))
    pilot = memory.autonomy
    pilot.advance(0, False)
    assert pilot.decision() is None
    pilot.advance(10000, True)
    for second in range(10000, 10900):
        pilot.advance(second, True)
        if ticket := pilot.decision():
            assert pilot.submit(ticket, chooser(ticket), "fallback")
        event = pilot.state["event"]
        if event:
            scout = SCOUTS[event["site"]]
            uninvolved = next(actor for actor in SCOUTS.values() if actor != scout)
            assert pilot.reply(uninvolved) == (None, None)
            for actor in (scout, DESK, OFFER, REPORT):
                message, token = pilot.reply(actor)
                if message:
                    validate(json.dumps({"action": "SAY_DIALOGUE", "text": message}))
                    if assist and token:
                        assert pilot.accept(token)
        if pilot.state["history"]:
            break
    event = pilot.state["history"][0]
    assert pilot.decision() is None
    memory.close()
    return event


def persistence():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "living-world.sqlite3"
        world = WorldMemory(path, "test", b"before")
        pilot = world.autonomy
        pilot.advance(100, True)
        pilot.advance(130, True)
        start = pilot.decision()
        assert not pilot.submit(start, "Viridian clone Brock", "qwen")
        assert pilot.state["event"] is None
        assert pilot.submit(start, start.options[0], "fallback")
        assert not pilot.submit(start, start.options[0], "fallback")
        pilot.advance(142, True)
        response = pilot.decision()
        assert pilot.submit(response, "inspect", "fallback")
        event = pilot.state["event"]
        witness = pilot.reply(SCOUTS[event["site"]])[1]
        assert pilot.accept(witness) and not pilot.accept(witness)
        assert pilot.reply(OFFER)[0]
        assert pilot.accept(pilot.reply(REPORT)[1])
        world.checkpoint(b"after")
        assert not pilot.submit(response, "inspect", "qwen")
        state = pilot.state
        world.close()
        reused = WorldMemory(path, "test", b"after")
        assert reused.autonomy.state == state
        reused.autonomy.advance(2000, True)
        assert reused.autonomy.state["history"][0]["result"] == "filed_with_player"
        assert reused.autonomy.state["history"][0]["player_report"]["kind"] == "relayed"
        assert reused.autonomy.state["player_trust"] == 1
        assert reused.autonomy.reply(DESK)[0] == "We filed your account.\nI remember that inquiry."
        reused.checkpoint(b"before")
        assert reused.autonomy.state["event"]["player"] == "reported"
        reused.close()
        another = WorldMemory(path, "other-save", b"after")
        assert another.autonomy.state["event"] is None
        another.close()


def history(event):
    return (event["site"], event["topic"], event["lead"],
            tuple(sorted(event["actions"].items())), event["player"], event["result"])


def main():
    start = perf_counter()
    without = [history(play(seed, False)) for seed in range(32)]
    with_player = [history(play(seed, True)) for seed in range(32)]
    assert without == [history(play(seed, False)) for seed in range(32)]
    assert with_player == [history(play(seed, True)) for seed in range(32)]
    assert len(set(without)) >= 12
    assert any(a[-1] != b[-1] for a, b in zip(without, with_player))
    assert any("decline" in dict(entry[3]).values() for entry in without)
    assert any("compare" in dict(entry[3]).values() for entry in without)
    persistence()
    summary = {
        "seeds": 32, "distinct_unassisted_histories": len(set(without)),
        "seeds_with_outcome_changed_by_player": sum(a[-1] != b[-1] for a, b in zip(without, with_player)),
        "unassisted_outcomes": sorted({a[-1] for a in without}),
        "example_unassisted": without[:4], "example_player_intervention": with_player[:4],
    }
    print(json.dumps(summary, indent=2))
    print(f"replay and checkpoint test: {(perf_counter()-start)*1000:.1f} ms", file=sys.stderr)


if __name__ == "__main__":
    main()
