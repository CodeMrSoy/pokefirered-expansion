"""Exercise the extracted distribution with its own runtime and emulator."""

import ctypes as c
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from play import Display, Game, bind
from bridge import Conversation, DialogueBridge, REPLY_OFFSET, SKIP, validate
from controls import BUTTONS, F2
from hybrid import HybridDialogue, prepare
from inference import LocalModel
from platform_io import atomic_write
from platform_scenario import scenario
from world import WorldMemory
from concurrent.futures import ThreadPoolExecutor


def check_files(root):
    manifest = json.loads((root / "release.json").read_text(encoding="utf-8"))
    for name, digest in manifest["files"].items():
        with (root / name).open("rb") as file:
            if hashlib.file_digest(file, "sha256").hexdigest() != digest:
                raise AssertionError(f"Package hash mismatch: {name}")
    return manifest


def run_frames(game, count, button=None):
    game.display.controls.buttons = {button} if button is not None else set()
    for _ in range(count):
        game.core.retro_run()


def key_check(display):
    controls = display.controls
    controls.draft = dict(controls.keys)
    controls.advance(controls.keys["Down"])
    for _ in range(len(BUTTONS) - 1):
        controls.advance(F2)
    assert controls.load() == controls.keys
    sdl = display.sdl
    bind(sdl, "SDL_SetHint", c.c_int, c.c_char_p, c.c_char_p)(b"SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS", b"1")
    attach = bind(sdl, "SDL_JoystickAttachVirtual", c.c_int, c.c_int, c.c_int, c.c_int, c.c_int)
    detach = bind(sdl, "SDL_JoystickDetachVirtual", c.c_int, c.c_int)
    index = attach(1, 6, 21, 0)
    assert index >= 0
    try:
        display.pump()
        assert controls.controller
    finally:
        assert detach(index) == 0
        display.pump()
    assert not controls.controller


def runtime_smoke(directory, core):
    rom = ROOT / "PokemonQuantum.gba"
    manifest = json.loads((ROOT / "rom.json").read_text(encoding="utf-8"))
    keys = ("field_hint", "brock_presence", "trainer_presence", "quest_view",
            "researcher_presence", "museum_view", "regional_view")
    rom_bytes = rom.read_bytes()
    assert hashlib.sha256(rom_bytes).hexdigest() == manifest["sha256"]

    def open_game():
        return Game(core, rom, rom_bytes, manifest["mailbox"], display,
                    **{key: manifest[key] for key in keys})

    display = Display(directory / "controls.json")
    try:
        key_check(display)
        game = open_game()
        try:
            fixture = (ROOT / "Phase11RegionalSociety.sav").read_bytes()
            game.load_save(fixture)
            run_frames(game, 180)
            for _ in range(10):
                for key in (3, 8):
                    run_frames(game, 2, key)
                    run_frames(game, 40)
                hint = game.read_hint()
                if hint and hint.area == "pewter" and not hint.busy:
                    break
            else:
                raise AssertionError("Packaged ROM failed to enter the Pewter field")
            assert display.texture and display.device
            assert game.save_bytes() == fixture
            target = directory / "Phase11RegionalSociety.sav"
            atomic_write(target, game.save_bytes())

            # Keep all writes inside the authorized host response window.
            bridge = DialogueBridge(game.read_request, game.write_reply, game.mailbox, deferred=True)
            assert bridge.poll(lambda _: SKIP) is None
            try:
                game.write_reply(game.mailbox + REPLY_OFFSET - 1, b"\0")
            except ValueError:
                pass
            else:
                raise AssertionError("Arbitrary mailbox write was accepted")
            game.publish_researcher(hint.frame, "museum")
            with TemporaryDirectory() as world_directory:
                scenario(Path(world_directory))
            memory = WorldMemory(directory / "test.sqlite3", target.name, fixture)
            try:
                game.publish_quest(memory.director, memory.society, memory.population)
            finally:
                memory.close()
        finally:
            game.close()
        game = open_game()
        try:
            game.load_save(target.read_bytes())
            assert game.save_bytes() == fixture
        finally:
            game.close()
    finally:
        display.controls.close()
        display.sdl.SDL_Quit()
    return "SDL video/audio, virtual controller, remap, ROM hint and bounded mailbox, battery write/reload, SQLite quest lifecycle"


def worker_failure_smoke():
    # The exact packaged launcher gets a nonexistent model. No external files
    # are touched. The host must still serve a valid authored fallback.
    model = LocalModel(ROOT / "inference", {"25": "Pikachu"},
                       catalog=ROOT / "world-knowledge.sqlite3", style="qwen3")
    model.worker.model = model.worker.runtime / "missing-model-for-smoke.gguf"
    world = WorldMemory(":memory:", "worker-failure", b"fixture")
    try:
        visitor = Conversation("pc_resident", 25)
        world.apply(world.context(visitor), "ADJUST_RELATIONSHIP")
        with ThreadPoolExecutor(max_workers=1) as pool:
            router = HybridDialogue(world, model, pool)
            request = router.request(visitor)
            try:
                request.future.result(timeout=45)
            except (RuntimeError, OSError):
                fallback, route = prepare(model, request.key.state, fallback=True)
                assert route == "fallback" and validate(fallback.dialogue)
                assert model.worker.process is None
            else:
                raise AssertionError("Missing model did not exercise worker failure")
    finally:
        model.close()
        world.close()


def validate_worker(report):
    for flag in ("--sandbox-test", "--model-test"):
        result = subprocess.run([sys.executable, "-B", "play.py", flag], cwd=ROOT,
                                capture_output=True, text=True, timeout=160)
        report[flag[2:]] = {"exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        if result.returncode:
            raise RuntimeError(f"{flag} failed")


def main():
    report_path = Path(sys.argv[1]).resolve()
    report = {"platform": sys.platform, "checks": {}, "native_windows": "unverified"}
    try:
        report["commit"] = check_files(ROOT)["commit"]
        report["checks"]["integrity"] = "passed"
        if sys.platform != "win32":
            raise RuntimeError("The bundled Windows executables require a Windows runner")
        with TemporaryDirectory() as directory:
            report["checks"]["host"] = runtime_smoke(Path(directory), ROOT / "mgba_libretro.dll")
        validate_worker(report)
        worker_failure_smoke()
        report["checks"]["worker_failure"] = "passed"
        report["native_windows"] = "passed"
    except Exception as error:
        report["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
