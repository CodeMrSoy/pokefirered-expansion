"""Offline planners consume observations and propose typed actions only."""

import json
from time import perf_counter

from inference import non_thinking_chat, windows_launcher_environment
from worker import ResidentWorker

from .actions import Rejected
from .region import ITEMS

GOAL_GRAMMAR = 'ambition ::= [A-Za-z] [A-Za-z ,!-]{2,44} "."'


def gemma(system, context):
    return f"<bos><start_of_turn>user\n{system}\n{context}<end_of_turn>\n<start_of_turn>model\n"


def offers(obs):
    """Ground model vocabulary in perceived opportunities and its own holdings."""
    person = obs["self"]
    here = person["location"]
    goals, actions = [], []

    def goal(label, kind, **target):
        value = dict(kind=kind, **target)
        if value not in (value for _, value in goals):
            goals.append((label, value))

    def action(label, verb, **arguments):
        value = dict(verb=verb, **arguments)
        if value not in (value for _, value in actions):
            actions.append((label, value))

    if person["goal"] and person["goal"]["status"] == "active":
        current = person["goal"]
        goals.append(("continue " + current["ambition"], current["target"]))
    for req in obs["requests"].values():
        if req["to"] == obs["actor"] and req["from"] in obs["people"]:
            peer, skill = req["from"], req["skill"]
            if person["skills"].get(skill):
                goal(f"teach {skill}", "teach", skill=skill)
                action(f"teach {skill}", "respond", peer=peer, skill=skill, decision="teach")
            action(f"decline {skill}", "respond", peer=peer, skill=skill, decision="decline")
    can_work = False
    for firm, business in obs["firms"].items():
        skill = business["skill"]
        if person["employer"] == firm:
            can_work = True
        elif business["vacancies"]:
            if skill in person["skills"]:
                action(f"take {skill} job", "employment", firm=firm)
                goal(f"get {skill} job", "employment", firm=firm)
                can_work = True
            else:
                goal(f"learn {skill} for job", "skill", skill=skill)
                goal(f"ask for {skill} lessons", "request", skill=skill)
                for key, peer in sorted(obs["people"].items(), key=lambda row: -row[1]["trust"]):
                    if key != "player":
                        action(f"ask {peer['name']} {skill}", "request", peer=key, skill=skill)
        for item in ITEMS:
            if item not in business["prices"]:
                continue
            if business["goods"].get(item, 0) and person["money"] >= business["prices"][item]:
                amount = person["goods"].get(item, 0) + 1
                action(f"buy {item}", "trade", firm=firm, item=item, count=1, side="buy")
                goal(f"own {amount} {item}", "goods", item=item, amount=amount)
            if person["goods"].get(item, 0):
                action(f"sell {item}", "trade", firm=firm, item=item, count=1, side="sell")
    if can_work:
        action("work shift", "work")
        goal(f"earn up to {person['money'] + 10} cash", "money", amount=person["money"] + 10)
    if person["energy"] < 5 or can_work:
        action("rest 6h", "rest")
        if person["energy"] < 5:
            goal("recover energy", "rested")
    for home, details in obs["housing"].items():
        if home != person["home"] and details["vacancies"] > 0 and details["rent"] <= person["money"]:
            goal(f"lease {short_place(home)}", "home", home=home)
            if home == here:
                action("lease this room", "rent", home=home)
    for route in obs["routes"].values():
        if route["open"]:
            there = route["b"] if route["a"] == here else route["a"]
            if obs["places"][there]["kind"] == "gym":
                continue
            action(f"go {short_place(there)}", "travel", to=there)
            goal(f"reach {short_place(there)}", "location", location=there)
    for key in obs["pokemon"]:
        if person["energy"] > 0 and obs["pokemon"][key]["practice"] < 100:
            action("train Pidgey", "train", pokemon=key)
            goal("practice with Pidgey", "practice", pokemon=key,
                 amount=obs["pokemon"][key]["practice"] + 1)
    return goals, actions


def short_place(place):
    return place.replace("City_", " ").replace("City", "").replace("PokemonCenter_1F", "Center")


def choices(labels):
    return " | ".join(json.dumps(label) for label in labels)


def named(rows):
    result = {}
    for label, value in rows:
        key = label
        while key in result:
            key += " again"
        result[key] = value
    return result


