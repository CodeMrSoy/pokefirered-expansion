"""Offline llama.cpp client. Only the isolated worker receives the prompt."""
import json
import os
import re
from pathlib import Path
import subprocess
import sys

PC_LINE = r"""tip ::= "Your PC " ("can " | "keeps " | "holds " | "stores ") [a-z] [A-Za-z0-9 -]{2,11} "."
"""
PROFILE = (
    "You are a friendly Pallet Town resident. You teach Pokemon trainers to use a PC. "
    "Speak directly to the trainer. First greet them or their visible Pokemon, then give "
    "one brief, concrete storage tip beginning with 'Your PC'."
)
EXAMPLE = (
    "<|im_start|>user\nNo Pokemon is visible.<|im_end|>\n"
    "<|im_start|>assistant\nHello, trainer!\nYour PC stores items.<|im_end|>\n"
)


def dialogue_grammar(species):
    if species and re.fullmatch("[A-Za-z][A-Za-z0-9 .'-]{0,19}", species):
        greeting = json.dumps(species) + ' ", " ("good " | "nice " | "hey ") '
        greeting += "[a-z] [A-Za-z0-9 '-]{0," + str(19 - len(species)) + "} [.!?]"
    else:
        greeting = '''"Hello" [A-Za-z0-9 ,'-]{0,22} [.!?]'''
    return 'root ::= ' + greeting + r' "\n" tip' + "\n" + PC_LINE


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
        prompt = (
            f"<|im_start|>system\n{PROFILE}<|im_end|>\n"
            f"{EXAMPLE}"
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
