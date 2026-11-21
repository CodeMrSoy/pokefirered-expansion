"""Project player-discovered Living World objectives into a read-only Book row."""
import struct
from zlib import crc32

QUEST_VIEW = struct.Struct("<4sIBBH")
BROCK_STATES = {"seeking": 1, "returned": 2, "contacted": 3, "completed_at_gym": 3,
                "cancelled": 4, "expired": 4}


def project_brock(director):
    quest = director.state["quest"]
    if not quest:
        return bytes(QUEST_VIEW.size)
    state = BROCK_STATES.get(quest["status"], 0)
    if state == 1 and quest["clue"] == "gym":
        state = 2
    if not state or not 0 < quest["plan"] <= 0xFFFFFFFF:
        return bytes(QUEST_VIEW.size)
    source = {"brock_departure_notice": 1, "gym_attendant_return_commitment": 2,
              "firsthand_brock": 3}.get(quest["source"], 0)
    if not source:
        return bytes(QUEST_VIEW.size)
    return QUEST_VIEW.pack(b"LWQ9", quest["plan"], state, source, 0)


def museum_exchange(society, actor, *, accepted=False):
    """Discover an actual staff request, or deliver its status to the issuer."""
    state = society.state
    objective = state.get("museum_objective")
    if actor == "assistant":
        event, request = next(((event, request) for event, request in state["requests"].items()
                               if request["sender"] == "researcher" and request["recipient"] == actor
                               and request["status"] in ("pending", "accepted")
                               and request["expires"] > society.now), (None, None))
        if request and (not objective or objective["event"] != event):
            if accepted:
                state["museum_objective"] = dict(event=event, source=actor, delivered=False)
                society.persist()
            return "The volunteer asked me\nfor a second look.\fMuseum Follow-up\nCheck in with the volunteer."
    if actor == "researcher" and objective and project_museum(society)[8] == 1:
        if accepted:
            objective["delivered"] = True
            society.record(actor, "player_delivered_report", event=objective["event"], source="assistant")
            society.persist()
        return "Thanks for the update.\nI'll check in with my peer."
    return None


def settle_museum(society):
    objective = society.state.get("museum_objective")
    if not objective or objective.get("final"):
        return False
    view = project_museum(society)[8]
    if view in (3, 4):
        objective["final"] = view
        return True
    return False


def project_museum(society):
    objective = society.state.get("museum_objective")
    if not objective or objective["source"] != "assistant":
        return bytes(QUEST_VIEW.size)
    request = society.state["requests"].get(objective["event"])
    if objective.get("final"):
        status = objective["final"]
        source = 3 if status == 3 else 1
    elif objective["delivered"] or (request and request["status"] == "resolved"):
        status, source = 3, 3
    elif not request or request["status"] in ("expired", "declined", "interrupted"):
        status, source = 4, 1
    elif society.now >= request["expires"]:
        status, source = 4, 1
    else:
        status, source = 1, 1
    return QUEST_VIEW.pack(b"LQM1", crc32(objective["event"].encode()) or 1, status, source, 0)


REGIONAL_STATES = {"active": 1, "completed": 3, "expired": 4, "withdrawn": 5}


def regional_exchange(population, actor, *, accepted=False):
    state = population.state
    objective = state.get("objective")
    if actor == "assistant" and (not objective or objective["status"] != "active"):
        for id_, event in state["events"].items():
            if event["kind"] != "survey_support" or event["audience"] != "museum_desk" or event["status"] != "active":
                continue
            if objective and objective["event"] == id_:
                continue
            if accepted:
                state["objective"] = {"event": id_, "status": "active", "source": "museum_desk"}
                population.persist()
            return "A survey team needs help.\nPass word to the volunteer.\fSurvey Notes added\nto your Quest Book."
    if actor == "researcher" and objective and objective["status"] == "active":
        if accepted:
            objective["status"] = "completed"
            objective["delivered"] = True
            population.persist()
        return "Thanks for the survey note.\nI'll tell the field team."
    return None


def project_regional(population):
    objective = population.state.get("objective") if population else None
    if not objective or objective["source"] != "museum_desk" or objective["status"] not in REGIONAL_STATES:
        return bytes(QUEST_VIEW.size)
    return QUEST_VIEW.pack(b"LW11", crc32(objective["event"].encode()) or 1,
                           REGIONAL_STATES[objective["status"]], 1, 0)
