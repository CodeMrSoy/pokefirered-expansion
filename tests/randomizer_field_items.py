#!/usr/bin/env python3
"""Compile production pickup logic with host stubs; no emulator is required."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "src/randomizer.c").read_text()
start = source.index("// Field pickups keep story keys fixed")
end = source.index("// Both legendary and mythical", start)
prefix = r"""
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#include "constants/items.h"
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef int bool32;
#define POCKET_KEY_ITEMS 5
#define RANDOMIZER_MAX_TM ITEM_TM50
#define RANDOMIZER_REASON_FIELD_ITEM 6
#define RANDOMIZE_FIELD_ITEMS 2
#define ARRAY_COUNT(a) (sizeof(a) / sizeof((a)[0]))
#define NELEMS(a) ARRAY_COUNT(a)
struct ScriptContext {int unused;};
struct Sfc32State {u32 value;};
struct {u8 mapNum, mapGroup, localId;} gObjectEvents[16];
u8 gSelectedObjectEvent;
struct Save {struct {u8 mapNum,mapGroup;} location;} save, *gSaveBlock1Ptr=&save;
u16 gSpecialVar_0x8000,gSpecialVar_0x8004,gSpecialVar_0x8005;
static int enabled=1;
static u32 seed=1, lastMap;
int RandomizerFeatureEnabled(int feature) {return enabled;}
int GetPocketByItemId(u16 id) {
    return (id==ITEM_GOLD_TEETH || id==ITEM_LIFT_KEY || id==ITEM_CARD_KEY
        || id==ITEM_SECRET_KEY || id==ITEM_SILPH_SCOPE
        || (id>=ITEM_HM01 && id<=ITEM_HM08)) ? POCKET_KEY_ITEMS : 1;
}
int ItemIsMail(u16 id) {return id>=ITEM_ORANGE_MAIL && id<=ITEM_RETRO_MAIL;}
int IsItemTMHM(u16 id) {return id>=ITEM_TM01 && id<=ITEM_HM08;}
struct Sfc32State RandomizerRandSeed(int reason,u32 map,u16 item) {
    lastMap=map;
    return (struct Sfc32State){seed ^ map ^ ((u32)item*2654435761u)};
}
u16 RandomizerNextRange(struct Sfc32State *s,u16 n) {
    assert(n); s->value=s->value*1664525u+1013904223u; return (s->value>>8)%n;
}
"""
checks = r"""
int main(void) {
    const u16 fixed[]={ITEM_GOLD_TEETH,ITEM_LIFT_KEY,ITEM_CARD_KEY,ITEM_SECRET_KEY,ITEM_SILPH_SCOPE,ITEM_NONE};
    for(seed=1;seed<=200;seed++) {
        for(unsigned i=0;i<ARRAY_COUNT(fixed);i++)
            assert(RandomizeFoundItem(fixed[i],3,4,1000)==fixed[i]);
        for(u16 item=ITEM_TM01;item<=ITEM_TM100;item++) {
            u16 r=RandomizeFoundItem(item,3,4,1000);
            assert(r>=ITEM_TM01 && r<=RANDOMIZER_MAX_TM && r!=item);
        }
        for(u16 item=1;item<ITEMS_COUNT;item++) {
            if(GetPocketByItemId(item)==POCKET_KEY_ITEMS && !(item>=ITEM_HM01 && item<=ITEM_HM08)) continue;
            if(item>=ITEM_TM01 && item<=ITEM_TM100) continue;
            u16 r=RandomizeFoundItem(item,3,4,1000);
            assert(ShouldRandomizeItem(r) && !IsItemTMHM(r) && r!=item);
            assert(RandomizeFoundItem(item,3,4,1000)==r);
        }
    }
    save.location.mapNum=3; save.location.mapGroup=4;
    gSpecialVar_0x8004=0x1234;
    gSpecialVar_0x8005=ITEM_POTION;
    FindHiddenItemRandomize_NativeCall(0);
    assert(lastMap==0x04031234);
    u16 hidden=gSpecialVar_0x8005;
    gSelectedObjectEvent=15;
    gObjectEvents[15].mapNum=99;
    gSpecialVar_0x8005=ITEM_POTION;
    FindHiddenItemRandomize_NativeCall(0);
    assert(gSpecialVar_0x8005==hidden);
    gObjectEvents[15].mapNum=3; gObjectEvents[15].mapGroup=4; gObjectEvents[15].localId=17;
    gSpecialVar_0x8000=ITEM_ORANGE_MAIL;
    FindItemRandomize_NativeCall(0);
    assert(lastMap==0x04030011 && !ItemIsMail(gSpecialVar_0x8000));
    enabled=0; gSpecialVar_0x8000=ITEM_POTION; gSpecialVar_0x8005=ITEM_POTION;
    FindItemRandomize_NativeCall(0); FindHiddenItemRandomize_NativeCall(0);
    assert(gSpecialVar_0x8000==ITEM_POTION && gSpecialVar_0x8005==ITEM_POTION);
    puts("PASS: 200 seeds, all item IDs, TM-only replacements, fixed story keys, no Mail/tools/HMs, stable hidden identity, toggle off");
}
"""
with tempfile.TemporaryDirectory() as directory:
    c = Path(directory)/"checks.c"
    exe = Path(directory)/"checks"
    whitelist = (ROOT / "src/data/randomizer/item_whitelist.h").read_text()
    whitelist = "\n".join(line for line in whitelist.splitlines() if not line.startswith("#include"))
    block = source[start:end].replace('#include "data/randomizer/item_whitelist.h"', whitelist)
    c.write_text(prefix+block+checks)
    subprocess.run(["cc","-std=c99","-I",str(ROOT/"include"),"-I",str(ROOT/"src"),str(c),"-o",str(exe)],check=True)
    subprocess.run([str(exe)],check=True)