def peak_bytes(worker):
    """Measure peak resident bytes of the model process when available."""
    process = worker.process
    if not process:
        return None
    try:
        if worker.runtime.joinpath("sandbox.exe").is_file():
            import subprocess
            script = (
                f"$p=Get-CimInstance Win32_Process -Filter 'ParentProcessId={process.pid}'; "
                "(Get-Process -Id $p.ProcessId).PeakWorkingSet64"
            )
            return int(subprocess.check_output(["powershell", "-NoProfile", "-Command", script], text=True))
        from pathlib import Path
        status = Path(f"/proc/{process.pid}/status").read_text()
        return int(next(line.split()[1] for line in status.splitlines() if line.startswith("VmHWM:"))) * 1024
    except (OSError, ValueError, StopIteration):
        return None


class OfflinePlanner:
    def __init__(self, runtime, model=None, *, style="qwen3", timeout=30, measure_memory=False):
        self.worker = ResidentWorker(runtime, windows_launcher_environment, timeout, model=model)
        self.render = gemma if style == "gemma" else non_thinking_chat
        self.measure_memory = measure_memory

    def __call__(self, obs, forecast):
        goals, actions = offers(obs)
        person = obs["self"]
        # Stay within the existing worker's 256-token prompt limit. The full
        # observation remains available to alternate planners and for replay.
        goals, actions = named(goals[:12]), named(actions[:16])
        if not goals or not actions:
            raise ValueError("no_perceived_opportunity")
        circumstances = (
            f"{person['name']}, {person['traits'][0]}, at {short_place(person['location'])}. "
            f"Cash {person['money']}, energy {person['energy']}/5, "
            f"{'employed' if person['employer'] else 'jobless'}, "
            f"{'housed' if person['home'] else 'no home'}. "
        )
        if obs["events"]:
            event = list(obs["events"].values())[-1]
            circumstances += f"Known event: {event['kind']}. "
        if any(f["goods"].get("POTION") == 0 for f in obs["firms"].values()):
            circumstances += "Local Mart has no Potion for sale. "
        if person["memories"] and (failure := person["memories"][-1].get("rejected")):
            circumstances += f"Last plan failed: {failure}. "
        started = perf_counter()
        prompts, timings = [], []

        def generate(system, context, grammar):
            prompt = self.render(system, context)
            value, timing = self.worker.generate(grammar, prompt)
            prompts.append(prompt)
            timings.append(timing)
            return value

        goal = person["goal"]
        if goal and goal["status"] == "active" and not obs["events"]:
            ambition, target = goal["ambition"], goal["target"]
            label = next(label for label, candidate in goals.items() if candidate == target)
            raw_goal = None
        else:
            raw_goal = generate(
                "Write a personal ambition ending with a period, then | and its exact success criterion. "
                "Make it relevant to your circumstances.",
                circumstances + "\nSuccess criteria: " + ", ".join(goals),
                'root ::= ambition "|" (' + choices(goals) + ')\n' + GOAL_GRAMMAR)
            ambition, label = raw_goal.split("|")
            target = goals[label]
        steps, selections, feedback = [], [], []
        for _ in range(4):
            available = {}
            for name, action in actions.items():
                try:
                    reached, trial = forecast([*steps, action], target)
                except Rejected:
                    continue
                available[name] = (action, reached, trial)
            if not available:
                break
            effects = ", ".join(name + (" (achieves goal)" if values[1] else "")
                                for name, values in available.items())
            chosen = generate(
                "Choose exactly one action that best advances your stated goal, or wait for help.",
                circumstances + f"Goal: {label}. Steps: {', '.join(selections) or 'none'}. "
                f"Actions: {effects}. You may also wait.",
                'root ::= ' + choices([*available, "wait"]))
            selections.append(chosen)
            feedback.append({name: result[1] for name, result in available.items()})
            if chosen == "wait":
                break
            action, reached, trial = available[chosen]
            steps.append(action)
            if reached or trial is None or action["verb"] == "request":
                break
            _, current_actions = offers(trial)
            actions = named(current_actions[:16])
        raw_plan = ";".join(selections)
        evidence = dict(raw_goal=raw_goal, raw_plan=raw_plan, prompts=prompts,
                        timings=timings, forecasts=feedback, elapsed_ms=round((perf_counter() - started) * 1000),
                        peak_bytes=peak_bytes(self.worker) if self.measure_memory else None)
        return dict(ambition=ambition.strip(), goal=target, steps=steps), evidence

    def close(self):
        self.worker.close()
