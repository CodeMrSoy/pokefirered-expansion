"""SDL keyboard bindings and hot-pluggable controller input for one GBA player."""
import ctypes as c
import json


# libretro joypad button IDs, SDL scancodes, and SDL controller button IDs.
BUTTONS = {
    "Up": (4, 82, 11), "Down": (5, 81, 12), "Left": (6, 80, 13), "Right": (7, 79, 14),
    "A": (8, 29, 0), "B": (0, 27, 1), "L": (10, 4, 9), "R": (11, 22, 10),
    "Start": (3, 40, 6), "Select": (2, 42, 4),
}
F1, F2, ESCAPE = 58, 59, 41
RESERVED = {F1, F2, ESCAPE}
AXIS_DEADZONE = 14000
DEFAULT_KEYS = {label: spec[1] for label, spec in BUTTONS.items()}


class MessageButton(c.Structure):
    _fields_ = [("flags", c.c_uint32), ("id", c.c_int), ("text", c.c_char_p)]


class MessageBox(c.Structure):
    _fields_ = [("flags", c.c_uint32), ("window", c.c_void_p), ("title", c.c_char_p),
                ("message", c.c_char_p), ("count", c.c_int),
                ("buttons", c.POINTER(MessageButton)), ("colors", c.c_void_p)]


class Controls:
    def __init__(self, sdl, bind, window, path, write, set_title):
        self.sdl, self.window, self.path, self.write, self.set_title = sdl, window, path, write, set_title
        self.buttons, self.controller = set(), None
        self.draft, self.step = None, 0
        self.pending_menu = False
        self.blocked = False
        self.release_key = None
        self.count = c.c_int()
        self.keyboard = bind(sdl, "SDL_GetKeyboardState", c.POINTER(c.c_uint8), c.POINTER(c.c_int))(
            c.byref(self.count))
        self.key_name = bind(sdl, "SDL_GetScancodeName", c.c_char_p, c.c_int)
        self.focus = bind(sdl, "SDL_GetKeyboardFocus", c.c_void_p)
        self.show = bind(sdl, "SDL_ShowMessageBox", c.c_int, c.POINTER(MessageBox), c.POINTER(c.c_int))
        self.keys = self.load()
        self.enabled = sdl.SDL_InitSubSystem(0x2000) == 0  # SDL_INIT_GAMECONTROLLER
        if self.enabled:
            self.device_count = bind(sdl, "SDL_NumJoysticks", c.c_int)
            self.is_controller = bind(sdl, "SDL_IsGameController", c.c_int, c.c_int)
            self.open_controller = bind(sdl, "SDL_GameControllerOpen", c.c_void_p, c.c_int)
            self.close_controller = bind(sdl, "SDL_GameControllerClose", None, c.c_void_p)
            self.attached = bind(sdl, "SDL_GameControllerGetAttached", c.c_int, c.c_void_p)
            self.get_button = bind(sdl, "SDL_GameControllerGetButton", c.c_uint8, c.c_void_p, c.c_int)
            self.get_axis = bind(sdl, "SDL_GameControllerGetAxis", c.c_int16, c.c_void_p, c.c_int)
            self.refresh_controller()

    def valid_key(self, key):
        return type(key) is int and 0 < key < self.count.value and key not in RESERVED and bool(self.key_name(key))

    def load(self):
        try:
            keys = json.loads(self.path.read_text(encoding="utf-8"))
            if (isinstance(keys, dict) and keys.keys() == DEFAULT_KEYS.keys()
                    and all(self.valid_key(key) for key in keys.values())
                    and len(set(keys.values())) == len(keys)):
                return keys
        except (OSError, ValueError):
            pass
        return DEFAULT_KEYS.copy()

    def close(self):
        if self.controller:
            self.close_controller(self.controller)
            self.controller = None

    def refresh_controller(self):
        if not self.enabled or (self.controller and self.attached(self.controller)):
            return
        self.close()
        for index in range(self.device_count()):
            if self.is_controller(index):
                self.controller = self.open_controller(index)
                if self.controller:
                    break

    def dialog(self, title, message, choices):
        buttons = (MessageButton * len(choices))(*(MessageButton(flags, id_, label) for flags, id_, label in choices))
        selection = c.c_int(-1)
        box = MessageBox(0x40, self.window, title, message, len(buttons), buttons, None)
        if self.show(c.byref(box), c.byref(selection)) != 0:
            return None
        return selection.value

    def save(self, keys):
        try:
            self.write(self.path, (json.dumps(keys, indent=2) + "\n").encode())
        except OSError:
            self.dialog(b"Controls", b"Could not save the keyboard settings.", [(3, 0, b"OK")])
            return
        self.keys = keys

    def prompt(self):
        label = tuple(BUTTONS)[self.step]
        self.set_title(f"Bind {label} ({self.step + 1}/{len(BUTTONS)}) | F2 keep | Esc cancel".encode())

    def advance(self, key):
        if key == ESCAPE:
            self.draft = None
        elif key == F2 or self.valid_key(key):
            if key != F2:
                label = tuple(BUTTONS)[self.step]
                current = self.draft[label]
                conflict = next((name for name, value in self.draft.items() if value == key), None)
                if conflict:
                    self.draft[conflict] = current
                self.draft[label] = key
            self.step += 1
            if self.step == len(BUTTONS):
                self.save(self.draft)
                self.draft = None
            else:
                self.prompt()
        if self.draft is None:
            self.release_key = key
            self.set_title(b"Living Quantum World - F1 Controls")

    def event(self, kind, key=None):
        if kind in (0x653, 0x654):  # Controller device added or removed
            self.refresh_controller()
        elif kind == 0x300 and self.draft is not None:
            self.advance(key)
        elif kind == 0x300 and key == F1:
            self.pending_menu = True

    def snapshot(self):
        self.buttons.clear()
        if self.pending_menu:
            self.pending_menu = False
            bindings = b"\n".join(label.encode() + b"  " + self.key_name(self.keys[label]) for label in BUTTONS)
            choice = self.dialog(
                b"Living Quantum World Controls",
                b"Controller: D-pad or left stick, A/B, LB/RB, Start and Back.\n\n"
                + bindings + b"\n\nRemap in the game window. Press F2 to keep a binding or Esc to cancel.",
                [(0, 1, b"Remap keyboard"), (0, 2, b"Reset keyboard"), (3, 0, b"Close")])
            # SDL can leave the keyboard focus on the game while a native
            # message box is unavailable. The wizard also works in that case.
            if choice in (None, 1):
                self.draft, self.step = self.keys.copy(), 0
                self.prompt()
            elif choice == 2:
                self.save(DEFAULT_KEYS.copy())
            self.blocked = True
        if self.draft is not None or self.focus() != self.window:
            return
        if self.release_key is not None:
            if self.keyboard[self.release_key]:
                return
            self.release_key = None
        pressed = {id_ for label, (id_, _, _) in BUTTONS.items() if self.keyboard[self.keys[label]]}
        if self.controller and self.attached(self.controller):
            pressed.update(id_ for id_, _, button in BUTTONS.values() if self.get_button(self.controller, button))
            x, y = self.get_axis(self.controller, 0), self.get_axis(self.controller, 1)
            pressed.update(id_ for id_, move in ((4, -y), (5, y), (6, -x), (7, x)) if move >= AXIS_DEADZONE)
        if self.blocked:
            # A menu action must be released before it can reach gameplay.
            self.blocked = bool(pressed)
        else:
            self.buttons = pressed
