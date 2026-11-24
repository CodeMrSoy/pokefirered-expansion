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
RELEASE_VERSION = "19.0.0-ecology-preview"
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
    parser.add_argument("--test-report", type=Path, help="Attach a test report for this exact release")
    parser.add_argument("--nm", default="arm-none-eabi-nm")
    parser.add_argument("--built-mgba", action="store_true", help="Use the core built by build-ci-windows.sh")
    parser.add_argument("--legacy-weights", action="store_true", help="Bundle Phase 4 Qwen 2.5 weights")
    args = parser.parse_args()
    inputs = args.inputs
    model_sha = LIGHTWEIGHT_SHA256 if args.legacy_weights else BALANCED_SHA256
    input_hashes = {**INPUTS, "model-q4.gguf": model_sha}
    if args.built_mgba:
        del input_hashes["mgba-win.zip"]
    for filename, expected in input_hashes.items():
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
    regional_view = next(int(line.split()[0], 16) for line in symbols.splitlines()
                         if line.endswith(" gLivingWorldRegionalQuestView"))
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
        shutil.copyfile(inputs / "PewterSocietyTest.sav", stage / "PewterRegionalTest.sav")
        (stage / "Play Pewter Regional Demo.cmd").write_bytes(
            b'@echo off\r\ncall "%~dp0Play.cmd" --pewter-regional\r\n')
        shutil.copyfile(inputs / "PewterSocietyTest.sav", stage / "Phase11RegionalSociety.sav")
        shutil.copyfile(inputs / "Phase13Pewter.sav", stage / "Phase13Pewter.sav")
        (stage / "Play Phase 11 Society Demo.cmd").write_bytes(
            b'@echo off\r\ncall "%~dp0Play.cmd" --phase11-demo\r\n')
        (stage / "Play Pewter Regional Retest.cmd").write_bytes(
            b'@echo off\r\ncall "%~dp0Play.cmd" --pewter-regional-retest\r\n')
        validator = (APP / "validate-offline-windows.cmd").read_text(encoding="ascii")
        (stage / "Validate Offline Runtime.cmd").write_bytes(validator.replace("\n", "\r\n").encode("ascii"))
        for name in ("play.py", "controls.py", "platform_io.py", "platform_scenario.py", "kanto.py", "autonomy.py", "world_rules.py", "agency.py",
                     "package_smoke.py", "launcher-windows.ps1", "population.py", "bridge.py", "inference.py", "worker.py", "world.py", "profiles.py",
                     "knowledge.py", "social.py", "reasoning.py", "hybrid.py", "routines.py", "director.py", "society.py", "planning.py", "region.py", "dynamic_quests.py", "PLAYTEST.md",
                     "PHASE2.md", "PHASE3.md", "PHASE4.md", "PHASE5.md", "PHASE6.md", "PHASE7.md", "PHASE8.md", "PHASE9.md", "PHASE10.md", "PHASE11.md", "PHASE12.md", "PHASE13.md", "PHASE14.md", "PHASE15.md", "PLATFORM.md"):
            shutil.copyfile(APP / name, stage / name)
        for name in ("world_manifest.py", "native_world.py", "world_initialization.py", "live_world.py", "ecology.py",
                     "world-manifest-v1.schema.json", "simulate.py", "PHASE17.md", "PHASE18.md", "PHASE19.md"):
            shutil.copyfile(APP / name, stage / name)
        shutil.copytree(APP / "simulation", stage / "simulation", ignore=shutil.ignore_patterns("__pycache__"))
        (stage / "kanto").mkdir()
        shutil.copyfile(APP / "kanto" / "identities.json", stage / "kanto" / "identities.json")
        subprocess.run([sys.executable, APP / "build-world-catalog.py", ROOT / "pokefirered.gba",
                        ROOT / "pokefirered.elf", stage / "world-catalog.json", "--nm", args.nm,
                        "--revision", revision], check=True)
        subprocess.run([sys.executable, APP / "build-knowledge.py", stage / "world-knowledge.sqlite3"], check=True)
        shutil.copyfile(APP / "launch-windows.cmd", stage / "Play.cmd")
        launcher = (APP / "open-launcher-windows.cmd").read_text(encoding="ascii")
        (stage / "Open Pokemon Quantum.cmd").write_bytes(launcher.replace("\n", "\r\n").encode("ascii"))
        (stage / "Play Pallet Demo.cmd").write_bytes(b'@echo off\r\ncall "%~dp0Play.cmd" --pallet-test\r\n')
        (stage / "Play Pallet Social Demo.cmd").write_bytes(b'@echo off\r\ncall "%~dp0Play.cmd" --pallet-social\r\n')

        extract_flat(inputs / "python-win.zip", stage / "python")
        pth = stage / "python" / "python312._pth"
        pth.write_text(pth.read_text() + "\n..\n", encoding="ascii")
        if args.built_mgba:
            shutil.copyfile(inputs / "mgba_libretro.dll", stage / "mgba_libretro.dll")
        else:
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
            "regional_view": regional_view,
            "profile_version": 15,
            "sha256": sha256(stage / "PokemonQuantum.gba"),
            "model_sha256": model_sha,
            "species": names,
            "revision": revision,
        }
        (stage / "rom.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        release = {
            "version": RELEASE_VERSION, "commit": revision, "rom_sha256": manifest["sha256"],
            "dependencies": {
                "python": "3.12.10", "sdl": "2.32.10",
                "mgba": "7a12d6d4b9acb14c0ae62c9166b6a2f3d08007f6", "llama_cpp": "b6500",
                "model": "Qwen2.5-0.5B Q4_0" if args.legacy_weights else "Qwen3-0.6B Q4_K_M",
                "model_sha256": model_sha, "input_hashes": input_hashes,
                "mgba_origin": "source-build" if args.built_mgba else "pinned-archive",
            },
            "files": {file.relative_to(stage).as_posix(): sha256(file)
                      for file in sorted(stage.rglob("*")) if file.is_file()},
            "test_status": {"native_windows": "unverified"},
        }
        if args.test_report:
            evidence = json.loads(args.test_report.read_text(encoding="utf-8"))
            if evidence.get("commit") != revision:
                raise ValueError("Test report commit does not match the package")
            release["test_status"].update(evidence["test_status"])
            (stage / "TEST-RESULTS.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
            release["files"]["TEST-RESULTS.json"] = sha256(stage / "TEST-RESULTS.json")
        (stage / "release.json").write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
        with ZipFile(args.output, "w", ZIP_DEFLATED, compresslevel=1) as archive:
            for file in sorted(stage.rglob("*")):
                if file.is_file():
                    archive.write(file, file.relative_to(stage.parent))
    print(f"{args.output} ({args.output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
