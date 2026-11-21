"""Minimal SDL2/libretro desktop player for the Living Quantum World test."""
import argparse
from concurrent.futures import Future, ThreadPoolExecutor
import ctypes as c
import ctypes.util
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import time

from bridge import (
    Conversation, DialogueBridge, MAILBOX_SIZE, REPLY_OFFSET, SKIP, TEXT_CAPACITY, WAIT, validate,
)
from controls import Controls
from director import DUTY, PRESENCE, TRIP, choose_brock
from dynamic_quests import (QUEST_VIEW, museum_exchange, project_brock, project_museum,
                            project_regional, regional_exchange)
from inference import LocalModel, windows_launcher_environment
from hybrid import FIELD_SIZE, FieldHint, HybridDialogue, prepare
from reasoning import BALANCED_SHA256, LIGHTWEIGHT_SHA256, GuideTurn, guide_reply, reported_fact
from profiles import PROFILES
from world import Encounter, WorldMemory
from society import PERSONAS, Ticket
from region import RESEARCHER_PRESENCE, TRAINER_PRESENCE
from planning import Proposal, choose_plan
from population import choose_commitment

ROOT = Path(__file__).resolve().parent
VOID = c.c_void_p
UINT = c.c_uint
INT = c.c_int
BROCK_PRESENCE = struct.Struct("<4sHBB")
BROCK_REQUESTS = frozenset(("brock_attendant", "brock_contact", "brock_return"))
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
    def __init__(self, controls_path=None):
        name = str(ROOT / "SDL2.dll") if sys.platform == "win32" else ctypes.util.find_library("SDL2-2.0")
        if not name:
            raise RuntimeError("SDL2 is unavailable")
        self.sdl = sdl = c.CDLL(name)
        if sdl.SDL_Init(0x20) != 0:
            raise RuntimeError("SDL could not start video")
        sdl.SDL_InitSubSystem(0x10)  # Audio is optional if the machine has no output.
        self.window = bind(sdl, "SDL_CreateWindow", VOID, c.c_char_p, INT, INT, INT, INT, UINT)(
            b"Living Quantum World - F1 Controls", 0x2FFF0000, 0x2FFF0000, 720, 480, 0x20)
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
        self.pause_device = bind(sdl, "SDL_PauseAudioDevice", None, UINT, INT)
        self.clear_audio = bind(sdl, "SDL_ClearQueuedAudio", None, UINT)
        self.device = 0
        self.audio_started = False
        self.texture = None
        self.pixel = 0
        self.event = (c.c_uint64 * 8)()
        self.controls = Controls(sdl, bind, self.window, controls_path or ROOT / "controls.json",
                                 atomic_write, lambda title: self.title(self.window, title))
        self.closed = False

    def open_audio(self, rate):
        request = AudioSpec(round(rate), 0x8010, 2, 0, 2048)
        obtained = AudioSpec()
        self.device = bind(self.sdl, "SDL_OpenAudioDevice", UINT, c.c_char_p, INT, VOID, VOID, INT)(
            None, 0, c.byref(request), c.byref(obtained), 0)
        self.audio_block = obtained.samples * 4  # Signed 16-bit stereo.

    def pause_audio(self):
        if self.device and (self.audio_started or self.queued(self.device)):
            self.pause_device(self.device, 1)
            self.clear_audio(self.device)
            self.audio_started = False

    def audio_queue_blocks(self):
        return self.queued(self.device) / self.audio_block if self.device else 0

    def audio(self, samples, count):
        if self.device:
            buffered = self.queued(self.device)
            if self.audio_started and not buffered:
                self.pause_device(self.device, 1)
                self.audio_started = False
            if self.queue(self.device, samples, count * 4) == 0:
                if not self.audio_started and buffered + count * 4 >= self.audio_block * 3:
                    self.pause_device(self.device, 0)
                    self.audio_started = True
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
            kind = self.event[0] & 0xFFFFFFFF
            if kind == 0x100:
                self.closed = True
            elif kind == 0x300:
                # SDL_KeyboardEvent: repeat at byte 13, SDL_Keysym at byte 16.
                event = bytes(self.event)
                if not event[13]:
                    self.controls.event(kind, struct.unpack_from("=i", event, 16)[0])
            else:
                self.controls.event(kind)
        if not self.closed:
            self.controls.snapshot()
        return not self.closed

    def key(self, port, device, index, button):
        return int(port == 0 and device == 1 and index == 0 and button in self.controls.buttons)


