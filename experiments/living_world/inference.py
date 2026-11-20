"""Offline llama.cpp client. Only the isolated worker receives the prompt."""
import json
import os
import re
from pathlib import Path
import subprocess
import sys

from bridge import validate

PROFILE = "You are the friendly neighbor by the Pallet Town pond who loves computers."
REACTIONS = {
    "Pikachu": (
        "Pikachu's cheeks can spark. You are protective of your computer wiring.",
        r'''root ::= "Pikachu, " ("mind my cables!" | "watch those sparks!" | "easy on the sparks!") "\n" ("My PC's had enough " ("shocks." | "trouble.") | "Stay clear of my PC." | "That would fry my PC.")''',
    ),
    "Squirtle": (
        "Squirtle is a little turtle with a shell. Invite it to swim in the pond.",
        r'''root ::= "Squirtle, " ("eyeing the pond?" | "fancy a swim?" | "ready for a dip?") "\n" ("That shell looks " ("sturdy." | "polished." | "spotless.") | "The pond's nice and cool.")''',
    ),
}


def dialogue_grammar(species):
    if species in REACTIONS:
        return REACTIONS[species][1]
    if species and re.fullmatch("[A-Za-z][A-Za-z0-9 .'-]{0,19}", species):
        ending = ' ("!" | ", hi there!")' if len(species) <= 17 else ' "!"'
        greeting = json.dumps(species) + ending
    else:
        greeting = '"Hello, trainer!"'
    return 'root ::= ' + greeting + r''' "\n" ("Your PC stores items." | "Try storing spare items." | "Try your PC for storage.")'''


def windows_launcher_environment():
    # Windows resolves the per-user AppContainer using LOCALAPPDATA when
    # CreateProcessW starts the worker. Pass only the required variables.
    required = ("SystemRoot", "LOCALAPPDATA")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError("Windows sandbox launcher needs " + ", ".join(missing))
    return {name: os.environ[name] for name in required}


class LocalModel:
    def __init__(self, runtime: Path, species_names: dict, timeout=8):
        self.runtime = runtime.resolve()
        self.species_names = species_names
        self.timeout = timeout

    def propose(self, context):
        species = self.species_names.get(str(context.visible_species))
        observation = f"You see {species}." if species else "No Pokemon is visible."
        if species in REACTIONS:
            observation += " " + REACTIONS[species][0]
        prompt = (
            f"<|im_start|>system\n{PROFILE} Reply with two short lines.<|im_end|>\n"
            f"<|im_start|>user\n{observation}<|im_end|>\n"
            "<|im_start|>assistant\n"
        )
        runtime = self.runtime
        model = runtime / "model.gguf"
        args = [str(model), dialogue_grammar(species), prompt]
        if sys.platform == "win32":
            command = [str(runtime / "sandbox.exe"), *args]
            env = windows_launcher_environment()
        elif sys.platform == "linux":
            command = [str(runtime / "offline-worker"), *args]
            env = {}
        else:
            raise RuntimeError("No inference isolation backend for this platform")
        # On Windows the launcher must keep Play.cmd's console for the
        # isolated console worker. Dialogue still travels through pipes.
        result = subprocess.run(
            command, cwd=runtime, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=self.timeout, check=False,
        )
        if result.returncode:
            reason = result.stderr.decode("utf-8", errors="replace").strip()[-240:]
            status = str(result.returncode)
            if sys.platform == "win32":
                status += f" (0x{result.returncode & 0xFFFFFFFF:08X})"
            raise RuntimeError(f"Offline worker exited {status}. {reason}")
        if sys.platform == "linux" and not result.stderr.startswith(b"LQW isolation active\n"):
            raise RuntimeError("Linux isolation did not initialize")
        # Windows text-mode stdout expands the worker's line break to CRLF.
        generated = result.stdout.decode("utf-8").replace("\r\n", "\n").strip()
        return json.dumps({"action": "SAY_DIALOGUE", "text": generated}, ensure_ascii=True)


class DialogueReplies:
    """Generate each context once per session and reuse its validated reply."""

    def __init__(self, executor, propose):
        self.executor = executor
        self.propose = propose
        self.pending = {}

    def prepare(self, context):
        reply = self.pending.get(context)
        if reply is None or (reply.done() and reply.exception() is not None):
            reply = self.executor.submit(self._generate, context)
            self.pending[context] = reply
        return reply

    def _generate(self, context):
        proposal = self.propose(context)
        validate(proposal)
        return proposal
