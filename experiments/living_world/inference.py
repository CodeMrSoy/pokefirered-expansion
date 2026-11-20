"""Watts's local dialogue and action proposals."""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from time import perf_counter

from bridge import validate
from knowledge import prompt_facts, retrieve
from worker import ResidentWorker
from world import Encounter
from profiles import PROFILES

TOPICS = {
    "Pikachu": "Pikachu can spark near the computer. Watts likes Electric Pokemon.",
    "Squirtle": "Squirtle likes water. The town pond is next to Watts.",
}
FIRST_LINES = {
    "Pikachu": ("Pikachu, watch those sparks!", "Pikachu, mind my cables!"),
    "Squirtle": ("Squirtle, ready for a dip?", "Squirtle, fancy a swim?"),
}
SECOND_LINES = {
    "Pikachu": ("My PC's had enough shocks.", "That would fry my PC.", "Stay clear of my PC."),
    "Squirtle": ("The pond's nice and cool.", "That shell looks sturdy.", "The water's clear today."),
}


def choices(lines):
    return "(" + " | ".join(json.dumps(line) for line in lines) + ")"


def dialogue_options(species, encounter, facts):
    if encounter.npc != "pc_resident":
        profile = PROFILES[encounter.npc]
        greeting = profile["greeting_lines"]
        reaction = profile["seen_lines"]
        if encounter.remembered:
            first = ("Good to see you both again.", greeting[0])
        elif encounter.visible_species == profile["favorite_species"] and species and len(species) <= 18:
            first = (f"Oh, a {species}!", reaction[0])
        else:
            first = (reaction[0], greeting[0]) if encounter.visible_species else (greeting[0],)
        second = (reaction[1], greeting[1]) if encounter.visible_species else (greeting[1],)
    elif encounter.completes_quest:
        first, second = ("Survey complete!",), ("You earned my repair tips.",)
    elif encounter.quest == "completed":
        first, second = ("Here is a repair tip.", "Back for a repair tip?"), (
            "Back up your field notes.", "Keep water away from PCs.",
        )
    elif encounter.remembered and species in FIRST_LINES:
        first, second = (f"Hello again, {species}!", f"I remember you, {species}!"), SECOND_LINES[species]
    elif species in FIRST_LINES:
        first, second = FIRST_LINES[species], SECOND_LINES[species]
    else:
        known_name = species and re.fullmatch(r"[A-Za-z][A-Za-z0-9 .'-]{0,19}", species)
        first = (f"{species}, hello!",) if known_name else ("Hello, trainer!", "Good to see you!")
        second = ("Your PC stores items.", "The pond's nice and cool.")
    grounded = tuple(dict.fromkeys(fact.line for fact in facts if fact.line))
    if grounded and not encounter.completes_quest and encounter.quest != "completed":
        second = grounded
        if not encounter.remembered and species in FIRST_LINES:
            reactions = {
                "oak": (f"Study that {species} closely.", f"Look at that {species}."),
                "blue": (f"You train that {species}?", f"I see you brought {species}."),
                "daisy": (f"Hello there, {species}.", f"{species}, you look cozy."),
            }
            first = reactions.get(encounter.npc, first)
        if encounter.npc == "oak" and not encounter.remembered and any(
            fact.key == "evolution:PIKACHU" for fact in facts
        ):
            first = ("Pikachu can become Raichu.", "That Pikachu could evolve.")
    return first, second


def windows_launcher_environment():
    required = ("SystemRoot", "LOCALAPPDATA")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError("Windows sandbox launcher needs " + ", ".join(missing))
    return {name: os.environ[name] for name in required}


