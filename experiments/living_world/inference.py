"""Watts's local dialogue and action proposals."""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from time import perf_counter

from bridge import validate
from worker import ResidentWorker
from world import Encounter, PROFILE

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


def dialogue_grammar(species, encounter):
    if encounter.completes_quest:
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
    return "root ::= " + choices(first) + r' "\n" ' + choices(second)


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


class LocalModel:
    def __init__(self, runtime: Path, species_names: dict, timeout=8):
        self.species_names = species_names
        self.worker = ResidentWorker(runtime, windows_launcher_environment, timeout)

    def plan(self, encounter):
        species = self.species_names.get(str(encounter.visible_species))
        instructions = (
            f"You are {PROFILE['name']}, a {PROFILE['role']}. "
            f"You are {', '.join(PROFILE['traits'])}. {PROFILE['primary_goal']} "
            f"{PROFILE['secondary_motivation']} Keep to experiences you witnessed."
        )
        observation = f"Visible Pokemon: {species or 'none'}. "
        if encounter.remembered:
            observation += "You remember meeting this Pokemon. "
        observation += f"Trust: {encounter.trust}. Survey: {encounter.quest}. "
        observation += TOPICS.get(species, "")
        allowed = encounter.allowed()
        action = allowed[0]
        start = perf_counter()
        grammar = dialogue_grammar(species, encounter)
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
        result, metrics = self.worker.generate(grammar, chat(instructions, observation + tail))
        if len(allowed) > 1:
            letter, _, text = result.partition("\n")
            if letter not in ("A", "B"):
                raise ValueError("Action choice outside grammar")
            action = allowed[letter == "B"]
        else:
            text = result
        if action == "PROPOSE_OPTIONAL_QUEST":
            text = "Pikachu again, I see!\nShow me a new Pokemon."
        raw = json.dumps({"action": "SAY_DIALOGUE", "text": text})
        validate(raw)
        return Proposal(raw, action, {
            **metrics,
            "planning_ms": round((perf_counter() - start) * 1000, 3),
        }, observation)

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
            stale = [key for key in self.pending if key.visible_species == context.visible_species]
            for key in stale:
                self.pending.pop(key).cancel()
            reply = self.executor.submit(self.propose, context)
            self.pending[context] = reply
        return reply
