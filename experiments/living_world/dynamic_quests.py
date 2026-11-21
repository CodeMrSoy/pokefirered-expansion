"""Project player-discovered Living World objectives into a read-only Book row."""
import struct

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
