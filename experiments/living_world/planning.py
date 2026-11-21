"""Compose short plans from concrete actions offered by the authoritative world."""
from dataclasses import dataclass
import json
from time import perf_counter


@dataclass(frozen=True)
class Proposal:
    goal: str
    steps: tuple
    available: tuple


# Goals describe an observable effect; agents select their own goal for a
# decision. They may use zero or more other actions to achieve it.
GOALS = {
    "WORK": "maintain_duty",
    "REST": "recover",
    "INVESTIGATE": "verify_observation",
    "TRAIN_POKEMON": "practice",
    "REQUEST_ASSISTANCE": "get_second_opinion",
    "DECLINE_REQUEST": "preserve_commitments",
    "SHARE_INFORMATION": "help_colleague",
    "EXCHANGE_INFORMATION": "report_discovery",
    "OFFER_ASSISTANCE": "help_colleague",
}


def options_for(steps):
    return tuple(dict.fromkeys(GOALS[step.action] for step in steps if step.action in GOALS))


def choose_plan(model, ticket, available, persona):
    if model.style != "qwen3":
        raise ValueError("World planning requires Qwen3")
    goals = options_for(available)
    codes = {str(i + 1): step for i, step in enumerate(available)}
    purposes = dict(zip("ABCDEFGHI", goals))
    aliases = {
        "WORK": "work", "REST": "rest", "INVESTIGATE": "investigate", "TRAIN_POKEMON": "train",
        "REQUEST_ASSISTANCE": "ask", "ACCEPT_REQUEST": "accept request",
        "DECLINE_REQUEST": "decline request", "ARRANGE_MEETING": "arrange meeting",
        "VISIT_NPC": "meet", "SHARE_INFORMATION": "send result", "TRAVEL_TO": "travel",
        "RETURN_TO_DUTY": "return", "EXCHANGE_INFORMATION": "report findings to",
        "OFFER_ASSISTANCE": "offer help to",
    }
    def choices(values):
        return " | ".join(map(json.dumps, values))
    grammar = ('root ::= goal ":" atom (" " atom)? (" " atom)? (" " atom)? (" " atom)? (" " atom)?\n'
               f'goal ::= {choices(purposes)}\natom ::= {choices(codes)}\n')
    methods = "; ".join(f"{code} {aliases.get(step.action, step.action.lower())}" +
                        (f" {step.target}" if step.target != ticket.cause else "")
                        for code, step in codes.items())
    motives = "; ".join(f"{code} {goal.replace('_', ' ')}" for code, goal in purposes.items())
    instructions = (f"You are the {persona.role}, {persona.temperament}. Your motivation is to {persona.motive}. "
                    "Compose one short goal and ordered actions. Choose a goal letter, a colon, and the necessary "
                    "action numbers separated by spaces. Avoid repeated actions. Example format C:1 2")
    prompt = model.render_prompt(instructions, f"{ticket.context}\nGoals: {motives}.\nActions: {methods}.")
    start = perf_counter()
    raw, metrics = model.worker.generate(grammar, prompt)
    label, separator, atoms = raw.strip().partition(":")
    codes_used = atoms.split()
    if not separator or label not in purposes or not 1 <= len(codes_used) <= 6 or any(
            code not in codes for code in codes_used):
        raise ValueError("Malformed goal or action identifiers")
    return Proposal(purposes[label], tuple(codes[code] for code in codes_used), available), {
        **metrics, "decision_ms": (perf_counter() - start) * 1000,
    }
