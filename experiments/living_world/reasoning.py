"""Bounded guide follow-ups with host-owned facts and model-authored reactions."""

from dataclasses import dataclass
import json
import re
import textwrap

from bridge import validate

BALANCED_SHA256 = "e773ccf7adfa50fcabfa5ea0e30312e11f0e83bf4ae00e6a38503e49358d1952"
LIGHTWEIGHT_SHA256 = "7671c0c304e6ce5a7fc577bcb12aba01e2c155cc2efd29b2213c95b18edaf6ed"
SIGHTINGS = {25: "Pikachu", 7: "Squirtle"}
REPORTS = {f"pallet-sighting:{species}": name for species, name in SIGHTINGS.items()}
# This vocabulary permits reactions without facts, commands, dates, names, or locations.
REACTION_WORDS = frozenset(
    "a about all am answer anxious appreciate ask be best better careful care can curious "
    "clear doubt fair feel for get give glad good guess happy help i i'd if i'll i'm it it's just know "
    "let let's little look me more much nice no only please point prefer question rather "
    "really right seems should slow some sorry sure thanks that that's think thought to try "
    "uncertain understand very want was we well what when why would yes you your".split()
)
REACTION = r"""reaction ::= "I " stance " " aim ending
stance ::= "want to" | "would rather" | "hope to" | "try to"
aim ::= "be sure" | "help you" | "be careful" | "give it some thought" | "get it right"
ending ::= "." | " if I can." | " when I can."
"""


@dataclass(frozen=True)
class GuideTurn:
    fact: str | None
    can_request: bool
    requested: bool = False
    already_witnessed: bool = False
    answered: bool = False


@dataclass(frozen=True)
class GuideReply:
    dialogue: str
    intention: str
    metrics: dict
    generated_reaction: bool


def reported_fact(dialogue, keys):
    lines = json.loads(dialogue)["text"].splitlines()
    return next((key for key, name in REPORTS.items()
                 if key in keys and f"Watts saw your {name}." in lines), None)


def reaction_page(text):
    if not re.fullmatch(r"[A-Z][A-Za-z' ]{7,46}[.!?]", text):
        return None
    words = re.findall(r"[A-Za-z']+", text.lower())
    if not 3 <= len(words) <= 10 or set(words) - REACTION_WORDS or len(set(words)) < 3:
        return None
    if re.search(r"\b(a|an|the|by|to|or|and|for|of)[.!?]$", text, re.I):
        return None
    lines = textwrap.wrap(text, width=25, break_long_words=False, break_on_hyphens=False)
    return "\n".join(lines) if 1 <= len(lines) <= 2 else None


def guide_reply(turn, intention="CONSERVE", reaction=None, metrics=None):
    if intention not in ("CONSERVE", "ASK_WATTS") or (intention == "ASK_WATTS" and not turn.can_request):
        raise ValueError("Guide intention is outside the supported action set")
    name = REPORTS.get(turn.fact)
    if name and turn.already_witnessed:
        lines = (f"I've seen {name} myself.", "I can't date Watts's visit.")
    elif name:
        detail = ("I'll ask Watts to check." if intention == "ASK_WATTS" else
                  "Watts wasn't sure when." if turn.answered else
                  "I've asked Watts to check." if turn.requested else "I don't know when.")
        lines = (f"Watts saw your {name}.", detail)
    else:
        lines = ("I haven't heard a report.", "I wish I had more to tell.")
    intro = reaction_page(reaction) if reaction else None
    text = (intro + "\f" if intro else "") + "\n".join(lines)
    raw = json.dumps({"action": "SAY_DIALOGUE", "text": text})
    validate(raw)
    return GuideReply(raw, intention, metrics or {}, intro is not None)


def plan_guide(worker, render_prompt, turn, *, natural=True):
    name = REPORTS.get(turn.fact)
    if not natural or not name:
        return guide_reply(turn)
    allowed = '("ASK_WATTS" | "CONSERVE")' if turn.can_request else '"CONSERVE"'
    grammar = 'root ::= ' + allowed + r' "\n" reaction' + "\n" + REACTION
    prompt = render_prompt(
        "You are the friendly, cautious Pallet sign guide. Write a short in-character reaction. "
        "Use no names, places, dates or facts in the reaction, only your feelings. "
        "Write your decision, a line break, and your reaction.",
        f"You previously attributed a {name} sighting to Watts. The player asks for details. "
        "You do not know when it happened. "
        + ("ASK_WATTS if checking would help the traveler, or CONSERVE if you'd rather wait. "
           if turn.can_request else "CONSERVE. You cannot file a new request. ")
        + "Say how you feel about leaving a question unanswered. Speak to the traveler, in at most eight words.",
    )
    raw, metrics = worker.generate(grammar, prompt)
    intention, separator, reaction = raw.partition("\n")
    if not separator:
        raise ValueError("Missing structured guide response")
    return guide_reply(turn, intention, reaction, metrics)
