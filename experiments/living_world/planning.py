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


def goals_for(step):
    if step.action == "INVESTIGATE" and step.target == "tracks":
        return ("survey_route", "verify_observation")
    return (GOALS[step.action],) if step.action in GOALS else ()


def options_for(steps):
    return tuple(dict.fromkeys(goal for step in steps for goal in goals_for(step)))


def choose_plan(model, ticket, available, persona, planner=None):
    if model.style != "qwen3":
        raise ValueError("World planning requires Qwen3")
    goals = options_for(available)
    codes = {str(i + 1): step for i, step in enumerate(available)}
    planning_start = perf_counter()
    paths = planner.plan_paths(ticket, available) if planner is not None else None
    if paths is not None:
        goals = tuple(goal for goal in goals if goal in paths)
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
    if paths is not None:
        indices = {step: code for code, step in codes.items()}
        grammar = path_grammar(purposes, paths, indices)
    else:
        grammar = ('root ::= goal ":" atom (" " atom)? (" " atom)? (" " atom)? (" " atom)? (" " atom)?\n'
                   f'goal ::= {choices(purposes)}\natom ::= {choices(codes)}\n')
    methods = "; ".join(f"{code} {aliases.get(step.action, step.action.lower())}" +
                        (f" {step.target}" if step.target != ticket.cause else "")
                        for code, step in codes.items())
    motives = "; ".join(f"{code} {goal.replace('_', ' ')}" for code, goal in purposes.items())
    instructions = (f"{persona.role}. {persona.motive}. Pick one useful goal. "
                    "Write its letter, colon, then ordered action IDs. Use few steps. Example A:1 2.")
    prompt = model.render_prompt(instructions,
                                 f"{ticket.context[:300]}\nGoals: {motives}.\nActions: {methods}.")
    start = perf_counter()
    raw, metrics = model.worker.generate(grammar, prompt, timeout=20)
    label, separator, atoms = raw.strip().partition(":")
    codes_used = atoms.split()
    if not separator or label not in purposes or not 1 <= len(codes_used) <= 6 or any(
            code not in codes for code in codes_used):
        raise ValueError("Malformed goal or action identifiers")
    return Proposal(purposes[label], tuple(codes[code] for code in codes_used), available), {
        **metrics, "decision_ms": (perf_counter() - start) * 1000,
        "graph_ms": (start - planning_start) * 1000,
    }



def path_grammar(purposes, paths, indices):
    """Share equivalent suffixes across goal/action transitions."""
    if not purposes:
        raise ValueError("No feasible plans for the available goals")
    for limit in (None, 24, 12, 6):
        rules = {}

        def rule(trie, leading_space):
            choices = []
            for part, tail in trie.items():
                if part is None:
                    choices.append('""')
                else:
                    token = json.dumps((" " if leading_space else "") + part)
                    if any(item is not None for item in tail):
                        token += " " + rule(tail, True)
                    choices.append(token)
            form = " | ".join(choices)
            if form not in rules:
                rules[form] = f"path-{len(rules)}"
            return rules[form]

        start = []
        for label, goal in purposes.items():
            trie = {}
            for plan in paths[goal][:limit]:
                node = trie
                for step in plan:
                    node = node.setdefault(indices[step], {})
                node[None] = {}
            start.append(f'{json.dumps(label + ":")} {rule(trie, False)}')
        grammar = "root ::= " + " | ".join(start) + "\n"
        grammar += "".join(f"{name} ::= {value}\n" for value, name in rules.items())
        if len(grammar) <= 4096:
            return grammar
    raise ValueError("Feasible action graph exceeds the worker grammar budget")
