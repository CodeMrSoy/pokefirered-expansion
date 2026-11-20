"""Build the offline Windows ZIP from a compiled ROM and staged, pinned inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[2]
APP = Path(__file__).resolve().parent
INPUTS = {
    "model-q4.gguf": "7671c0c304e6ce5a7fc577bcb12aba01e2c155cc2efd29b2213c95b18edaf6ed",
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
    args = parser.parse_args()
    inputs = args.inputs
    for filename, expected in INPUTS.items():
        if sha256(inputs / filename) != expected:
            raise ValueError(f"SHA-256 mismatch for {filename}")
    symbols = subprocess.check_output([args.nm, ROOT / "pokefirered.elf"], text=True)
    mailbox = next(int(line.split()[0], 16) for line in symbols.splitlines()
                   if line.endswith(" gLivingWorldMailbox"))
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
        for name in ("play.py", "bridge.py", "inference.py", "worker.py", "world.py", "PLAYTEST.md"):
            shutil.copyfile(APP / name, stage / name)
        shutil.copyfile(APP / "launch-windows.cmd", stage / "Play.cmd")
        (stage / "Play Pallet Demo.cmd").write_bytes(b'@echo off\r\ncall "%~dp0Play.cmd" --pallet-test\r\n')

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

        manifest = {
            "mailbox": mailbox,
            "sha256": sha256(stage / "PokemonQuantum.gba"),
            "model_sha256": INPUTS["model-q4.gguf"],
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
