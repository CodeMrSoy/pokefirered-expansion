#!/usr/bin/env python3
"""Compile production early-encounter selection with controlled species/PRNG stubs."""
from pathlib import Path
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "src/randomizer.c").read_text()
config = (ROOT / "include/config/randomizer.h").read_text()
minimum = int(re.search(r"#define RANDOMIZER_EARLY_MIN_CATCH_RATE\s+(\d+)", config).group(1))

def function(name):
    match = re.search(r"^(?:static )?(?:inline )?[^\n;]+\b"+name+r"\([^;]*?\)\n\{", source, re.M)
    assert match, name
    end = source.index("{", match.start())+1
    depth = 1
    while depth:
        depth += (source[end]=="{")-(source[end]=="}")
        end += 1
    return source[match.start():end]

groups = json.loads((ROOT / "data/maps/map_groups.json").read_text())
names = {
    "PalletTown":"PALLET_TOWN", "ViridianCity":"VIRIDIAN_CITY",
    "PewterCity":"PEWTER_CITY", "Route1":"ROUTE1", "Route2":"ROUTE2",
    "Route22":"ROUTE22", "ViridianForest":"VIRIDIAN_FOREST",
    "Route3":"ROUTE3", "MtMoon_1F":"MT_MOON_1F", "Havora_Market":"HAVORA_MARKET",
}
defines = ""
for group, group_name in enumerate(groups["group_order"]):
    for number, name in enumerate(groups[group_name]):
        if name in names:
            defines += f"#define MAP_{names[name]} ({number} | ({group} << 8))\n"

prefix = r"""
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32; typedef int bool32;
#define TRUE 1
#define FALSE 0
#define SPECIES_NONE 0
#define SPECIES_RATTATA 1
#define RANDOMIZER_MAX_MON 10
#define MON_RANDOMIZER_INVALID 99
#define RANDOMIZE_WILD_MON 1
#define RANDOMIZER_REASON_WILD_ENCOUNTER 1
#define RANDOMIZER_OPTION_SPECIES_MODE 0
#define MGBA_LOG_DEBUG 0
#define MgbaPrintf(...) ((void)0)
#define MAP_NUM(m) ((m)&255)
#define MAP_GROUP(m) ((m)>>8)
enum WildPokemonArea {LAND,WATER,ROCKS,FISHING,HIDDEN};
struct Info {int baseHP,randomizerMode,isLegendary,isMythical,isUltraBeast,catchRate;};
static struct Info gSpeciesInfo[11]={
 {0,99,0,0,0,0}, {30,0,0,0,0,255}, {30,0,0,0,0,119},
 {30,0,0,0,0,120}, {30,0,1,0,0,255}, {30,0,0,1,0,255},
 {30,0,0,0,1,255}, {30,99,0,0,0,255}, {0,0,0,0,0,255},
 {30,0,0,0,0,200}, {30,0,0,0,0,3}
};
static u32 runSeed=1;
static int enabled=1,mode=0;
static u16 forced=4;
int RandomizerFeatureEnabled(int f) {return enabled;}
int GetRandomizerOption(int o) {return mode;}
u32 GetRandomizerSeed(void) {return runSeed;}
u16 RandomizeMon(int reason,int option,u32 seed,u16 original) {return forced;}
int IsRandomizationPossible(u16 original,u16 candidate) {
 return mode==0 || (mode==1 && candidate==3);
}
u16 RandomizerRandRange(int reason,u32 data1,u32 data2,u16 range) {
 assert(range); return (runSeed*1664525u+data1*1013904223u+data2)%range;
}
"""
checks = r"""
int main(void) {
 const u16 early[]={MAP_PALLET_TOWN,MAP_VIRIDIAN_CITY,MAP_PEWTER_CITY,MAP_ROUTE1,MAP_ROUTE2,MAP_ROUTE22,MAP_VIRIDIAN_FOREST};
 const u16 later[]={MAP_ROUTE3,MAP_MT_MOON_1F,MAP_HAVORA_MARKET};
 assert(!IsEarlyCatchSpecies(2)); assert(IsEarlyCatchSpecies(3));
 assert(!IsEarlyCatchSpecies(4)); assert(!IsEarlyCatchSpecies(5)); assert(!IsEarlyCatchSpecies(6));
 assert(!IsEarlyCatchSpecies(7)); assert(!IsEarlyCatchSpecies(8)); assert(!IsEarlyCatchSpecies(0));
 assert(!IsEarlyCatchSpecies(65535));
 unsigned long cases=0;
 for(runSeed=1;runSeed<=200;runSeed++)
  for(mode=0;mode<3;mode++)
   for(unsigned m=0;m<sizeof(early)/sizeof(*early);m++)
    for(int area=LAND;area<=HIDDEN;area++)
     for(int slot=0;slot<12;slot++)
      for(forced=0;forced<=RANDOMIZER_MAX_MON;forced++) {
       u16 result=RandomizeWildEncounter(1,MAP_NUM(early[m]),MAP_GROUP(early[m]),area,slot);
       assert(IsEarlyCatchSpecies(result));
       assert(result==RandomizeWildEncounter(1,MAP_NUM(early[m]),MAP_GROUP(early[m]),area,slot));
       if(IsEarlyCatchSpecies(forced)) assert(result==forced);
       else if(mode==1) assert(result==3);
       cases++;
      }
 enabled=1; forced=4;
 for(unsigned m=0;m<sizeof(later)/sizeof(*later);m++)
  assert(RandomizeWildEncounter(1,MAP_NUM(later[m]),MAP_GROUP(later[m]),LAND,0)==4);
 enabled=0;
 for(unsigned m=0;m<sizeof(early)/sizeof(*early);m++)
  assert(RandomizeWildEncounter(2,MAP_NUM(early[m]),MAP_GROUP(early[m]),LAND,0)==2);
 // Map number alone must not activate protection in another map group.
 assert(!IsEarlyCatchMap(MAP_NUM(MAP_ROUTE1),99));
 // Empty custom pools must not make a zero-range PRNG call.
 for(unsigned i=0;i<=RANDOMIZER_MAX_MON;i++) gSpeciesInfo[i].catchRate=0;
 assert(RandomizeEarlyCatchSpecies(1,4,123)==SPECIES_RATTATA);
 printf("PASS: %lu selections; 200 seeds; all early maps, encounter areas and slots; catch threshold; legendary/mythical/UB exclusion; mode fallback; stable results; later maps; disabled behavior\n",cases);
}
"""
code = prefix + defines + f"\n#define RANDOMIZER_EARLY_MIN_CATCH_RATE {minimum}\n"
for name in ["IsSpeciesPermitted","IsRandomizerLegendary","IsEarlyCatchMap","IsEarlyCatchSpecies","RandomizeEarlyCatchSpecies","RandomizeWildEncounter"]:
    code += function(name)+"\n"
with tempfile.TemporaryDirectory() as directory:
    c = Path(directory)/"early.c"
    binary = Path(directory)/"early"
    c.write_text(code+checks)
    subprocess.run(["cc","-std=c99","-O2","-Wall","-Wextra","-Werror","-Wno-unused-parameter",str(c),"-o",str(binary)],check=True)
    subprocess.run([str(binary)],check=True)
