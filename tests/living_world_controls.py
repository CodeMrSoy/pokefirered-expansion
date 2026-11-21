"""Exercise the desktop route with SDL virtual controllers and keyboard capture."""
import ctypes as c
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
from tempfile import TemporaryDirectory

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "experiments/living_world"))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from controls import BUTTONS, DEFAULT_KEYS, ESCAPE, F1, F2
from play import Display, Game, bind


def push_key(display, key, repeat=False):
    event = bytearray(56)
    struct.pack_into("=I", event, 0, 0x300)
    struct.pack_into("=i", event, 16, key)
    event[13] = int(repeat)
    push = bind(display.sdl, "SDL_PushEvent", c.c_int, c.c_void_p)
    assert push(c.create_string_buffer(bytes(event))) == 1
    assert display.pump()


class Descriptor(c.Structure):
    _fields_ = [("flags", c.c_uint64), ("ptr", c.c_void_p), ("offset", c.c_size_t),
                ("start", c.c_size_t), ("select", c.c_size_t), ("disconnect", c.c_size_t),
                ("length", c.c_size_t), ("address_space", c.c_char_p)]


class MemoryMap(c.Structure):
    _fields_ = [("descriptors", c.POINTER(Descriptor)), ("count", c.c_uint)]


class InputProbe(Game):
    def __init__(self, core, display):
        symbols = subprocess.check_output(
            [os.environ.get("ARM_NM", "arm-none-eabi-nm"), root / "pokefirered.elf"], text=True)
        addresses = {parts[2]: int(parts[0], 16) for line in symbols.splitlines()
                     if len(parts := line.split()) == 3}
        self.key_address = addresses["gMain"] + 0x28  # heldKeysRaw in include/main.h
        self.keys_ptr = None
        rom = root / "pokefirered.gba"
        super().__init__(Path(core), rom, rom.read_bytes(), addresses["gLivingWorldMailbox"], display)
        for _ in range(360):
            self.core.retro_run()
        assert self.keys_ptr

    def environment(self, command, data):
        if command & 0xFFFF == 36:  # RETRO_ENVIRONMENT_SET_MEMORY_MAPS
            maps = c.cast(data, c.POINTER(MemoryMap)).contents
            for desc in maps.descriptors[:maps.count]:
                if desc.ptr and desc.start <= self.key_address < desc.start + desc.length:
                    self.keys_ptr = desc.ptr + desc.offset + self.key_address - desc.start
            return True
        return super().environment(command, data)

    def check(self, mask):
        for _ in range(3):
            self.core.retro_run()
        assert c.c_uint16.from_address(self.keys_ptr).value == mask


def exercise(display, profile, game):
    controls = display.controls
    sdl = display.sdl
    bind(sdl, "SDL_SetHint", c.c_int, c.c_char_p, c.c_char_p)(
        b"SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS", b"1")
    controls.focus = lambda: display.window  # The dummy backend has no native window focus.
    controls.keyboard = (c.c_uint8 * controls.count.value)()
    assert not controls.controller
    attach = bind(sdl, "SDL_JoystickAttachVirtual", c.c_int, c.c_int, c.c_int, c.c_int, c.c_int)
    detach = bind(sdl, "SDL_JoystickDetachVirtual", c.c_int, c.c_int)
    joystick = bind(sdl, "SDL_GameControllerGetJoystick", c.c_void_p, c.c_void_p)
    press = bind(sdl, "SDL_JoystickSetVirtualButton", c.c_int, c.c_void_p, c.c_int, c.c_uint8)
    axis = bind(sdl, "SDL_JoystickSetVirtualAxis", c.c_int, c.c_void_p, c.c_int, c.c_int16)
    index = attach(1, 6, 21, 0)  # SDL_JOYSTICK_TYPE_GAMECONTROLLER
    assert index >= 0
    display.pump()
    assert controls.controller, "Hotplug should activate the gamepad"
    device = joystick(controls.controller)
    gba_masks = {"A": 1, "B": 2, "Select": 4, "Start": 8, "Right": 16, "Left": 32,
                 "Up": 64, "Down": 128, "R": 256, "L": 512}
    for label, (id_, _, key) in BUTTONS.items():
        assert press(device, key, 1) == 0
        display.pump()
        assert display.key(0, 1, 0, id_) and not display.key(1, 1, 0, id_)
        if game:
            game.check(gba_masks[label])
        assert press(device, key, 0) == 0
        display.pump()
        assert not display.key(0, 1, 0, id_)
        if game:
            game.check(0)
    for value, held in ((5000, False), (22000, True)):
        assert axis(device, 0, -value) == 0
        display.pump()
        assert bool(display.key(0, 1, 0, 6)) == held
    assert detach(index) == 0
    display.pump()
    assert not controls.controller and not display.key(0, 1, 0, 6)
    index = attach(1, 6, 21, 0)
    display.pump()
    assert controls.controller, "The gamepad should reconnect without a restart"

    controls.dialog = lambda *args: 1  # Choose Remap in the native modal.
    push_key(display, F1, repeat=True)
    assert controls.draft is None
    push_key(display, F1)
    for _ in range(4):
        push_key(display, F2)
    assert controls.step == 4
    push_key(display, DEFAULT_KEYS["B"])  # Using B's old key for A swaps the two.
    for _ in range(5):
        push_key(display, F2)
    assert controls.draft is None
    keys = json.loads(profile.read_text())
    assert keys["A"] == DEFAULT_KEYS["B"] and keys["B"] == DEFAULT_KEYS["A"]
    assert len(set(keys.values())) == len(BUTTONS)
    controls.keyboard[keys["A"]] = 1
    display.pump()
    assert display.key(0, 1, 0, 8) and not display.key(0, 1, 0, 0)
    if game:
        game.check(1)
    controls.focus = lambda: None
    display.pump()
    assert not controls.buttons
    controls.focus = lambda: display.window
    controls.keyboard[keys["A"]] = 0

    push_key(display, F1)
    push_key(display, 20)
    push_key(display, ESCAPE)
    assert controls.keys == keys and controls.load() == keys
    controls.dialog = lambda *args: 2
    push_key(display, F1)
    assert controls.load() == DEFAULT_KEYS
    profile.write_text('{"A": -1}')
    assert controls.load() == DEFAULT_KEYS

    # A controller connected before app initialization must be found too.
    controls.close()
    controls.refresh_controller()
    assert controls.controller
    assert detach(index) == 0
    display.pump()
    print("PASS SDL hotplug, all ten buttons, stick deadzone, reconnect, remap, persistence, focus and reset")


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        path = Path(directory) / "controls.json"
        display = Display(path)
        game = None
        try:
            core = os.environ.get("MGBA_CORE")
            game = InputProbe(core, display) if core else None
            exercise(display, path, game)
            if game:
                print("PASS all SDL controller buttons and the remapped keyboard key reached mGBA's GBA input")
        finally:
            if game:
                game.close()
            display.controls.close()
            display.sdl.SDL_Quit()