def chat(instructions, observation):
    return (
        f"<|im_start|>system\n{instructions}<|im_end|>\n"
        f"<|im_start|>user\n{observation}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )


@dataclass(frozen=True)
class Proposal:
    dialogue: str
    action: str
    metrics: dict
    context_sent: str
    knowledge: tuple = ()


class LocalModel:
    def __init__(self, runtime: Path, species_names: dict, timeout=8, *,
                 catalog=None, fact_limit=2, fact_budget=220):
        self.species_names = species_names
        self.catalog = catalog
        self.fact_limit = fact_limit
        self.fact_budget = fact_budget
        self.worker = ResidentWorker(runtime, windows_launcher_environment, timeout)

    def plan(self, encounter):
        start = perf_counter()
        facts = retrieve(self.catalog, encounter, limit=self.fact_limit, budget=self.fact_budget) if self.catalog else ()
        retrieved = perf_counter()
        species = self.species_names.get(str(encounter.visible_species))
        profile = PROFILES[encounter.npc]
        instructions = (
            f"You are {profile['name']}, a {profile['role']}. "
            f"You are {', '.join(profile['traits'])}. {profile['primary_goal']} "
            f"{profile['secondary_motivation']} Use known facts and personal observations. "
            "Keep beliefs and rumors uncertain."
        )
        observation = f"Visible Pokemon: {species or 'none'}. "
        if encounter.remembered:
            observation += "You remember meeting this Pokemon. "
        if encounter.npc == "pc_resident":
            observation += f"Trust: {encounter.trust}. Survey: {encounter.quest}. "
            if self.catalog is None:
                observation += TOPICS.get(species, "")
        elif encounter.visible_species == profile["favorite_species"]:
            observation += "This is your favorite Pokemon. "
        if facts:
            observation += "Known: " + prompt_facts(facts) + " "
        allowed = encounter.allowed()
        action = allowed[0]
        first, second = dialogue_options(species, encounter, facts)
        grammar = "root ::= " + choices(first) + r' "\n" ' + choices(second)
        tail = " Speak in two short lines."
        if len(allowed) > 1:
            _, body = grammar.split(" ::= ", 1)
            grammar = r'root ::= ("A" | "B") "\n" body' + "\nbody ::= " + body
            tail = (
                f" Choose A for {allowed[0]} or B for {allowed[1]}. "
                "Choose A if it furthers a personal goal. A recurring visitor with your favorite "
                "is a good candidate for a pond survey. Write the letter, then two short lines."
            )
            if allowed[0] == "PROPOSE_OPTIONAL_QUEST":
                grammar = r'root ::= "A" | "B" "\n" body' + "\nbody ::= " + body
                tail += " If you offer a survey, write only A."
        prompt = chat(instructions, observation + tail)
        inference_start = perf_counter()
        result, metrics = self.worker.generate(grammar, prompt)
        if len(allowed) > 1:
            letter, _, text = result.partition("\n")
            if letter not in ("A", "B"):
                raise ValueError("Action choice outside grammar")
            action = allowed[letter == "B"]
        else:
            text = result
        if action == "PROPOSE_OPTIONAL_QUEST":
            if result != "A":
                raise ValueError("Quest choice must contain only its action")
            text = "Pikachu again, I see!\nShow me a new Pokemon."
        else:
            first_line, _, second_line = text.partition("\n")
            if first_line not in first or second_line not in second:
                raise ValueError("Generated dialogue is outside approved choices")
        raw = json.dumps({"action": "SAY_DIALOGUE", "text": text})
        validate(raw)
        return Proposal(raw, action, {
            **metrics,
            "retrieval_ms": round((retrieved - start) * 1000, 3),
            "context_ms": round((inference_start - retrieved) * 1000, 3),
            "planning_ms": round((perf_counter() - start) * 1000, 3),
        }, observation, tuple(fact.key for fact in facts))

    def propose(self, conversation):
        return self.plan(Encounter(conversation.npc, conversation.visible_species)).dialogue

    def close(self):
        self.worker.close()


class DialogueReplies:
    """Reuse proposals while the observed facts and world state match."""

    def __init__(self, executor, propose):
        self.executor = executor
        self.propose = propose
        self.pending = {}

    def prepare(self, context):
        reply = self.pending.get(context)
        if reply is None or (reply.done() and reply.exception() is not None):
            stale = [key for key in self.pending if key.npc == context.npc and key.visible_species == context.visible_species]
            for key in stale:
                self.pending.pop(key).cancel()
            reply = self.executor.submit(self.propose, context)
            self.pending[context] = reply
        return reply
