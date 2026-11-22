"""Bounded, compositional planning for the two existing Pewter Mart residents."""

from copy import deepcopy
from dataclasses import dataclass
import re
import json

ACTORS = {
    "resident": "Patient, keen to contribute. Values practical experience.",
    "neighbor": "Thrifty, wary of bad bargains. Values clear records.",
}
SKILLS = ("sales", "stock")
PEER = {"resident": "neighbor", "neighbor": "resident"}
OUTCOMES = tuple(f"{kind} {skill}" for kind in ("learn", "staff", "mentor") for skill in SKILLS)
GOAL_GRAMMAR = '''root ::= word (" " word){1,7} "."
word ::= [A-Za-z] [a-z]{0,11}
'''


def initial():
    return dict(turn=0, due=None, asked={}, audit=[], people={
        actor: dict(skills=[skill], job=None, goal="", trust=0, feedback="")
        for actor, skill in zip(ACTORS, SKILLS, strict=True)
    })


@dataclass(frozen=True)
class Ticket:
    save: str
    revision: int
    actor: str
    context: str
    snapshot: dict
    purpose: str = "agency"


def achieved(person, target):
    kind, skill = target.split()
    if kind == "learn":
        return skill in person["skills"]
    if kind == "staff":
        return person["job"] == skill
    return skill in person.get("taught", [])


def unfinished(person):
    target = person.get("target")
    return target if target and not achieved(person, target) else None


def stimulus(a, actor, endorsed):
    peer = PEER[actor]
    return [a["asked"].get(peer), endorsed if actor == "resident" else False,
            a["people"][actor]["trust"], a["people"][actor]["feedback"].startswith(peer)]


def ticket(rules):
    a = rules.state.get("agency", initial())
    if (not rules.badge or rules.quarantined or rules.now is None or rules.state["open_at"] is None
            or rules.now < (a["due"] if a["due"] is not None else rules.state["open_at"])):
        return None
    candidates = list(ACTORS)
    if a["turn"] % 2:
        candidates.reverse()
    for actor in candidates:
        # Ordinary shifts need no inference. Reconsider on a new request,
        # a response from a colleague, or a player's endorsement.
        signal = stimulus(a, actor, rules.state["endorsed"])
        prior = [e for e in a["audit"] if e["actor"] == actor]
        retry = unfinished(a["people"][actor]) and prior and prior[-1].get("review") == "unmet"
        if not prior or (len(prior) < 6 and (prior[-1].get("signal") != signal or retry or
                (not prior[-1]["committed"] and (len(prior) == 1 or prior[-2]["committed"])))):
            break
    else:
        return None
    me = a["people"][actor]
    other = PEER[actor]
    detail = (f"You: {actor}. {ACTORS[actor]} Known skills: {','.join(me['skills'])}. "
              f"Job: {me['job']}. Prior goal: {me['goal']}. Trust: {me['trust']}. "
              f"Player backs counter: {rules.state['endorsed'] if actor == 'resident' else 'unknown'}. "
              f"Peer requests: {a['asked'].get(other)}. My request: {a['asked'].get(actor)}. "
              f"Last result: {me['feedback']}.")
    return Ticket(rules.world.save, rules.state["revision"], actor, detail, deepcopy(a))


def capabilities(a, actor):
    available = []
    for verb in ("practice", "ask", "teach", "decline", "work"):
        for skill in SKILLS:
            try:
                execute(deepcopy(a), actor, verb, skill)
            except ValueError:
                continue
            available.append(f"{verb} {skill}")
    return available


