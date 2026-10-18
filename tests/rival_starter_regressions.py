#!/usr/bin/env python3
"""Run production starter scoring/selection functions against controlled graphs.

Requires Python 3 and a host C compiler. No ROM or emulator is needed.
"""
from pathlib import Path
import os
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def function(source, name):
    match = re.search(r"^(?:static )?[^\n;]+\b" + name + r"\([^;]*?\)\n\{", source, re.M)
    assert match, name
    end = source.index("{", match.start()) + 1
    depth = 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[match.start():end]


source = (ROOT / "src/randomizer.c").read_text()
code = r"""
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
#define NUM_SPECIES 32
#define SPECIES_NONE 0
#define SPECIES_CHARMANDER 1
#define SPECIES_BULBASAUR 2
#define SPECIES_SQUIRTLE 3
#define EVO_NONE 0
#define EVO_LEVEL 1
#define EVO_ITEM 2
#define EVO_TRADE 3
#define EVOLUTIONS_END 0xffff
#define RANDOMIZE_STARTER_AND_GIFT_MON 1
#define ARRAY_COUNT(a) (sizeof(a) / sizeof((a)[0]))
struct Evolution {u16 method, param, targetSpecies;};
struct SpeciesInfo {u16 baseHP,baseAttack,baseDefense,baseSpeed,baseSpAttack,baseSpDefense;};
static struct SpeciesInfo gSpeciesInfo[NUM_SPECIES + 1];
static struct Evolution graph[NUM_SPECIES + 1][5];
static u16 sPlayerStarterSpecies[3];
static int enabled, nullSpecies;
static u16 SanitizeSpeciesId(u16 species) {return species > NUM_SPECIES ? 0 : species;}
static const struct Evolution *GetSpeciesEvolutions(u16 species) {
    return species == nullSpecies ? NULL : graph[species];
}
static int RandomizerFeatureEnabled(int feature) {(void)feature; return enabled;}
static u16 GetRandomizedStarterSpecies(u16 slot) {assert(slot < 3); return sPlayerStarterSpecies[slot];}
static void stats(u16 species, u16 total) {
    gSpeciesInfo[species] = (struct SpeciesInfo){total-5,1,1,1,1,1};
}
static void edge(u16 from, int index, u16 method, u16 to) {
    graph[from][index] = (struct Evolution){method,0,to};
}
"""
for name in ["GetSpeciesBaseStatTotal", "GetEvolutionLineBaseStatTotal",
             "GetRivalStarterBaseStatTotal", "GetRivalStarterSlot", "GetRivalStarterSpecies"]:
    code += function(source, name) + "\n"
code += r"""
int main(void) {
    nullSpecies = -1;
    for (int i=0; i<=NUM_SPECIES; i++) {
        stats(i, 100);
        for (int j=0; j<5; j++)
            graph[i][j].method = EVOLUTIONS_END;
    }
    // A weaker base wins thanks to its three-stage line: 200 -> 400 -> 600.
    // Its rival candidate has a stronger base but weaker final: 400 -> 500.
    stats(1,200); stats(2,400); stats(3,600);
    stats(4,400); stats(5,500); stats(6,900);
    edge(1,0,EVO_LEVEL,2); edge(2,0,EVO_LEVEL,3);
    edge(4,0,EVO_LEVEL,5);
    sPlayerStarterSpecies[0]=6; // Player's even stronger choice must be excluded.
    sPlayerStarterSpecies[1]=4; sPlayerStarterSpecies[2]=1;
    enabled=1;
    assert(GetRivalStarterSlot(0)==2);
    assert(GetRivalStarterSpecies(0)==1); // Receive the base, not its final form.
    assert(GetRivalStarterSlot(99)==2); // Invalid player slot defaults to zero.
    assert(GetRivalStarterSlot(1)==0);
    assert(GetRivalStarterSlot(2)==0);
    // Explore every branch, including item/trade and a shared evolution target.
    stats(7,650); stats(8,550);
    edge(4,1,EVO_ITEM,8); edge(8,0,EVO_TRADE,7);
    edge(4,2,EVO_TRADE,7);
    assert(GetRivalStarterBaseStatTotal(4)==650);
    assert(GetRivalStarterSlot(0)==1);
    // A metadata relationship must not inflate this starter to the 900 BST form.
    edge(1,1,EVO_NONE,6);
    assert(GetRivalStarterBaseStatTotal(1)==600);
    // Cycles and invalid/egg targets cannot loop or read outside the bitset.
    edge(3,0,EVO_LEVEL,1); edge(3,1,EVO_ITEM,65535);
    edge(3,2,EVO_ITEM,NUM_SPECIES);
    assert(GetRivalStarterBaseStatTotal(1)==600);
    assert(GetRivalStarterBaseStatTotal(0)==0);
    assert(GetRivalStarterBaseStatTotal(65535)==0);
    assert(GetRivalStarterBaseStatTotal(NUM_SPECIES)==0);
    // No evolution table and a standalone species retain their own strength.
    nullSpecies=9; stats(9,700);
    assert(GetRivalStarterBaseStatTotal(9)==700);
    assert(GetRivalStarterBaseStatTotal(6)==900);
    // Keep a stronger pre-evolution's potential if an evolution lowers BST.
    stats(10,800); edge(10,0,EVO_LEVEL,5);
    assert(GetRivalStarterBaseStatTotal(10)==800);
    // Stable ties favor the first remaining slot, regardless of base BST.
    stats(7,600);
    assert(GetRivalStarterSlot(0)==1);
    for (int i=0; i<20; i++) assert(GetRivalStarterSlot(0)==1);
    enabled=0;
    assert(GetRivalStarterSlot(0)==2);
    assert(GetRivalStarterSlot(1)==0);
    assert(GetRivalStarterSlot(2)==1);
    assert(GetRivalStarterSpecies(0)==SPECIES_CHARMANDER);
    assert(GetRivalStarterSpecies(1)==SPECIES_BULBASAUR);
    assert(GetRivalStarterSpecies(2)==SPECIES_SQUIRTLE);
    puts("PASS: evolution potential, all branches, player exclusion, base reward, metadata, cycles, invalid targets, ties, and randomizer off");
}
"""
with tempfile.TemporaryDirectory() as directory:
    c_file = Path(directory) / "checks.c"
    binary = Path(directory) / "checks"
    c_file.write_text(code)
    subprocess.run(["cc", "-std=c99", "-Wall", "-Wextra", "-Werror", "-fsanitize=address,undefined",
                    "-fno-omit-frame-pointer", str(c_file), "-o", str(binary)], check=True)
    # LeakSanitizer cannot inspect processes in some container environments.
    subprocess.run([str(binary)], check=True, env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"})
