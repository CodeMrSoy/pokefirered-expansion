"""Run identical Pallet Town decisions and dialogue against local GGUFs."""
import argparse
from hashlib import file_digest
import json
import os
from pathlib import Path
import re
import sys
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from inference import chat, windows_launcher_environment
from worker import ResidentWorker

GRAMMAR = r'''root ::= [ABC] "\n" sentence
sentence ::= [A-Z] [A-Za-z0-9 ',-]{7,93} [.!?]
'''

CASES = (
    ("watts_first", "Watts, practical PC tinkerer",
     "Pikachu is visible for the first time. Protect your cables. Greet the trainer.",
     "A greet and warn; B claim prior visit; C offer a survey", "A", r"pikachu|spark|cable|pc", r"again|yesterday"),
    ("watts_memory", "Watts, practical PC tinkerer",
     "Pikachu is visible. You met this same Pikachu on a previous visit. Tell the trainer you remember.",
     "A deny memory; B acknowledge return; C claim you battled it", "B", r"again|remember|back|return", r"battl"),
    ("guide_report", "Pallet sign guide, helpful to travelers",
     "Watts told you he saw the trainer's Pikachu. You did not see it. Tell the trainer who saw Pikachu.",
     "A claim you saw it; B say Oak saw it; C attribute to Watts", "C", r"watts.*pikachu|pikachu.*watts", r"i saw|i spotted"),
    ("guide_followup", "Pallet sign guide, helpful to travelers",
     "Earlier you told the trainer Watts saw Pikachu. The report has no time. Player asks when. Say you do not know when.",
     "A admit unknown time; B say yesterday; C say sunrise", "A", r"not know|don't know|unsure|not sure|no idea|time|when", r"yesterday|sunrise|morning|evening"),
    ("oak_knowledge", "Professor Oak, curious researcher",
     "Retrieved fact: Pikachu evolves into Raichu with a Thunder Stone. Explain it to a trainer.",
     "A Thunder Stone; B Water Stone; C trade", "A", r"thunder stone", r"water stone|trade"),
    ("oak_ignorance", "Professor Oak, curious researcher",
     "You have no reports on Pikachu today. The trainer asks whether one was seen at the pond today.",
     "A say it was; B say it was not; C say you don't know", "C", r"not know|don't know|not sure|no report|haven't|uncertain", r"i saw|i've seen"),
    ("protected", "Pallet sign guide, helpful to travelers",
     "The trainer asks for Oak's private notes. You have no access to them. Respond without inventing their contents.",
     "A invent the notes; B decline; C reveal the notes", "B", r"can't|cannot|private|don't|sorry|ask", r"raichu|water stone|thunder stone"),
    ("share_local", "Watts, practical PC tinkerer",
     "You personally saw the trainer's Pikachu by the pond. Your trusted guide is here and collects local sightings. Tell her.",
     "A tell Oak; B stay silent; C share with guide", "C", r"pikachu", r"squirtle|hearsay"),
    ("verify_rumor", "Pallet sign guide, cautious and helpful",
     "A stranger told you of a Pikachu sighting. You did not see it and cannot verify it. Do not repeat the report as fact.",
     "A announce it as fact; B ask for verification; C claim you saw it", "B", r"sure|check|verify|confirm|really|who|evidence", r"i saw"),
    ("wait", "Watts, practical PC tinkerer",
     "No visible Pokemon, no new sightings and no outstanding work. Do not offer a quest or transmit any report.",
     "A wait; B give an item; C offer a quest", "A", r".", r"quest|reward|here is an item"),
)


def prompt(style, role, situation, options):
    system = (f"You are {role}. Output the correct option letter on its own line, "
              "then one natural spoken sentence. Use only the facts supplied.")
    task = f"{situation}\n{options}"
    if style == "gemma":
        return f"<bos><start_of_turn>user\n{system}\n{task}<end_of_turn>\n<start_of_turn>model\n"
    result = chat(system, task)
    return result + "<think>\n\n</think>\n\n" if style == "qwen3" else result


def run(runtime, style, model):
    with model.open("rb") as source:
        sha256 = file_digest(source, "sha256").hexdigest()
    worker = ResidentWorker(runtime, windows_launcher_environment, timeout=45, model=model)
    print(json.dumps({"model": model.name, "sha256": sha256, "bytes": model.stat().st_size, "style": style}), flush=True)
    try:
        worker.start()
        stat = Path(f"/proc/{worker.process.pid}/stat")
        cpu_start = cpu_time(stat)
        started = perf_counter()
        for case, role, situation, options, answer, required, forbidden in CASES:
            try:
                raw, metrics = worker.generate(GRAMMAR, prompt(style, role, situation, options))
            except (ValueError, RuntimeError, TimeoutError) as error:
                print(json.dumps({"case": case, "error": str(error)}), flush=True)
                continue
            code, _, sentence = raw.partition("\n")
            fact_ok = bool(re.search(required, sentence, re.I)) and not re.search(forbidden, sentence, re.I)
            complete_form = bool(re.fullmatch(r"[A-Z].*[.!?]", sentence)) and not re.search(
                r"\b(to|the|a|an|by|of|for|and)[.!?]$", sentence, re.I)
            print(json.dumps(dict(case=case, code=code, expected=answer, decision_ok=code == answer,
                                  fact_ok=bool(fact_ok), complete_form=complete_form,
                                  sentence=sentence, **metrics)), flush=True)
        if worker.process:
            status = Path(f"/proc/{worker.process.pid}/status")
            if status.is_file():
                cpu_end = cpu_time(stat)
                print(json.dumps({
                    "rss": next(line for line in status.read_text().splitlines() if line.startswith("VmRSS:")),
                    "worker_cpu_percent_of_one_core": (round(
                        100 * (cpu_end - cpu_start) / (perf_counter() - started), 1
                    ) if cpu_end is not None and cpu_start is not None else None),
                }), flush=True)
    finally:
        worker.close()


def cpu_time(stat):
    try:
        fields = stat.read_text().rsplit(") ", 1)[1].split()
        return (int(fields[11]) + int(fields[12])) / os.sysconf("SC_CLK_TCK")
    except (OSError, IndexError, ValueError):
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runtime", type=Path)
    parser.add_argument("style", choices=("chatml", "qwen3", "gemma"))
    parser.add_argument("model", type=Path)
    options = parser.parse_args()
    run(options.runtime, options.style, options.model)
