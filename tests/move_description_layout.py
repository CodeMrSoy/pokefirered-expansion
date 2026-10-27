#!/usr/bin/env python3
"""Check every compiled move description against the actual UI fonts and boxes."""
import os
import pathlib
import re
import struct
import subprocess

root = pathlib.Path(__file__).resolve().parents[1]
rom = (root / 'pokefirered.gba').read_bytes()
prefix = os.environ.get('ARM_NM', 'arm-none-eabi-nm').removesuffix('nm')
symbols = {}
for line in subprocess.check_output([prefix + 'nm', '-S', str(root / 'pokefirered.elf')], text=True).splitlines():
    parts = line.split()
    if len(parts) == 4:
        symbols[parts[3]] = (int(parts[0], 16) - 0x08000000, int(parts[1], 16))
cpp = subprocess.check_output([prefix + 'cpp', '-P', '-I', str(root / 'include'), '-'],
                              input='#include "constants/moves.h"\nMOVES_COUNT_ALL\n', text=True)
count = eval(cpp.strip().splitlines()[-1], {'__builtins__': {}}, {})
base, size = symbols['gMovesInfo']
assert size % count == 0
stride = size // count

def read_string(pointer):
    offset = pointer - 0x08000000
    assert 0 <= offset < len(rom)
    return rom[offset:rom.index(b'\xff', offset)]

def widths(symbol):
    offset, length = symbols[symbol]
    return rom[offset:offset + length]

normal = widths('gFontNormalLatinGlyphWidths')
small = widths('gFontSmallLatinGlyphWidths')
fonts_source = (root / 'src/text.c').read_text()

def font_height(font):
    block = re.search(r'\[' + font + r'\] = \{(.*?)\}', fonts_source, re.S)[1]
    return int(re.search(r'\.maxLetterHeight = (\d+)', block)[1])

def window(source, marker):
    block = source[source.index(marker):].split('}', 1)[0]
    return {key: int(value, 0) for key, value in re.findall(r'\.(width|height|baseBlock) = (0x[\da-fA-F]+|\d+)', block)}

summary_source = (root / 'src/pokemon_summary_screen.c').read_text()
summary = window(summary_source, '[POKESUM_WIN_MOVES_4 - 3]')
# The description begins at x=7/y=42 below Power and Accuracy.
assert re.search(r'FONT_NORMAL,\s*7, 42,\s*0, 0,.*?\.description', summary_source, re.S)
relearner = window((root / 'src/learn_move.c').read_text(), '.tilemapLeft = 2,\n        .tilemapTop = 6,')
battle_source = (root / 'src/battle_bg.c').read_text()
battles = [window(battle_source[pos:], '[B_WIN_MOVE_DESCRIPTION]')
           for pos in [m.start() for m in re.finditer(r'\[B_WIN_MOVE_DESCRIPTION\]', battle_source)]]
assert len(battles) == 2
categories = [window(battle_source[pos:], '[B_WIN_CATEGORY_ICON]')
              for pos in [m.start() for m in re.finditer(r'\[B_WIN_CATEGORY_ICON\]', battle_source)]]
assert len(categories) == len(battles)
battle_text = (root / 'src/battle_message.c').read_text().split('[B_WIN_MOVE_DESCRIPTION] = {', 1)[1].split('}', 1)[0]
assert '.fontId = FONT_SMALL,' in battle_text
checks = [('Summary', normal, summary['width'] * 8 - 7, summary['height'] * 8 - 42, font_height('FONT_NORMAL')),
          ('Move Relearner', normal, relearner['width'] * 8 - 1, relearner['height'] * 8, font_height('FONT_NORMAL_COPY_2'))]
for i, (box, category) in enumerate(zip(battles, categories)):
    # A header occupies one text line above the move's description.
    checks.append((f'Battle {i}', small, box['width'] * 8, box['height'] * 8 - 1 - font_height('FONT_SMALL'), font_height('FONT_SMALL')))
    assert box['baseBlock'] + box['width'] * box['height'] <= category['baseBlock'], 'Battle window overlaps category icon tiles'
    assert category['baseBlock'] + category['width'] * category['height'] <= 1024, 'Category window exceeds character tiles'
small_narrow = widths('gFontSmallNarrowLatinGlyphWidths')
small_narrower = widths('gFontSmallNarrowerLatinGlyphWidths')
errors = []
for move in range(count):
    name, pointer = struct.unpack_from('<II', rom, base + move * stride)
    # Summary/level-up name buffers hold 16 glyphs plus EOS. Long special
    # names use an ellipsis; shorter names keep their full spelling.
    full_name = read_string(name)
    display_name = full_name[:16]
    if len(full_name) > 16:
        display_name = display_name[:15] + b'\xb0'
    name_widths = [sum(glyphs[c] for c in display_name)
                   for glyphs in (normal, small, small_narrow, small_narrower)]
    if min(name_widths) > 80:
        errors.append(f'Move {move}: display name exceeds the 80px move pane')
    description = read_string(pointer)
    assert not any(c in description for c in (0xfc, 0xfd, 0xf7)), 'Extend auditor for new inline controls'
    lines = description.split(b'\xfe')
    for screen, glyphs, width, height, line_height in checks:
        widest = max(sum(glyphs[c] for c in line) for line in lines)
        if widest > width or len(lines) * line_height > height:
            errors.append(f'Move {move}, {screen}: {widest}/{width}px, {len(lines) * line_height}/{height}px')
assert not errors, '\n'.join(errors)
print(f'PASS all {count} compiled move descriptions fit Summary, Move Relearner and both battle layouts; all move names fit the five-row learning list')