class Game:
    def __init__(self, core_path, rom_path, rom, mailbox, display, *, field_hint=None, brock_presence=None, trainer_presence=None, quest_view=None, researcher_presence=None, museum_view=None, regional_view=None):
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
                0x02000000 <= field_hint <= 0x02040000 - FIELD_SIZE
                or not (field_hint + FIELD_SIZE <= mailbox or mailbox + MAILBOX_SIZE <= field_hint)):
            self.close()
            raise RuntimeError("Invalid field hint location")
        self.hint_ptr = None if field_hint is None else ram + field_hint - 0x02000000
        ranges = [(mailbox, MAILBOX_SIZE), (field_hint, FIELD_SIZE)]
        for name, address, size in (("brock_ptr", brock_presence, BROCK_PRESENCE.size),
                                    ("trainer_ptr", trainer_presence, BROCK_PRESENCE.size),
                                    ("researcher_ptr", researcher_presence, BROCK_PRESENCE.size),
                                    ("quest_ptr", quest_view, QUEST_VIEW.size), ("museum_ptr", museum_view, QUEST_VIEW.size),
                                    ("regional_ptr", regional_view, QUEST_VIEW.size)):
            if address is not None and (
                    address % 4 or not 0x02000000 <= address <= 0x02040000 - size
                    or any(start is not None and address < start + length and start < address + size
                           for start, length in ranges)):
                self.close()
                raise RuntimeError(f"Invalid position projection: {name}")
            setattr(self, name, None if address is None else ram + address - 0x02000000)
            ranges.append((address, size))
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
        return FieldHint.decode(c.string_at(self.hint_ptr, FIELD_SIZE)) if self.hint_ptr else None

    def publish_brock(self, frame, location):
        if self.brock_ptr is not None:
            code = PRESENCE[location]
            data = BROCK_PRESENCE.pack(b"LWB1", frame, code, code ^ 255)
            c.memmove(self.brock_ptr, data, BROCK_PRESENCE.size)

    def publish_trainer(self, frame, location):
        if self.trainer_ptr is not None:
            code = TRAINER_PRESENCE[location]
            data = BROCK_PRESENCE.pack(b"LWS1", frame, code, code ^ 255)
            c.memmove(self.trainer_ptr, data, BROCK_PRESENCE.size)

    def publish_researcher(self, frame, location):
        if self.researcher_ptr is not None:
            code = RESEARCHER_PRESENCE[location]
            payload = BROCK_PRESENCE.pack(b"LWR1", frame, code, code ^ 255)
            c.memmove(self.researcher_ptr, payload, len(payload))

    def publish_quest(self, director, society, population=None):
        if self.quest_ptr is not None:
            c.memmove(self.quest_ptr, project_brock(director), QUEST_VIEW.size)
        if self.museum_ptr is not None:
            c.memmove(self.museum_ptr, project_museum(society), QUEST_VIEW.size)
        if self.regional_ptr is not None:
            c.memmove(self.regional_ptr, project_regional(population), QUEST_VIEW.size)

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
    mode.add_argument("--pewter-demo", action="store_true")
    mode.add_argument("--pewter-society", action="store_true")
    mode.add_argument("--pewter-regional", action="store_true")
    mode.add_argument("--phase11-demo", action="store_true")
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
            if model.style == "qwen3":
                society = smoke_memory.society
                society.regional_demo = True
                society.tick(39600, "pewter")
                ticket = society.decision("researcher")
                plan, metrics = choose_plan(model, ticket, society.primitives(ticket),
                                            PERSONAS[ticket.actor], society.planning_snapshot())
                society.submit(ticket, plan)
                print("Regional:", plan.goal, [(step.action, step.target) for step in plan.steps], metrics)
        finally:
            smoke_memory.close()
            model.close()
        return 0
    profile_name = "LivingQuantumWorldPhase11" if args.phase11_demo or manifest.get("profile_version") == 11 else "LivingQuantumWorld"
    profile = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local/share")) / profile_name
    profile.mkdir(parents=True, exist_ok=True)
    demo = "PalletSocialTest.sav" if args.pallet_social else "PalletTest.sav" if args.pallet_test else None
    if args.phase11_demo:
        demo = "Phase11RegionalSociety.sav"
    elif args.pewter_regional:
        demo = "PewterRegionalTest.sav"
    elif args.pewter_society:
        demo = "PewterSocietyTest.sav"
    elif args.pewter_demo:
        demo = "PewterTest.sav"
    save_path = profile / (demo or "PokemonQuantum.sav")
    core_path = ROOT / ("mgba_libretro.dll" if sys.platform == "win32" else "mgba_libretro.so")
    display = Display(profile / "controls.json")
    game = Game(core_path, rom_path, rom, manifest["mailbox"], display,
                field_hint=manifest.get("field_hint"), brock_presence=manifest.get("brock_presence"),
                trainer_presence=manifest.get("trainer_presence"), quest_view=manifest.get("quest_view"),
                researcher_presence=manifest.get("researcher_presence"), museum_view=manifest.get("museum_view"),
                regional_view=manifest.get("regional_view"))
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
            title = b"Living Quantum World - F1 Controls"
            next_prediction = 0.0
            previous_hint_frame = None
            prediction_error = None

            society = memory.society
            population = memory.population if args.phase11_demo else None
            if population:
                population.model_decisions = model.style == "qwen3"
            resident_work = None
            society.demo = args.pewter_society or args.pewter_regional or args.phase11_demo
            society.regional_demo = args.pewter_regional or args.phase11_demo
            director = memory.director
            director.demo = args.pewter_demo
            director.society_demo = society.demo
            director.notice_required = True
            planning = None
            plan_retry_after = 0.0
            plan_budget = {}
            plan_cache = {}

            def run_decision(chooser, request, queued, available=None, planner=None):
                delay = (time.perf_counter() - queued) * 1000
                if available is None:
                    plan, metrics = chooser(model, request)
                else:
                    plan, metrics = chooser(model, request, available, PERSONAS[request.actor], planner)
                return plan, {**metrics, "queue_ms": delay}

            def run_commitment(ticket, queued):
                wait = (time.perf_counter() - queued) * 1000
                choice, metrics = choose_commitment(model, ticket)
                return choice, {**metrics, "queue_ms": wait}

            def propose(context):
                nonlocal staged, scene, lookup, guide_turn, guide_work, guide_result, last_guide
                if context.npc in ("society_assistant", "society_trainer", "society_researcher"):
                    actor = context.npc.removeprefix("society_")
                    message = (regional_exchange(population, actor) if population else None)
                    message = message or museum_exchange(society, actor) or society.message(actor)
                    return json.dumps({"action": "SAY_DIALOGUE", "text": message}) if message else SKIP
                if context.npc in BROCK_REQUESTS:
                    message = director.message(context.npc)
                    return json.dumps({"action": "SAY_DIALOGUE", "text": message}) if message else SKIP
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

            next_frame = time.monotonic()
            next_save = next_frame + 2
            while True:
                remaining = next_frame - time.monotonic()
                if remaining > 0:
                    time.sleep(remaining)
                if not display.pump():
                    break
                if display.controls.draft is not None:
                    title = None  # Restore the game title when keyboard capture ends.
                    display.pause_audio()
                    time.sleep(game.frame_period)
                    next_frame = time.monotonic()
                    continue
                queued_blocks = display.audio_queue_blocks()
                if queued_blocks >= 5:
                    # Drain excess audio before running another GBA frame.
                    time.sleep(game.frame_period / 4)
                    next_frame = time.monotonic()
                    continue
                start = time.monotonic()
                # Carry small scheduling overruns into the next frame. Reset after
                # a long stall to avoid fast-forwarding through stale input.
                if start - next_frame > game.frame_period * 3:
                    next_frame = start
                # Correct small differences between the device clock and frame
                # clock before the next audio callback runs out of samples.
                pace = 0.98 if display.audio_started and queued_blocks < 2 else 1
                next_frame += game.frame_period * pace
                game.core.retro_run()
                staged = None
                scene = None
                guide_result = None
                trace = bridge.poll(propose)
                next_title = b"Living Quantum World - NPC is thinking" if bridge.pending else b"Living Quantum World - F1 Controls"
                if next_title != title:
                    display.title(display.window, next_title)
                    title = next_title
                if trace and trace["context"]["npc"] in ("society_assistant", "society_trainer", "society_researcher"):
                    if trace["validation"] == "accepted":
                        actor = trace["context"]["npc"].removeprefix("society_")
                        if not population or not regional_exchange(population, actor, accepted=True):
                            museum_exchange(society, actor, accepted=True)
                    trace["route"] = "attributed_society_memory"
                    log.write(json.dumps(trace) + "\n")
                    trace = None
                if trace and trace["context"]["npc"] in BROCK_REQUESTS:
                    if trace["validation"] == "accepted":
                        director.message(trace["context"]["npc"], accepted=True)
                    if trace["context"]["npc"] in ("brock_attendant", "brock_return"):
                        director.challenger()
                    trace["route"] = "world_director"
                    trace["objective"] = director.state["quest"]
                    log.write(json.dumps(trace) + "\n")
                    trace = None
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
                            activity=lookup.key.state.activity,
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
                        if event["status"] == "shared":
                            memory.routines.discovery_pending = True
                        event["simulation_ms"] = (time.perf_counter() - simulation_start) * 1000
                        log.write(json.dumps({"social": event}) + "\n")
                if not bridge.pending and start >= next_prediction:
                    hint = game.read_hint()
                    try:
                        fresh = hint if hint and hint.frame != previous_hint_frame else None
                        if fresh:
                            for change in memory.routines.tick(fresh.local_second):
                                log.write(json.dumps({"world_event": change}) + "\n")
                            protected = bool(fresh.story) if fresh.area in ("", "pewter", "pewter_gym", "route_2") else False
                            director.observe(fresh.local_second, fresh.area, protected, fresh.busy)
                            society.tick(fresh.local_second, fresh.area, fresh.busy)
                            if population:
                                transitions = population.demo_tick(fresh.local_second)
                                if transitions:
                                    log.write(json.dumps({"regional_transitions": transitions,
                                                          "residents": len(population.state["actors"]),
                                                          "regional_clock": population.state["clock"],
                                                          "area": fresh.area}) + "\n")
                                if resident_work:
                                    ticket, future = resident_work
                                    if future.done():
                                        resident_work = None
                                        if population.decision(ticket.request) == ticket:
                                            try:
                                                choice, metrics = future.result()
                                            except (OSError, ValueError, RuntimeError, TimeoutError) as error:
                                                choice, metrics = "HELP", {"fallback": str(error)[:220]}
                                            population.submit(ticket, choice)
                                            log.write(json.dumps({"regional_commitment": ticket.request,
                                                                  "resident": ticket.actor, "choice": choice,
                                                                  "ready_wait_seconds": population.state["clock"] - ticket.ready,
                                                                  **metrics}) + "\n")
                                    elif population.decision(ticket.request) != ticket and future.cancel():
                                        resident_work = None
                                if (not resident_work and not planning and not fresh.busy
                                        and replies.worker_idle() and (ticket := population.decision())):
                                    resident_work = ticket, pool.submit(run_commitment, ticket, time.perf_counter())
                            director.notice = society.notice_for_brock()
                            director.offscreen = society.state["visited"] and not director.demo
                            society.reconcile_brock(director.state.get("last_notice_result"))
                            if planning is not None:
                                request, future = planning
                                social_plan = isinstance(request, Ticket)
                                ready_now = society.decision(request.actor) if social_plan else director.decision()
                                authority = society if social_plan else director
                                if future.done():
                                    planning = None
                                    metrics = {}
                                    failure = None
                                    try:
                                        selected, metrics = future.result()
                                    except (OSError, ValueError, RuntimeError, TimeoutError) as error:
                                        selected = request.choices[0] if social_plan else DUTY
                                        failure = str(error)[:220]
                                    try:
                                        try:
                                            authority.submit(request, selected, fallback=failure)
                                        except ValueError as error:
                                            if not isinstance(selected, Proposal) or request != ready_now:
                                                raise
                                            selected, failure = request.choices[0], str(error)
                                            authority.submit(request, selected, fallback=failure)
                                        if isinstance(selected, Proposal) and request.cause == "open_shift":
                                            key = (request.save, request.actor, request.context, selected.available)
                                            plan_cache[key] = selected
                                            if len(plan_cache) > 16:
                                                del plan_cache[next(iter(plan_cache))]
                                        if not social_plan:
                                            society.respond_brock(request.notice, selected == TRIP)
                                        steps = selected.steps if isinstance(selected, Proposal) else selected
                                        directive = [step.action for step in steps] if social_plan else selected.goal
                                        log.write(json.dumps({"directive": directive,
                                                              "actor": request.actor if social_plan else "brock",
                                                              "cause": request.cause if social_plan else request.trigger,
                                                              "metrics": metrics, "fallback": failure}) + "\n")
                                    except ValueError as error:
                                        log.write(json.dumps({"director_rejection": str(error)}) + "\n")
                                elif request != ready_now and future.cancel():
                                    planning = None
                            if not resident_work and planning is None and start >= plan_retry_after and game.brock_ptr:
                                request = (society.decision() if society.demo and not director.notice
                                           else director.decision()) or society.decision()
                                if request is not None and replies.worker_idle():
                                    social_plan = isinstance(request, Ticket)
                                    key = ((request.save, request.actor, request.window, request.cause) if social_plan else
                                           (request.checkpoint, "brock", request.number))
                                    attempts = plan_budget.get(key, 0)
                                    if attempts < 2:
                                        plan_budget[key] = attempts + 1
                                        if len(plan_budget) > 24:
                                            del plan_budget[next(iter(plan_budget))]
                                        plan_retry_after = start + 5
                                        chooser = choose_plan if social_plan else choose_brock
                                        available = society.primitives(request) if social_plan else None
                                        cache_key = (request.save, request.actor, request.context, available) if available else None
                                        cached = plan_cache.get(cache_key) if social_plan and request.cause == "open_shift" else None
                                        if cached:
                                            future = Future()
                                            future.set_result((cached, {"cache_hit": True, "queue_ms": 0}))
                                        else:
                                            future = pool.submit(run_decision, chooser, request, time.perf_counter(), available,
                                                                 society.planning_snapshot() if social_plan else None)
                                        planning = request, future
                                    else:
                                        authority = society if social_plan else director
                                        fallback_plan = request.choices[0] if social_plan else DUTY
                                        authority.submit(request, fallback_plan, fallback="decision retry limit")
                                        log.write(json.dumps({"directive": "routine",
                                                              "fallback": "decision retry limit"}) + "\n")
                            game.publish_quest(director, society, population)
                            game.publish_brock(fresh.frame, director.location)
                            game.publish_trainer(fresh.frame, society.state["agents"]["trainer"]["location"])
                            game.publish_researcher(fresh.frame, society.state["agents"]["researcher"]["location"])
                        predicted = None if args.no_predict or planning or resident_work else replies.predict(fresh, start)
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
                        game.publish_quest(director, society, population)
                        atomic_write(save_path, current)
                        previous = current
                    next_save = start + 2
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
            display.controls.close()
            display.sdl.SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
