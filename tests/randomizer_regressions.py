#!/usr/bin/env python3
"""Host regression checks for encounter wiring and rival story milestones.

Extracts production functions; encounter selection and randomization are controlled
stubs so assertions verify arguments/results, not PRNG quality or gameplay.
Run with python3 tests/randomizer_regressions.py (requires a host C compiler).
"""
from pathlib import Path
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

wild = (ROOT / "src/wild_encounter.c").read_text()
rival = (ROOT / "src/randomizer.c").read_text()
prefix = """#include <stdint.h>
#include <stdio.h>
#include <assert.h>
typedef uint8_t u8; typedef uint16_t u16; typedef int bool8;
#define FALSE 0
#define OW_LIGHTNING_ROD 0
#define OW_FLASH_FIRE 0
#define OW_HARVEST 0
#define OW_STORM_DRAIN 0
#define GEN_8 8
#define TRUE 1
#define WILD_CHECK_REPEL 1
#define WILD_CHECK_KEEN_EYE 2
#define ABILITY_MAGNET_PULL 1
#define ABILITY_STATIC 2
#define ABILITY_HARVEST 3
#define ABILITY_FLASH_FIRE 4
#define ABILITY_STORM_DRAIN 5
#define TYPE_STEEL 1
#define TYPE_ELECTRIC 2
#define TYPE_GRASS 3
#define TYPE_FIRE 4
#define TYPE_WATER 5
#define LAND_WILD_COUNT 12
#define WATER_WILD_COUNT 5
#define TRY_GET_ABILITY_INFLUENCED_WILD_MON_INDEX(...) 0
#define TryGetAbilityInfluencedWildMonIndex(...) 0
struct WildPokemon {u8 minLevel,maxLevel;u16 species;};
struct WildPokemonInfo {u8 encounterRate; const struct WildPokemon *wildPokemon;};
enum WildPokemonArea {WILD_AREA_LAND,WILD_AREA_WATER,WILD_AREA_ROCKS,WILD_AREA_FISHING,WILD_AREA_HIDDEN};
struct Save {struct {u8 mapGroup,mapNum;} location;} saved={{3,7}},*gSaveBlock1Ptr=&saved;
u8 ChooseWildMonIndex_Land(void){return 1;}
u8 ChooseWildMonIndex_WaterRock(void){return 1;}
u8 ChooseWildMonLevel(const struct WildPokemon *p,u8 i,u8 a){return p[i].minLevel;}
int IsWildLevelAllowedByRepel(u8 l){return 1;}
int IsAbilityAllowingEncounter(u8 l){return 1;}
int seed;
int GetRandomizerSeed(void){return seed;}
static int calls;
u16 RandomizeWildEncounter(u16 species,u8 mapNum,u8 mapGroup,enum WildPokemonArea a,u8 slot){assert(species==19);assert(mapNum==7);assert(mapGroup==3);assert(slot==1);calls++;return 25;}
void CreateWildMon(u16 species,u8 level,u8 slot){assert(species==(seed?25:19));assert(level==5);assert(slot==1);}
u8 ChooseWildMonIndex_Fishing(u8 rod){return 1;}
void UpdateChainFishingStreak(void){}
"""
roles = rival[rival.index("enum\n{\n    RIVAL_ROLE_STARTER"):rival.index("static u8 GetRivalRosterRole")]
code = prefix + '\n' + roles + '\n#include "constants/opponents.h"\n'
for source, name in [(wild, "TryGenerateWildMon"), (wild, "GenerateFishingEncounter"),
                     (rival, "GetRivalEncounterStage"), (rival, "HasRivalReachedSecondOccurrence")]:
    code += function(source, name) + "\n"
code += r"""
int main(void) {
    struct WildPokemon table[12]={{2,2,16},{5,5,19}};
    struct WildPokemonInfo info={10,table};
    for (int enabled=0; enabled<2; enabled++) {
        seed=enabled?123:0;
        for (int area=WILD_AREA_LAND; area<=WILD_AREA_ROCKS; area++)
            assert(TryGenerateWildMon(&info,area,0));
        for (int rod=0;rod<3;rod++)
            assert(GenerateFishingEncounter(&info,rod)==(seed?25:19));
    }
    assert(calls==6);
    for (int id=TRAINER_CHAMPION_REMATCH_SQUIRTLE; id<=TRAINER_CHAMPION_REMATCH_CHARMANDER; id++)
        for (int role=RIVAL_ROLE_STARTER;role<=RIVAL_ROLE_GYARADOS;role++)
            assert(HasRivalReachedSecondOccurrence(role,id));
    assert(!HasRivalReachedSecondOccurrence(RIVAL_ROLE_STARTER,TRAINER_RIVAL_OAKS_LAB_SQUIRTLE));
    assert(HasRivalReachedSecondOccurrence(RIVAL_ROLE_STARTER,TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE));
    assert(!HasRivalReachedSecondOccurrence(RIVAL_ROLE_BIRD,TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE));
    assert(HasRivalReachedSecondOccurrence(RIVAL_ROLE_BIRD,TRAINER_RIVAL_CERULEAN_SQUIRTLE));
    assert(!HasRivalReachedSecondOccurrence(RIVAL_ROLE_STARTER,65535));
    puts("PASS: land/water/rock, all rods, randomizer on/off, map arguments, rival rematches and story milestones");
}
"""
with tempfile.TemporaryDirectory() as directory:
    source = Path(directory) / "checks.c"
    binary = Path(directory) / "checks"
    source.write_text(code)
    subprocess.run(["cc", "-std=c99", "-I", str(ROOT / "include"), str(source), "-o", str(binary)], check=True)
    subprocess.run([str(binary)], check=True)
