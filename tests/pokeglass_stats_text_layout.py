#!/usr/bin/env python3
"""Audit every compiled ability string against the Stats screen's actual font."""
import os
from pathlib import Path
import struct
import subprocess

root = Path(__file__).resolve().parents[1]
rom = (root / 'pokefirered.gba').read_bytes()
symbols = {}
for line in subprocess.check_output([os.environ.get('ARM_NM', 'arm-none-eabi-nm'), '-S', str(root / 'pokefirered.elf')], text=True).splitlines():
    fields = line.split()
    if len(fields) == 4:
        symbols[fields[3]] = (int(fields[0], 16) - 0x08000000, int(fields[1], 16))
start, size = symbols['gFontSmallLatinGlyphWidths']
widths = rom[start:start + size]

def text(address):
    return rom[address:rom.index(b'\xff', address)]

def width(string):
    assert b'\xfe' not in string, 'Stats requires a single line'
    assert all(character < 0xF7 for character in string), 'Unexpected text control code'
    return sum(widths[character] for character in string)

start, size = symbols['gAbilitiesInfo']
# Ability's compiled layout: name[17], padding, description pointer, AI rating.
assert size % 28 == 0
for index in range(size // 28):
    entry = start + index * 28
    description = struct.unpack_from('<I', rom, entry + 20)[0] - 0x08000000
    assert width(text(entry)) <= 143, ('Ability name too wide', index)
    assert width(text(description)) <= 189, ('Ability description too wide', index)
print(f'PASS {size // 28} ability names/descriptions fit Stats columns and borders')
