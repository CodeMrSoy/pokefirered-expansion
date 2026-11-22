"""Exercise independent responses, transaction rollback, save branching and agent idling."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments/living_world"))
import agency
from world import WorldMemory
from world_rules import CHECKOUT, MART


def test_world(path, cooperate):
    world = WorldMemory(path, "test", b"before")
    rules = world.rules
    rules.observe(0, True)

    def turn(t, actor, plan, accepted=True):
        rules.observe(t, True)
        ticket = agency.ticket(rules)
        assert ticket and ticket.actor == actor
        assert agency.submit(rules, ticket, plan) == accepted
        assert not agency.submit(rules, ticket, plan)

    turn(50, "resident", "Build a store ledger|ask stock;work sales")
    assert rules.reply(CHECKOUT)
    turn(150, "neighbor", "Teach my neighbor|teach stock;set badge", False)
    assert rules.state["agency"]["asked"] == {"resident":"stock"}
    assert rules.state["agency"]["people"]["resident"]["skills"] == ["sales"]
    turn(250, "neighbor", "Answer my neighbor|" + ("teach stock" if cooperate else "decline stock"))
    turn(350, "resident", "Keep clear records|" + ("work stock" if cooperate else "practice stock;work stock"))
    assert rules.state["agency"]["people"]["resident"]["trust"] == int(cooperate)
    assert rules.reply(MART) == "I am checking supplies."
    world.checkpoint(b"new")
    world.close()
    resumed = WorldMemory(path, "test", b"new")
    resumed.rules.observe(500, True)
    assert resumed.rules.reply(MART) == "I am checking supplies."
    previous = WorldMemory(path, "test", b"before")
    assert previous.rules.state["agency"]["turn"] == 4
    assert resumed.rules.endorse()
    assert agency.ticket(resumed.rules)
    assert not previous.rules.state["endorsed"]
    previous.close()
    resumed.close()


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        for choice in (False, True):
            test_world(Path(folder) / f"{choice}.sqlite", choice)
    print("PASS consent, refusal, atomic rejection, stale results, checkpoint isolation, player influence")