def generate(model, request):
    me = request.snapshot["people"][request.actor]
    target = unfinished(me)
    if target:
        goal = me["goal"]
        timing = {}
        timings = []
    else:
        targets = [t for t in OUTCOMES if not achieved(me, t)]
        grammar = GOAL_GRAMMAR.replace(' "."', ' "." "|" outcome') + "outcome ::= " + " | ".join(map(json.dumps, targets))
        prompt = model.render_prompt(
            "Write a short ambition and choose its finish condition. Learn means know a skill, "
            "staff means perform that duty, mentor means teach a peer. Sales serves shoppers. "
            "Stock organizes shelves.", request.context)
        result, timing = model.worker.generate(grammar, prompt, timeout=25)
        goal, target = result.split("|")
        goal = goal.removesuffix(".")
        timings = [timing["inference_ms"]]
    trial = deepcopy(request.snapshot)
    steps = []
    for _ in range(3):
        allowed = capabilities(trial, request.actor)
        if any(step.startswith("work ") for step in steps):
            allowed = [step for step in allowed if not step.startswith("work ")]
        if steps:
            allowed.append("finish")
        else:
            allowed.append("wait")
        prompt = model.render_prompt(
            "Choose a useful next step. Practice learns; ask requests teaching; teach answers a request; "
            "work changes duty. Finish once your target is met.",
            f"{request.context} Goal: {goal}. Target: {target}. "
            f"Target met in trial: {achieved(trial['people'][request.actor], target)}. "
            f"Steps: {', '.join(steps) or 'none'}. Options: {', '.join(allowed)}.")
        if unfinished(me):
            effects = []
            for option in allowed:
                forecast = deepcopy(trial)
                if option not in ("wait", "finish"):
                    execute(forecast, request.actor, *option.split())
                outcome = "goal reached" if achieved(forecast["people"][request.actor], target) else "still open"
                effects.append(f"{option} = {outcome}")
            prompt = model.render_prompt(
                "Your previous plan left your goal unfinished. Revise it using the predicted effects. "
                "Choose an effective step when possible. You can wait for help.",
                f"Goal: {goal}. Success: {target}. Feedback: {me['feedback']}. "
                f"Trial steps: {', '.join(steps)}. " + ". ".join(effects))
        grammar = "root ::= " + " | ".join(map(json.dumps, allowed))
        step, metrics = model.worker.generate(grammar, prompt, timeout=18)
        timings.append(metrics["inference_ms"])
        if step == "wait":
            steps.append(step)
            break
        if step == "finish":
            break
        if step not in allowed:
            raise ValueError("worker chose unavailable capability")
        execute(trial, request.actor, *step.split())
        steps.append(step)
    return goal + "|" + target + "|" + ";".join(steps), {**timing, "calls": len(timings),
                                           "inference_ms": round(sum(timings), 3)}


def execute(a, actor, verb, skill):
    me = a["people"][actor]
    peer = PEER[actor]
    if skill not in SKILLS:
        raise ValueError("unknown skill")
    if verb == "practice":
        if skill in me["skills"] or a["asked"].get(actor) == skill:
            raise ValueError("skill already learned or awaiting peer")
        me["skills"].append(skill)
    elif verb == "ask":
        if actor in a["asked"] or skill in me["skills"]:
            raise ValueError("request redundant")
        a["asked"][actor] = skill
    elif verb in ("teach", "decline"):
        if a["asked"].get(peer) != skill:
            raise ValueError("peer did not request this skill")
        if verb == "teach":
            if skill not in me["skills"]:
                raise ValueError("teacher lacks skill")
            learner = a["people"][peer]
            if skill in learner["skills"]:
                raise ValueError("learner already qualified")
            learner["skills"].append(skill)
            taught = me.setdefault("taught", [])
            if skill not in taught:
                taught.append(skill)
            learner["trust"] = min(5, learner["trust"] + 1)
        del a["asked"][peer]
        a["people"][peer]["feedback"] = f"{actor} answered {verb} {skill}"
    elif verb == "work":
        if skill not in me["skills"] or me["job"] == skill:
            raise ValueError("skill missing or already on duty")
        me["job"] = skill
    else:
        raise ValueError("unsupported capability")
    if skill in me["skills"] and a["asked"].get(actor) == skill:
        del a["asked"][actor]


