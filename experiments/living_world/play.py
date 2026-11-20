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

from bridge import (
    Conversation, DialogueBridge, MAILBOX_SIZE, REPLY_OFFSET, SKIP, TEXT_CAPACITY, WAIT, validate,
)
from inference import LocalModel, windows_launcher_environment
from hybrid import FIELD_HINT, FieldHint, HybridDialogue, prepare
from reasoning import BALANCED_SHA256, LIGHTWEIGHT_SHA256, GuideTurn, guide_reply, reported_fact
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
    def __init__(self, core_path, rom_path, rom, mailbox, display, *, field_hint=None):
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
        if field_hint is not None and (field_hint % 4 or not
                0x02000000 <= field_hint <= 0x02040000 - FIELD_HINT.size
                or not (field_hint + FIELD_HINT.size <= mailbox or mailbox + MAILBOX_SIZE <= field_hint)):
            self.close()
            raise RuntimeError("Invalid field hint location")
        self.hint_ptr = None if field_hint is None else ram + field_hint - 0x02000000
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

    def read_hint(self):
        return FieldHint.decode(c.string_at(self.hint_ptr, FIELD_HINT.size)) if self.hint_ptr else None

    def write_reply(self, address, data):
        offset = address - self.mailbox
        if not ((offset == REPLY_OFFSET and len(data) == 4)
                or (offset == REPLY_OFFSET + 4
                    and (data in (b"\0", b"\xff") or 1 < len(data) <= TEXT_CAPACITY + 1))):
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
    mode.add_argument("--pallet-social", action="store_true")
    parser.add_argument("--lightweight", action="store_true", help="Use short dialogue and skip optional prose")
    parser.add_argument("--no-predict", action="store_true", help="Disable approach prefetch for comparison")
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
    try:
        with (runtime / "model.gguf").open("rb") as weights:
            digest = hashlib.file_digest(weights, "sha256").hexdigest()
    except OSError:
        digest = None
    style = {BALANCED_SHA256: "qwen3", LIGHTWEIGHT_SHA256: "chatml"}.get(digest, "unavailable")
    model = LocalModel(runtime, manifest["species"], catalog=ROOT / "world-knowledge.sqlite3",
                       style=style, natural=style == "qwen3" and not args.lightweight)
    if args.model_test:
        expected = {
            "pc_resident": "watts:pikachu",
            "oak": "evolution:PIKACHU",
            "blue": "battle:electric",
            "daisy": "care:pikachu",
        }
        smoke_memory = WorldMemory(":memory:", "smoke", b"")
        try:
            with ThreadPoolExecutor(max_workers=1) as pool:
                router = HybridDialogue(smoke_memory, model, pool)
                for npc, fact in expected.items():
                    lookup = router.request(Conversation(npc, 25))
                    proposal, route = lookup.future.result()
                    if fact not in proposal.knowledge:
                        raise RuntimeError(f"Missing expected Pikachu fact for {npc}")
                    print(PROFILES[npc]["name"], validate(proposal.dialogue).decode("ascii"), route)
            if model.style == "unavailable":
                raise RuntimeError("Packaged local model is missing or has an unknown checksum")
            action, metrics, _ = model.survey(Encounter("pc_resident", 25, remembered=True, trust=1))
            print("Watts survey", action, metrics)
            reply = model.guide(GuideTurn("pallet-sighting:25", True))
            print("Guide follow-up", validate(reply.dialogue).decode("ascii"), reply.intention, reply.metrics)
        finally:
            smoke_memory.close()
            model.close()
        return 0
    profile = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local/share")) / "LivingQuantumWorld"
    profile.mkdir(parents=True, exist_ok=True)
    demo = "PalletSocialTest.sav" if args.pallet_social else "PalletTest.sav" if args.pallet_test else None
    save_path = profile / (demo or "PokemonQuantum.sav")
    core_path = ROOT / ("mgba_libretro.dll" if sys.platform == "win32" else "mgba_libretro.so")
    display = Display()
    game = Game(core_path, rom_path, rom, manifest["mailbox"], display,
                field_hint=manifest.get("field_hint"))
    memory = None
    previous = None
    try:
        if save_path.is_file():
            game.load_save(save_path.read_bytes())
        elif demo:
            game.load_save((ROOT / demo).read_bytes())
        previous = game.save_bytes()
        memory = WorldMemory(profile / "living-world.sqlite3", save_path.name, previous,
                             unsaved=not demo and not save_path.is_file())
        bridge = DialogueBridge(game.read_request, game.write_reply, game.mailbox, deferred=True)
        with ThreadPoolExecutor(max_workers=1) as pool, (profile / "dialogue.jsonl").open(
            "a", encoding="utf-8", buffering=1
        ) as log:
            replies = HybridDialogue(memory, model, pool)
            staged = None
            scene = None
            lookup = None
            last_guide = None
            guide_turn = None
            guide_work = None
            guide_result = None
            title = b"Living Quantum World"
            next_prediction = 0.0
            previous_hint_frame = None
            prediction_error = None

            def propose(context):
                nonlocal staged, scene, lookup, guide_turn, guide_work, guide_result, last_guide
                if context.npc == "pallet_exchange":
                    last_guide = None
                    scene = memory.social.scene()
                    return scene[1] if scene else SKIP
                if context.npc == "guide_followup":
                    if bridge.pending is None:
                        if last_guide is None or last_guide[0] != bridge.sequence or time.monotonic() > last_guide[2]:
                            return SKIP
                        guide_turn = memory.social.guide_turn(last_guide[1])
                        last_guide = None
                        guide_work = None
                        if guide_turn.can_request and model.natural:
                            replies.prioritize_followup()
                            guide_work = pool.submit(model.guide, guide_turn)
                    if guide_work is None:
                        guide_result = guide_reply(guide_turn)
                        return guide_result.dialogue
                    if not guide_work.done():
                        return WAIT
                    try:
                        guide_result = guide_work.result()
                    except (ValueError, RuntimeError, TimeoutError, OSError) as error:
                        guide_result = guide_reply(guide_turn, metrics={"fallback_error": str(error)[:240]})
                    return guide_result.dialogue
                if bridge.pending is None:
                    last_guide = None
                    lookup = replies.request(context, game.read_hint())
                if not lookup.future.done():
                    return WAIT
                checking = time.perf_counter()
                if lookup.key != replies.key(context, game.read_hint()):
                    raise ValueError("Dialogue context changed before delivery")
                try:
                    proposal, route = lookup.future.result()
                except (ValueError, RuntimeError, TimeoutError, OSError) as error:
                    proposal, route = prepare(model, lookup.key.state, fallback=True)
                    proposal.metrics["fallback_error"] = str(error)[:240]
                if proposal.action not in lookup.key.state.intentions:
                    raise ValueError("Rejected action outside the encounter allowlist")
                staged = (lookup, proposal, route, (time.perf_counter() - checking) * 1000)
                return proposal.dialogue

            next_save = time.monotonic() + 2
            while display.pump():
                start = time.monotonic()
                game.core.retro_run()
                staged = None
                scene = None
                guide_result = None
                trace = bridge.poll(propose)
                next_title = b"Living Quantum World - NPC is thinking" if bridge.pending else b"Living Quantum World"
                if next_title != title:
                    display.title(display.window, next_title)
                    title = next_title
                if trace and trace["context"]["npc"] == "pallet_exchange":
                    if scene and trace["validation"] == "accepted":
                        memory.social.displayed(scene[0])
                        trace["event"] = scene[0]
                    trace["route"] = "scheduled_exchange"
                    log.write(json.dumps(trace) + "\n")
                    trace = None
                if trace and trace["context"]["npc"] == "guide_followup":
                    if guide_result and trace["validation"] == "accepted":
                        trace.update(intention=guide_result.intention, report=guide_turn.fact,
                                     generated_reaction=guide_result.generated_reaction, metrics=guide_result.metrics)
                        trace["route"] = ("model_followup" if "inference_ms" in guide_result.metrics
                                          else "retrieved_followup")
                        try:
                            if memory.social.apply_guide_turn(guide_turn, guide_result.intention):
                                trace["changes"].append("guide_requested_verification")
                        except ValueError as error:
                            trace["action_error"] = str(error)
                    log.write(json.dumps(trace) + "\n")
                    trace = None
                if trace:
                    trace["profile"] = PROFILES[trace["context"]["npc"]]
                    trace["fallback"] = trace["validation"] != "accepted"
                    trace["route"] = "stock_fallback"
                    if staged:
                        lookup, proposal, route, check_ms = staged
                        encounter = lookup.key.state.encounter
                        trace.update(
                            context_sent=proposal.context_sent,
                            knowledge_facts=proposal.knowledge,
                            proposed_action=proposal.action,
                            metrics=proposal.metrics,
                            route=route,
                            cache=lookup.cache,
                            state_ms=lookup.state_ms,
                            cache_lookup_ms=lookup.lookup_ms,
                            context_validation_ms=check_ms,
                            topic=lookup.key.state.topic,
                            action_result="rejected",
                        )
                        if not trace["fallback"]:
                            try:
                                updates = memory.apply(encounter, proposal.action)
                                trace["changes"].extend(updates)
                                trace["action_result"] = "approved"
                                if encounter.npc == "sign_guide":
                                    sequence = (trace["sequence"] + 1) & 0xFFFFFFFF or 1
                                    last_guide = (sequence, reported_fact(proposal.dialogue, proposal.knowledge),
                                                  time.monotonic() + 90)
                            except ValueError as error:
                                trace["action_error"] = str(error)
                    trace["memory"] = memory.snapshot(trace["context"]["npc"])
                    trace["acquired_knowledge"] = memory.knowledge(
                        trace["context"]["npc"], trace["context"]["visible_species"]
                    )
                    log.write(json.dumps(trace) + "\n")
                if not bridge.pending and memory.social.deadline is not None:
                    simulation_start = time.perf_counter()
                    event = memory.social.tick(time.time())
                    if event:
                        event["simulation_ms"] = (time.perf_counter() - simulation_start) * 1000
                        log.write(json.dumps({"social": event}) + "\n")
                if not args.no_predict and not bridge.pending and start >= next_prediction:
                    hint = game.read_hint()
                    try:
                        predicted = replies.predict(hint if hint and hint.frame != previous_hint_frame else None,
                                                    start)
                        if predicted:
                            log.write(json.dumps({"prefetched": predicted.state.encounter.npc,
                                                  "species": predicted.state.encounter.visible_species,
                                                  "topic": predicted.state.topic}) + "\n")
                        prediction_error = None
                    except (ValueError, RuntimeError, OSError) as error:
                        if str(error) != prediction_error:
                            prediction_error = str(error)
                            log.write(json.dumps({"prediction_error": prediction_error}) + "\n")
                    previous_hint_frame = hint.frame if hint else None
                    next_prediction = start + 0.10
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
