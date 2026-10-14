#!/usr/bin/env python3
"""Tablet Pokédex visibility, navigation, text, habitats, and cleanup checks."""
import pathlib
import re
import struct
import numpy as np

setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))

def enum_names(path, prefix):
    source = path.read_text().split('enum', 1)[1].split('}', 1)[0]
    return re.findall(r'\b' + prefix + r'[A-Z0-9_]+\b', source)

dex_names = enum_names(m.root / 'include/constants/pokedex.h', 'NATIONAL_DEX_')
area_names = enum_names(m.root / 'include/constants/region_map_sections.h', 'MAPSEC_')
count = dex_names.index('NATIONAL_DEX_PECHARUNT')
area_count = area_names.index('MAPSEC_COUNT')

class GlassDex(c.Structure):
    _fields_ = [('species', c.c_uint16 * count), ('areas', c.c_uint16 * area_count),
                ('count', c.c_uint16), ('cursor', c.c_uint16), ('seen', c.c_uint16),
                ('caught', c.c_uint16), ('sprite', c.c_uint16), ('areaCount', c.c_uint16),
                ('areaPage', c.c_uint8), ('view', c.c_uint8), ('filter', c.c_uint8),
                ('alphabetical', c.c_uint8), ('textPage', c.c_uint8), ('textLines', c.c_uint8),
                ('text', (c.c_uint8 * 64) * 16)]

shell_mask = np.zeros((160, 240), dtype=bool)
shell_mask[10:150, 12:228] = True
shell_mask[23:136, 20:220] = False
hub_shell = None

def data():
    current = np.asarray(m.screen)[shell_mask]
    if not np.array_equal(current, hub_shell):
        ys, xs = np.where(shell_mask)
        different = np.any(current != hub_shell, axis=1)
        print('Shell differences:', list(zip(xs[different], ys[different]))[:30], flush=True)
        m.snap('tablet-dex-shell-error')
    assert np.array_equal(current, hub_shell), 'Dex content changed the shared tablet shell'
    pointer = struct.unpack('<I', m.read(m.symbols['sGlassDex'], 4))[0]
    return GlassDex.from_buffer_copy(m.read(pointer, c.sizeof(GlassDex)))

def open_app():
    global hub_shell
    m.press(3)
    m.press(8)
    assert m.read(m.symbols['sHubCursor'], 1) == b'\x00'
    hub_shell = np.asarray(m.screen)[shell_mask].copy()
    m.press(8)
    wait_task('Task_PokeGlassPokedex')

assert native('IsNationalPokedexEnabled') == 1, 'New games need the FireRed National Dex flag'
native('FlagSet', 0x829)  # Pokédex obtained, without granting any entries.
assert native('AddBagItem', 717, 1) == 1
native('DisableNationalPokedex')
open_app()
assert data().count == data().seen == data().caught == 0
m.snap('tablet-dex-empty')
m.press(8)
assert data().view == 0
m.press(3)  # Empty caught filter.
assert data().filter == 1 and data().count == 0
m.press(0)
assert m.read(m.symbols['sGlassDex'], 4) == b'\x00' * 4
m.press(0)
assert native('IsNationalPokedexEnabled') == 1, 'Existing saves must upgrade on app open'

seen = (1, 4, 7, 25, 133, 143, 152, 252, 722, 1025)
caught = (1, 252, 1025)
for dex in seen:
    native('GetSetPokedexFlag', dex, 2)
for dex in caught:
    native('GetSetPokedexFlag', dex, 3)
expected_species = [native('NationalPokedexNumToSpecies', dex) for dex in seen]
open_app()
assert data().count == len(seen) and data().seen == len(seen) and data().caught == len(caught)
assert list(data().species[:data().count]) == expected_species
m.snap('tablet-dex-list')
m.press(8)
assert data().view == 1 and data().textLines > 0
m.snap('tablet-dex-entry')
for _ in range((data().textLines + 1) // 2):
    m.press(8, 20)
assert data().textPage == 0
m.press(2)  # SELECT: cry, leaving the entry intact.
assert data().view == 1
m.press(11)  # R: habitat.
assert data().view == 2
m.snap('tablet-dex-habitat')
m.press(0)
assert data().view == 1
m.press(0)
assert data().view == 0
m.press(5, 20)
m.press(8)
assert data().view == 1
assert data().textLines == 2  # Seen-only entry stays locked.
m.snap('tablet-dex-seen-only')
m.press(0)
for _ in range(2):
    m.press(5, 20)
m.press(8)
m.press(11)
assert data().view == 2 and data().areaCount > 0, 'Pikachu should have wild habitat locations'
m.snap('tablet-dex-pikachu-habitat')
m.press(0)
m.press(0)
for _ in range(2):
    m.press(4, 20)
m.press(11)
assert data().cursor >= 6
m.snap('tablet-dex-non-kanto')
m.press(5, 20)
m.press(5, 20)
m.press(8)
assert data().species[data().cursor] == expected_species[-1]
m.snap('tablet-dex-gen9-entry')
m.press(0)
m.press(3)
assert data().filter == 1 and data().count == len(caught)
m.snap('tablet-dex-caught')
m.press(2)
assert data().alphabetical == 1
m.snap('tablet-dex-alphabetical')
m.press(0)
assert m.read(m.symbols['sGlassDex'], 4) == b'\x00' * 4
assert 0xd111 not in struct.unpack('<16H', m.read(m.symbols['sSpritePaletteTags'], 32))

for _ in range(8):
    m.press(8)
    wait_task('Task_PokeGlassPokedex')
    m.press(0)
    assert m.read(m.symbols['sGlassDex'], 4) == b'\x00' * 4
    assert 0xd111 not in struct.unpack('<16H', m.read(m.symbols['sSpritePaletteTags'], 32))
m.press(0)
assert native('GetNationalPokedexCount', 0) == len(seen)
assert native('GetNationalPokedexCount', 1) == len(caught)
assert native('TrySavingData', 0) == 1
m.lib.retro_reset()
m.run(360)
m.press(3)
m.press(8)
m.press(8)
m.run(180)
assert native('IsNationalPokedexEnabled') == 1
assert native('GetNationalPokedexCount', 0) == len(seen)
assert native('GetNationalPokedexCount', 1) == len(caught)
open_app()
assert data().count == len(seen)
m.snap('tablet-dex-save-reload')
m.press(0)
m.press(0)
print('Tablet Dex empty/list/detail/habitat/cry/filter/sort, non-Kanto/Gen9 visibility, cleanup, and real save/reload passed')
