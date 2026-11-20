"""Minimal SDL2/libretro desktop player for the Living Quantum World test."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import ctypes as c
import ctypes.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

from bridge import Conversation, DialogueBridge, MAILBOX_SIZE, REPLY_OFFSET, TEXT_CAPACITY, validate
from inference import DialogueReplies, LocalModel, windows_launcher_environment
from profiles import PROFILES
from world import Encounter, WorldMemory

ROOT = Path(__file__).resolve().parent
VOID = c.c_void_p
UINT = c.c_uint
INT = c.c_int
KEYS = {8: 29, 0: 27, 2: 42, 3: 40, 4: 82, 5: 81, 6: 80, 7: 79, 10: 4, 11: 22}
PIXELS = {0: 0x15130F02, 1: 0x16161804, 2: 0x15151002}


class GameInfo(c.Structure):
    _fields_ = [("path", c.c_char_p), ("data", VOID), ("size", c.c_size_t), ("metadata", c.c_char_p)]


class AvInfo(c.Structure):
    _fields_ = [("base_width", UINT), ("base_height", UINT), ("max_width", UINT),
                ("max_height", UINT), ("aspect", c.c_float), ("fps", c.c_double),
                ("sample_rate", c.c_double)]


class AudioSpec(c.Structure):
    _fields_ = [("frequency", INT), ("format", c.c_uint16), ("channels", c.c_uint8),
                ("silence", c.c_uint8), ("samples", c.c_uint16), ("padding", c.c_uint16),
                ("size", UINT), ("callback", VOID), ("userdata", VOID)]


def bind(library, name, result, *arguments):
    fn = getattr(library, name)
    fn.restype, fn.argtypes = result, arguments
    return fn


class Display:
    def __init__(self):
        name = str(ROOT / "SDL2.dll") if sys.platform == "win32" else ctypes.util.find_library("SDL2-2.0")
        if not name:
            raise RuntimeError("SDL2 is unavailable")
        self.sdl = sdl = c.CDLL(name)
        if sdl.SDL_Init(0x20) != 0:
            raise RuntimeError("SDL could not start video")
        sdl.SDL_InitSubSystem(0x10)  # Audio is optional if the machine has no output.
        self.window = bind(sdl, "SDL_CreateWindow", VOID, c.c_char_p, INT, INT, INT, INT, UINT)(
            b"Living Quantum World", 0x2FFF0000, 0x2FFF0000, 720, 480, 0x20)
        self.renderer = bind(sdl, "SDL_CreateRenderer", VOID, VOID, INT, UINT)(self.window, -1, 0)
        if not self.window or not self.renderer:
            raise RuntimeError("SDL could not open the game window")
        bind(sdl, "SDL_RenderSetLogicalSize", INT, VOID, INT, INT)(self.renderer, 240, 160)
        self.create_texture = bind(sdl, "SDL_CreateTexture", VOID, VOID, UINT, INT, INT, INT)
        self.update_texture = bind(sdl, "SDL_UpdateTexture", INT, VOID, VOID, VOID, INT)
        self.copy = bind(sdl, "SDL_RenderCopy", INT, VOID, VOID, VOID, VOID)
        self.present = bind(sdl, "SDL_RenderPresent", None, VOID)
        self.clear = bind(sdl, "SDL_RenderClear", INT, VOID)
        self.title = bind(sdl, "SDL_SetWindowTitle", None, VOID, c.c_char_p)
        self.queue = bind(sdl, "SDL_QueueAudio", INT, UINT, VOID, UINT)
        self.queued = bind(sdl, "SDL_GetQueuedAudioSize", UINT, UINT)
        self.device = 0
        self.texture = None
        self.pixel = 0
        self.event = (c.c_uint64 * 8)()
        self.keyboard = bind(sdl, "SDL_GetKeyboardState", c.POINTER(c.c_uint8), VOID)(None)
        self.closed = False

    def open_audio(self, rate):
        request = AudioSpec(round(rate), 0x8010, 2, 0, 1024)
        self.device = bind(self.sdl, "SDL_OpenAudioDevice", UINT, c.c_char_p, INT, VOID, VOID, INT)(
            None, 0, c.byref(request), None, 0)
        if self.device:
            self.sdl.SDL_PauseAudioDevice(self.device, 0)

    def audio(self, samples, count):
        if self.device and self.queued(self.device) < 16000:
            self.queue(self.device, samples, count * 4)
        return count

    def draw(self, data, width, height, pitch):
        if not data or data == VOID(-1).value:
            return
        if not self.texture:
            self.texture = self.create_texture(self.renderer, PIXELS[self.pixel], 1, width, height)
            if not self.texture:
                return
        self.update_texture(self.texture, None, data, pitch)
        self.clear(self.renderer)
        self.copy(self.renderer, self.texture, None, None)
        self.present(self.renderer)

    def pump(self):
        while self.sdl.SDL_PollEvent(c.byref(self.event)):
            if self.event[0] & 0xFFFFFFFF == 0x100:
                self.closed = True
        return not self.closed

    def key(self, port, device, index, button):
        return self.keyboard[KEYS[button]] if port == 0 and button in KEYS else 0


class Game:
    def __init__(self, core_path, rom_path, rom, mailbox, display):
        self.display = display
        self.mailbox = mailbox
        self.core = core = c.CDLL(str(core_path))
        self.rom_buffer = c.create_string_buffer(rom)
        self.info = GameInfo(os.fsencode(rom_path), c.addressof(self.rom_buffer), len(rom), None)
        # Keep callback objects alive through retro_deinit.
        self.callbacks = []
        self.set_callback("environment", c.c_bool, (UINT, VOID), self.environment)
        self.set_callback("video_refresh", None, (VOID, UINT, UINT, c.c_size_t), display.draw)
        self.set_callback("audio_sample_batch", c.c_size_t, (VOID, c.c_size_t), display.audio)
        self.set_callback("audio_sample", None, (c.c_int16, c.c_int16), lambda left, right: None)
        self.set_callback("input_poll", None, (), lambda: None)
        self.set_callback("input_state", c.c_int16, (UINT, UINT, UINT, UINT), display.key)
        core.retro_init()
        if not bind(core, "retro_load_game", c.c_bool, VOID)(c.byref(self.info)):
            core.retro_deinit()
            raise RuntimeError("mGBA rejected the bundled ROM")
        self.memory = bind(core, "retro_get_memory_data", VOID, UINT)
        self.memory_size = bind(core, "retro_get_memory_size", c.c_size_t, UINT)
        ram = self.memory(2)
        if not ram or not 0x02000000 <= mailbox <= 0x02040000 - MAILBOX_SIZE:
            self.close()
            raise RuntimeError("mGBA mailbox is unavailable")
        self.mailbox_ptr = ram + mailbox - 0x02000000
        av = AvInfo()
        core.retro_get_system_av_info(c.byref(av))
        self.frame_period = 1 / av.fps
        display.open_audio(av.sample_rate)

    def set_callback(self, name, result, arguments, callback):
        prototype = c.CFUNCTYPE(result, *arguments)
        wrapped = prototype(callback)
        self.callbacks.append(wrapped)
        bind(self.core, f"retro_set_{name}", None, prototype)(wrapped)

    def environment(self, command, data):
        if command == 10:
            value = c.cast(data, c.POINTER(INT))[0]
            if value in PIXELS:
                self.display.pixel = value
                return True
        return False

    def read_request(self, address, size):
        if address != self.mailbox or size != REPLY_OFFSET:
            raise ValueError("Invalid mailbox read")
        return c.string_at(self.mailbox_ptr, size)

    def write_reply(self, address, data):
        offset = address - self.mailbox
        if not ((offset == REPLY_OFFSET and len(data) == 4)
                or (offset == REPLY_OFFSET + 4 and 1 < len(data) <= TEXT_CAPACITY + 1)):
            raise ValueError("Invalid mailbox write")
        c.memmove(self.mailbox_ptr + offset, data, len(data))

    def load_save(self, data):
        if len(data) != self.memory_size(0):
            raise ValueError("The battery save does not match the emulator's save size")
        c.memmove(self.memory(0), data, len(data))

    def save_bytes(self):
        return c.string_at(self.memory(0), self.memory_size(0))

    def close(self):
        self.core.retro_unload_game()
        self.core.retro_deinit()


def atomic_write(path, data):
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
        temp = Path(output.name)
        try:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
            output.close()
            os.replace(temp, path)
        finally:
            temp.unlink(missing_ok=True)


def verify_windows_sandbox(runtime):
    with tempfile.TemporaryDirectory() as directory:
        sentinel = Path(directory) / "user-data.txt"
        sentinel.write_text("protected", encoding="ascii")
        result = subprocess.run(
            [str(runtime / "sandbox.exe"), "--probe", str(sentinel)],
            cwd=runtime, env=windows_launcher_environment(), stdin=subprocess.DEVNULL,
            timeout=10, capture_output=True, text=True,
        )
        print(result.stdout.strip() or result.stderr.strip())
        return result.returncode != 0 or sentinel.read_text(encoding="ascii") != "protected"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--sandbox-test", action="store_true")
    mode.add_argument("--model-test", action="store_true")
    mode.add_argument("--pallet-test", action="store_true")
    args = parser.parse_args()
    runtime = ROOT / "inference"
    if args.sandbox_test:
        if sys.platform != "win32":
            raise RuntimeError("This command tests the Windows isolation backend")
        return int(verify_windows_sandbox(runtime))

    manifest = json.loads((ROOT / "rom.json").read_text(encoding="utf-8"))
    rom_path = ROOT / "PokemonQuantum.gba"
    rom = rom_path.read_bytes()
    if hashlib.sha256(rom).hexdigest() != manifest["sha256"]:
        raise RuntimeError("The bundled ROM and mailbox manifest do not match")
    model = LocalModel(runtime, manifest["species"], catalog=ROOT / "world-knowledge.sqlite3")
    if args.model_test:
        expected = {
            "pc_resident": "watts:pikachu",
            "oak": "evolution:PIKACHU",
            "blue": "battle:electric",
            "daisy": "care:pikachu",
        }
        try:
            for npc, fact in expected.items():
                proposal = model.plan(Encounter(npc, 25))
                if fact not in proposal.knowledge:
                    raise RuntimeError(f"Missing expected Pikachu fact for {npc}")
                print(PROFILES[npc]["name"], validate(proposal.dialogue).decode("ascii"), proposal.metrics)
        finally:
            model.close()
        return 0
    profile = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local/share")) / "LivingQuantumWorld"
    profile.mkdir(parents=True, exist_ok=True)
    save_path = profile / ("PalletTest.sav" if args.pallet_test else "PokemonQuantum.sav")
    core_path = ROOT / ("mgba_libretro.dll" if sys.platform == "win32" else "mgba_libretro.so")
    display = Display()
    game = Game(core_path, rom_path, rom, manifest["mailbox"], display)
    memory = None
    previous = None
    try:
        if save_path.is_file():
            game.load_save(save_path.read_bytes())
        elif args.pallet_test:
            game.load_save((ROOT / "PalletTest.sav").read_bytes())
        previous = game.save_bytes()
        memory = WorldMemory(profile / "living-world.sqlite3", save_path.name, previous,
                             unsaved=not args.pallet_test and not save_path.is_file())
        bridge = DialogueBridge(game.read_request, game.write_reply, game.mailbox)
        with ThreadPoolExecutor(max_workers=1) as pool, (profile / "dialogue.jsonl").open(
            "a", encoding="utf-8", buffering=1
        ) as log:
            replies = DialogueReplies(pool, model.plan)
            staged = None
            def prepare_demo():
                if args.pallet_test:
                    for species in (25, 7):
                        replies.prepare(memory.context(Conversation("pc_resident", species)))

            # Prepare likely replies while the title screen and field stay responsive.
            prepare_demo()

            def propose(context):
                nonlocal staged
                encounter = memory.context(context)
                work = replies.prepare(encounter)
                if not work.done():
                    display.title(display.window, b"Living Quantum World - NPC is thinking")
                try:
                    while not work.done():
                        if not display.pump():
                            raise RuntimeError("Window closed")
                        time.sleep(0.015)
                    proposal = work.result()
                    staged = (encounter, proposal)
                    if proposal.action not in encounter.allowed():
                        raise ValueError("Rejected action outside the encounter allowlist")
                    return proposal.dialogue
                finally:
                    display.title(display.window, b"Living Quantum World")

            next_save = time.monotonic() + 2
            while display.pump():
                start = time.monotonic()
                game.core.retro_run()
                staged = None
                trace = bridge.poll(propose)
                if trace:
                    trace["profile"] = PROFILES[trace["context"]["npc"]]
                    trace["fallback"] = trace["validation"] != "accepted"
                    if staged:
                        encounter, proposal = staged
                        trace.update(
                            context_sent=proposal.context_sent,
                            knowledge_facts=proposal.knowledge,
                            proposed_action=proposal.action,
                            metrics=proposal.metrics,
                            action_result="rejected",
                        )
                        if not trace["fallback"]:
                            try:
                                updates = memory.apply(encounter, proposal.action)
                                trace["changes"].extend(updates)
                                trace["action_result"] = "approved"
                                if updates:
                                    prepare_demo()
                            except ValueError as error:
                                trace["action_error"] = str(error)
                    trace["memory"] = memory.snapshot(trace["context"]["npc"])
                    trace["acquired_knowledge"] = memory.knowledge(
                        trace["context"]["npc"], trace["context"]["visible_species"]
                    )
                    log.write(json.dumps(trace) + "\n")
                if start >= next_save:
                    current = game.save_bytes()
                    if current != previous:
                        if save_path.exists():
                            atomic_write(save_path.with_suffix(".bak"), previous)
                        memory.checkpoint(current)
                        atomic_write(save_path, current)
                        previous = current
                    next_save = start + 2
                time.sleep(max(0, game.frame_period - (time.monotonic() - start)))
    finally:
        model.close()
        try:
            current = game.save_bytes()
            if memory is not None and current != previous:
                if save_path.exists():
                    atomic_write(save_path.with_suffix(".bak"), previous)
                memory.checkpoint(current)
                atomic_write(save_path, current)
        finally:
            if memory is not None:
                memory.close()
            game.close()
            display.sdl.SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
