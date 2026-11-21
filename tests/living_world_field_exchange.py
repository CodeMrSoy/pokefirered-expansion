"""A field report may travel only along approved social contacts."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from planning import Proposal
from society import Step
from world import WorldMemory

memory = WorldMemory(":memory:", "exchange", b"start")
society = memory.society
start = 39600
society.tick(start, "pewter")
society.tick(start, "viridian")
ticket = society.decision("researcher")
trip = (Step("TRAVEL_TO", "route_2"), Step("INVESTIGATE", "tracks"),
        Step("RETURN_TO_DUTY", "museum"))
society.submit(ticket, Proposal("verify_observation", trip, society.primitives(ticket)))
for second in (28, 60, 88):
    society.tick(start+second, "viridian")
ticket = society.decision("researcher")
assert ticket.cause == "report_field_observation"
society.submit(ticket, Proposal("report_discovery", (Step("EXCHANGE_INFORMATION", "assistant"),),
                                 society.primitives(ticket)))
society.tick(start+92, "viridian")
actors = society.state["agents"]
assert actors["assistant"]["facts"]["report:tracks:researcher"]["source"] == "researcher"
assert not actors["trainer"]["facts"]
ticket = society.decision("assistant")
society.submit(ticket, Proposal("report_discovery", (Step("EXCHANGE_INFORMATION", "trainer"),),
                                 society.primitives(ticket)))
society.tick(start+96, "viridian")
received = actors["trainer"]["facts"]["report:tracks:researcher"]
assert received["source"] == "assistant" and received["origin"] == "researcher"
assert received["kind"] == "reported"
assert not society.facts_to_share("assistant", "trainer")
assert not society.facts_to_share("assistant", "researcher")
assert not society.facts_to_share("researcher", "attendant")
memory.close()
print("PASS offscreen discovery, authorized relay, preserved original witness, no echo or private broadcast")
