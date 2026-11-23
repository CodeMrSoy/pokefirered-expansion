"""Versioned read-only native context and isolated mGBA query transport."""
import ctypes as c
from struct import Struct

from world_manifest import catalog_check

MAGIC = 0x3731574C
KEYS = ("magic", "version", "generation", "origin", "seed", "mode", "modes", "features",
        "species_mode", "difficulty", "cap", "trainer_id", "starter_chosen", "starter_slot", "map")
CONTEXT = Struct("<15I")
HEADER = Struct("<6I")
COMMAND = Struct("<2I")
RESULT = Struct("<22I")
PAGE = 32
BASE = 0x02000000


def ewram_pointer(memory, address, size):
    base, length = memory(2)
    # The pinned libretro mGBA reports the GB size even for a GBA core.
    # Its GBA SYSTEM_RAM pointer nevertheless points to the full 256 KiB EWRAM.
    if length == 0x8000:
        length = 0x40000
    if not base or address % 4 or address < BASE or size > min(length, 0x40000) - (address - BASE):
        raise ValueError("Native export port outside EWRAM")
    return base + address - BASE


def read_context(memory, catalog):
    ptr = ewram_pointer(memory, catalog["ports"]["context"], CONTEXT.size)
    state = dict(zip(KEYS, CONTEXT.unpack(c.string_at(ptr, CONTEXT.size))))
    if state["magic"] != MAGIC or state["version"] != 1 or not state["generation"]:
        return None
    state.pop("magic")
    if not state.pop("starter_chosen"):
        state["starter_slot"] = None
    return state


def snapshot(core):
    from play import bind, VOID

    size = bind(core, "retro_serialize_size", c.c_size_t)()
    if not 0 < size <= 8 * 1024 * 1024:
        raise ValueError("Unsupported mGBA snapshot size")
    data = c.create_string_buffer(size)
    if not bind(core, "retro_serialize", c.c_bool, VOID, c.c_size_t)(data, size):
        raise RuntimeError("Could not snapshot player core")
    return data.raw


class NullDisplay:
    def open_audio(self, rate): pass
    def draw(self, *args): pass
    def audio(self, _, count): return count
    def key(self, *args): return 0


class Replica:
    """Construct only in a child process. Libretro cores expose singleton state."""
    page = PAGE

    def __init__(self, rom_path, core_path, catalog, frozen, expected_context=None):
        from play import Game, bind, VOID

        rom = rom_path.read_bytes()
        catalog_check(catalog, rom)
        self.game = Game(core_path, rom_path, rom, catalog["ports"]["context"], NullDisplay())
        try:
            data = c.create_string_buffer(frozen)
            if not bind(self.game.core, "retro_unserialize", c.c_bool, VOID, c.c_size_t)(data, len(frozen)):
                raise ValueError("mGBA rejected the isolated snapshot")
            self.context = read_context(self.memory, catalog)
            if not self.context or (expected_context is not None and self.context != expected_context):
                raise ValueError("Replica context differs from committed game")
            self.port = ewram_pointer(self.memory, catalog["ports"]["query"],
                                      HEADER.size + PAGE * (COMMAND.size + RESULT.size))
        except Exception:
            self.game.close()
            raise
        self.sequence = 0

    def memory(self, key):
        return self.game.memory(key), self.game.memory_size(key)

    def query(self, command, rows):
        if not 0 < len(rows) <= PAGE or command not in range(1, 7):
            raise ValueError("Invalid native export query")
        self.sequence += 1
        generation = self.context["generation"]
        request = HEADER.pack(MAGIC, generation, self.sequence, command, len(rows), 0)
        request += b"".join(COMMAND.pack(*row) for row in rows)
        c.memmove(self.port, request, len(request))
        for _ in range(180):
            self.game.core.retro_run()
            magic, gen, seq, op, count, reply = HEADER.unpack(c.string_at(self.port, HEADER.size))
            if (magic, gen, seq, op, count) != (MAGIC, generation, self.sequence, command, len(rows)):
                raise RuntimeError("Replica lost the committed export context")
            if reply == self.sequence:
                data = c.string_at(self.port + HEADER.size + PAGE * COMMAND.size, RESULT.size * count)
                return list(RESULT.iter_unpack(data))
        raise TimeoutError("Replica export did not complete in 180 frames")

    def close(self):
        self.game.close()
