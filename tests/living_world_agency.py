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


def follow_through(path):
    world = WorldMemory(path, "follow", b"first")
    rules = world.rules
    rules.observe(0, True)
    rules.observe(50, True)
    goal = "Become a cashier|staff sales|"
    assert agency.submit(rules, agency.ticket(rules), goal + "practice stock")
    assert rules.reply(MART) == "I hope to work the counter."
    assert not rules.reply(CHECKOUT)
    assert rules.state["agency"]["audit"][-1]["review"] == "unmet"
    world.checkpoint(b"mid-goal")
    world.close()
    world = WorldMemory(path, "follow", b"mid-goal")
    rules = world.rules
    rules.observe(150, True)
    assert agency.submit(rules, agency.ticket(rules), "Organize shelves|staff stock|work stock")
    rules.observe(250, True)
    request = agency.ticket(rules)
    assert request.actor == "resident" and "Still need to staff sales" in request.context
    assert not agency.submit(rules, request, "Forget the counter|staff stock|work stock")
    rules.observe(350, True)
    assert agency.submit(rules, agency.ticket(rules), goal + "work sales")
    result = rules.state["agency"]["audit"][-1]
    assert result["after"] and not result["before"] and rules.reply(CHECKOUT)
    assert rules.reply(MART) == "I can serve customers now."
    world.close()


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        follow_through(Path(folder) / "review.sqlite")
    print("PASS unmet goal survives reload, resists substitution and reaches native sales duty")
