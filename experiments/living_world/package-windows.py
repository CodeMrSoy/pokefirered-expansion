"""Build the offline Windows ZIP from a compiled ROM and staged, pinned inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

from reasoning import BALANCED_SHA256, LIGHTWEIGHT_SHA256

ROOT = Path(__file__).resolve().parents[2]
APP = Path(__file__).resolve().parent
INPUTS = {
    "mgba-win.zip": "a7ae453b739d3f9117537e8ca7275ecebd923d9035b52435f556470bf58a268f",
    "python-win.zip": "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3",
    "sdl-win.zip": "6cf9706eefd0a4a06dc764007934d428afaf029fabdd408a9e646048c91e18fb",
}


def sha256(path):
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def extract_flat(archive, target, allowed=None):
    with ZipFile(archive) as source:
        for entry in source.infolist():
            if not entry.is_dir() and (allowed is None or entry.filename in allowed):
                if Path(entry.filename).name != entry.filename or "\\" in entry.filename:
                    raise ValueError(f"Unexpected ZIP entry {entry.filename}")
                with source.open(entry) as original, (target / entry.filename).open("wb") as output:
                    shutil.copyfileobj(original, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--nm", default="arm-none-eabi-nm")
    parser.add_argument("--legacy-weights", action="store_true", help="Bundle Phase 4 Qwen 2.5 weights")
    args = parser.parse_args()
    inputs = args.inputs
    model_sha = LIGHTWEIGHT_SHA256 if args.legacy_weights else BALANCED_SHA256
    for filename, expected in {**INPUTS, "model-q4.gguf": model_sha}.items():
        if sha256(inputs / filename) != expected:
            raise ValueError(f"SHA-256 mismatch for {filename}")
    symbols = subprocess.check_output([args.nm, ROOT / "pokefirered.elf"], text=True)
    mailbox = next(int(line.split()[0], 16) for line in symbols.splitlines()
                   if line.endswith(" gLivingWorldMailbox"))
    field_hint = next(int(line.split()[0], 16) for line in symbols.splitlines()
                      if line.endswith(" gLivingWorldFieldHint"))
    brock_presence = next(int(line.split()[0], 16) for line in symbols.splitlines()
                          if line.endswith(" gLivingWorldBrockPresence"))
    trainer_presence = next(int(line.split()[0], 16) for line in symbols.splitlines()
                            if line.endswith(" gLivingWorldTrainerPresence"))
    quest_view = next(int(line.split()[0], 16) for line in symbols.splitlines()
                      if line.endswith(" gLivingWorldQuestView"))
    researcher_presence = next(int(line.split()[0], 16) for line in symbols.splitlines()
                               if line.endswith(" gLivingWorldResearcherPresence"))
    museum_view = next(int(line.split()[0], 16) for line in symbols.splitlines()
                       if line.endswith(" gLivingWorldMuseumQuestView"))
    names = {}
    header = (ROOT / "include/constants/species.h").read_text()
    for key, id_ in re.findall(r"^#define SPECIES_([A-Z0-9_]+)\s+(\d+)\b", header, re.MULTILINE):
        if key != "NONE":
            names.setdefault(id_, key.replace("_", " ").title())
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / "LivingQuantumWorld"
        stage.mkdir()
        licenses = stage / "licenses"
        licenses.mkdir()
        (stage / "inference").mkdir()
        (stage / "python").mkdir()
        shutil.copyfile(ROOT / "pokefirered.gba", stage / "PokemonQuantum.gba")
        shutil.copyfile(inputs / "PalletTest.sav", stage / "PalletTest.sav")
        shutil.copyfile(inputs / "PalletSocialTest.sav", stage / "PalletSocialTest.sav")
        shutil.copyfile(inputs / "PewterTest.sav", stage / "PewterTest.sav")
        shutil.copyfile(inputs / "PewterSocietyTest.sav", stage / "PewterSocietyTest.sav")
        (stage / "Play Pewter Society Demo.cmd").write_bytes(
            b'@echo off\r\ncall "%~dp0Play.cmd" --pewter-society\r\n')
        for name in ("play.py", "bridge.py", "inference.py", "worker.py", "world.py", "profiles.py",
                     "knowledge.py", "social.py", "reasoning.py", "hybrid.py", "routines.py", "director.py", "society.py", "planning.py", "region.py", "dynamic_quests.py", "PLAYTEST.md",
                     "PHASE2.md", "PHASE3.md", "PHASE4.md", "PHASE5.md", "PHASE6.md", "PHASE7.md", "PHASE8.md", "PHASE9.md"):
            shutil.copyfile(APP / name, stage / name)
        subprocess.run([sys.executable, APP / "build-knowledge.py", stage / "world-knowledge.sqlite3"], check=True)
        shutil.copyfile(APP / "launch-windows.cmd", stage / "Play.cmd")
        (stage / "Play Pallet Demo.cmd").write_bytes(b'@echo off\r\ncall "%~dp0Play.cmd" --pallet-test\r\n')
        (stage / "Play Pallet Social Demo.cmd").write_bytes(b'@echo off\r\ncall "%~dp0Play.cmd" --pallet-social\r\n')

        extract_flat(inputs / "python-win.zip", stage / "python")
        pth = stage / "python" / "python312._pth"
        pth.write_text(pth.read_text() + "\n..\n", encoding="ascii")
        extract_flat(inputs / "mgba-win.zip", stage, {"mgba_libretro.dll"})
        extract_flat(inputs / "sdl-win.zip", stage, {"SDL2.dll"})

        for exe in ("sandbox.exe", "sandbox-probe.exe", "offline-worker.exe"):
            shutil.copyfile(inputs / exe, stage / "inference" / exe)
        shutil.copyfile(inputs / "model-q4.gguf", stage / "inference" / "model.gguf")
        for license_file in sorted((inputs / "licenses").glob("*-LICENSE.txt")):
            shutil.copyfile(license_file, licenses / license_file.name)
        for name in ("Qwen", "SDL", "llama.cpp", "mGBA"):
            if not (licenses / (name + "-LICENSE.txt")).is_file():
                raise ValueError(f"Missing license for {name}")

        (stage / "Play Pewter World Demo.cmd").write_bytes(
            b'@echo off\r\ncall "%~dp0Play.cmd" --pewter-demo\r\n')
        manifest = {
            "mailbox": mailbox,
            "field_hint": field_hint,
            "brock_presence": brock_presence,
            "trainer_presence": trainer_presence,
            "researcher_presence": researcher_presence,
            "quest_view": quest_view,
            "museum_view": museum_view,
            "sha256": sha256(stage / "PokemonQuantum.gba"),
            "model_sha256": model_sha,
            "species": names,
            "revision": revision,
        }
        (stage / "rom.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        with ZipFile(args.output, "w", ZIP_DEFLATED, compresslevel=1) as archive:
            for file in sorted(stage.rglob("*")):
                if file.is_file():
                    archive.write(file, file.relative_to(stage.parent))
    print(f"{args.output} ({args.output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