def submit(rules, request, raw, timing=None, error=None):
    live = ticket(rules)
    if live is None or live.save != request.save:
        return False
    if live != request:
        if live.actor == request.actor and live.revision != request.revision:
            changed = deepcopy(rules.state)
            a = changed.setdefault("agency", initial())
            reason = "Circumstances changed. Reconsider current commitments."
            a["people"][live.actor]["feedback"] = reason
            a["due"] = rules.now
            a["audit"] = [*a["audit"][-15:], dict(actor=live.actor, proposal=str(raw)[:160],
                signal=stimulus(a, live.actor, changed["endorsed"]), checked=[], committed=False,
                reason=reason, source="superseded", timing=timing)]
            changed["revision"] += 1
            rules.store(changed)
        return False
    state = deepcopy(rules.state)
    a = state.setdefault("agency", initial())
    trial = deepcopy(a)
    decisions = []
    accepted = False
    try:
        if error:
            raise ValueError(str(error)[:64])
        if not isinstance(raw, str) or len(raw) > 160:
            raise ValueError("malformed plan")
        goal, _, plan = raw.partition("|")
        goal = goal.strip()
        person = trial["people"][request.actor]
        prior_target = unfinished(person)
        target = None
        if "|" in plan:
            target, plan = plan.split("|", 1)
            if target not in OUTCOMES:
                raise ValueError("unknown goal condition")
        if prior_target and (target != prior_target or goal != person["goal"]):
            raise ValueError("unfinished commitment changed")
        steps = plan.split(";")
        if not re.fullmatch(r"[A-Za-z][A-Za-z ']{2,94}", goal) or not 1 <= len(steps) <= 4:
            raise ValueError("malformed goal or step count")
        if sum(s.startswith("work ") for s in steps) > 1:
            raise ValueError("conflicting duties")
        if "wait" in steps and len(steps) != 1:
            raise ValueError("waiting conflicts with action")
        for step in steps:
            decisions.append(step)
            if step == "wait":
                continue
            verb, separator, skill = step.partition(" ")
            if not separator:
                raise ValueError("missing argument")
            execute(trial, request.actor, verb, skill)
        person.update(goal=goal, feedback="plan completed")
        if target:
            person["target"] = target
            met = achieved(person, target)
            person["feedback"] = "Goal reached" if met else f"Still need to {target}. Last tried {plan}"[:80]
        else:
            person.pop("target", None)
        a = state["agency"] = trial
        accepted = True
    except ValueError as exc:
        reason = str(exc)
        a["people"][request.actor]["feedback"] = f"{decisions[-1] if decisions else 'plan'}: {reason}"[:80]
    a["audit"] = [*a["audit"][-15:], dict(actor=request.actor, proposal=str(raw)[:160],
                  signal=stimulus(a, request.actor, state["endorsed"]), checked=decisions, committed=accepted, reason="ok" if accepted else reason,
                  source="worker_failure" if error else "model", timing=timing)]
    if accepted and target:
        previous = request.snapshot["people"][request.actor]
        a["audit"][-1].update(target=target, before=achieved(previous, target), after=met,
            review="met" if met else "stalled" if prior_target else "unmet")
    a["turn"] += 1
    a["due"] = rules.now + (90 if accepted else 45)
    state["revision"] += 1
    rules.store(state)
    return accepted


def validate_state(a):
    if (not isinstance(a, dict) or set(a) != set(initial()) or type(a["turn"]) is not int
            or a["turn"] < 0 or type(a["due"]) is not int or a["due"] < 0
            or not isinstance(a["people"], dict) or set(a["people"]) != set(ACTORS)
            or not isinstance(a["asked"], dict) or set(a["asked"]) - set(ACTORS)
            or not isinstance(a["audit"], list) or len(a["audit"]) > 16):
        raise ValueError("invalid agency state")
    for actor, person in a["people"].items():
        if (not isinstance(person, dict) or set(person) - {"target","taught"} != {"skills","job","goal","trust","feedback"}
                or not isinstance(person["skills"], list) or not 1 <= len(person["skills"]) <= 2
                or any(s not in SKILLS for s in person["skills"])
                or len(set(person["skills"])) != len(person["skills"])
                or person["job"] is not None and person["job"] not in person["skills"]
                or type(person["trust"]) is not int or not 0 <= person["trust"] <= 5
                or not isinstance(person["goal"], str) or len(person["goal"]) > 95
                or not isinstance(person["feedback"], str) or len(person["feedback"]) > 80):
            raise ValueError("invalid resident")
        if ("target" in person and person["target"] not in OUTCOMES
                or not isinstance(person.get("taught", []), list)
                or len(person.get("taught", [])) > len(SKILLS)
                or any(skill not in person["skills"] for skill in person.get("taught", []))):
            raise ValueError("invalid goal evidence")
        if actor in a["asked"] and (a["asked"][actor] not in SKILLS or a["asked"][actor] in person["skills"]):
            raise ValueError("invalid request")
    for entry in a["audit"]:
        if (not isinstance(entry, dict) or entry.get("actor") not in ACTORS
                or type(entry.get("committed")) is not bool or not isinstance(entry.get("signal"), list)
                or len(entry["signal"]) != 4):
            raise ValueError("invalid agency history")
