#!/usr/bin/env python3
"""Run the actual Cap Candy target helper with host mocks and memory checks."""
from pathlib import Path
import os
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
source = (root / "src/party_menu.c").read_text()
start = source.index("static u8 GetCapCandyTargetLevel(")
end = source.index("\nvoid ItemUseCB_RareCandy(", start)
helper = source[start:end]

prefix = r'''
#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint8_t bool8;
#define TRUE 1
#define FALSE 0
#define MAX_MON_MOVES 4
#define MON_DATA_SPECIES 0
#define MON_DATA_MOVE1 1
#define LEVEL_UP_MOVE_END 0xFFFF
#define EVOLUTIONS_END 0xFFFF
enum { EVO_NONE, EVO_LEVEL, EVO_TRADE, EVO_ITEM };
struct LevelUpMove { u16 move, level; };
struct Evolution { u16 method, param, targetSpecies; const void *params; };
struct Pokemon { u16 moves[4]; };
static const struct LevelUpMove *moves;
static const struct Evolution *evos;
static u16 GetMonData(struct Pokemon *mon, int field) {
    return field == MON_DATA_SPECIES ? 1 : mon->moves[field - MON_DATA_MOVE1];
}
static const struct LevelUpMove *GetSpeciesLevelUpLearnset(u16 species) {
    (void)species; return moves;
}
static const struct Evolution *GetSpeciesEvolutions(u16 species) {
    (void)species; return evos;
}
'''
cases = r'''
int main(void) {
    struct Pokemon mon = {{10, 0, 0, 0}};
    const struct LevelUpMove empty[] = {{LEVEL_UP_MOVE_END, 0}};
    const struct LevelUpMove learnset[] = {{10, 6}, {11, 9}, {12, 7}, {LEVEL_UP_MOVE_END, 0}};
    const struct Evolution end[] = {{EVOLUTIONS_END, 0, 0, NULL}};
    const struct Evolution level[] = {{EVO_LEVEL, 8, 2, NULL}, {EVOLUTIONS_END, 0, 0, NULL}};
    const struct Evolution conditional[] = {{EVO_LEVEL, 0, 2, NULL}, {EVOLUTIONS_END, 0, 0, NULL}};
    const struct Evolution mixed[] = {{EVO_NONE, 0, 2, NULL}, {EVO_LEVEL, 8, 3, NULL}, {EVOLUTIONS_END, 0, 0, NULL}};
    const struct Evolution item[] = {{EVO_ITEM, 0, 2, NULL}, {EVOLUTIONS_END, 0, 0, NULL}};
    const struct Evolution high[] = {{EVO_LEVEL, 300, 2, NULL}, {EVOLUTIONS_END, 0, 0, NULL}};
    moves = empty; evos = NULL;
    assert(GetCapCandyTargetLevel(&mon, 5, 14) == 14);
    evos = end;
    assert(GetCapCandyTargetLevel(&mon, 5, 14) == 14);
    moves = learnset;
    assert(GetCapCandyTargetLevel(&mon, 5, 14) == 7);
    assert(GetCapCandyTargetLevel(&mon, 5, 6) == 6);
    moves = empty; evos = level;
    assert(GetCapCandyTargetLevel(&mon, 5, 14) == 8);
    assert(GetCapCandyTargetLevel(&mon, 8, 14) == 9);
    assert(GetCapCandyTargetLevel(&mon, 10, 14) == 11);
    evos = conditional;
    assert(GetCapCandyTargetLevel(&mon, 5, 14) == 6);
    evos = mixed;
    assert(GetCapCandyTargetLevel(&mon, 5, 14) == 8);
    evos = item;
    assert(GetCapCandyTargetLevel(&mon, 5, 14) == 14);
    evos = high;
    assert(GetCapCandyTargetLevel(&mon, 5, 100) == 100);
    evos = conditional;
    assert(GetCapCandyTargetLevel(&mon, 99, 100) == 100);
    puts("Cap Candy: 12 boundary cases passed with address/undefined-behavior sanitizers.");
}
'''
with tempfile.TemporaryDirectory() as directory:
    directory = Path(directory)
    cfile = directory / "cap_candy.c"
    binary = directory / "cap_candy"
    cfile.write_text(prefix + helper + cases)
    subprocess.run(["cc", "-std=c99", "-Wall", "-Wextra", "-Werror",
                    "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
                    "-o", str(binary), str(cfile)], check=True)
    # These tests allocate no heap memory; disable leak scanning for containers
    # where LeakSanitizer cannot inspect process threads. Bounds checks remain on.
    subprocess.run([str(binary)], check=True,
                   env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"})
