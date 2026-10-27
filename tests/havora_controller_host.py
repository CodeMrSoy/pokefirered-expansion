"""Run production Havora C predicates on the host with engine boundary stubs.

This checks actual controller code, not GBA task execution or rendering.
Run alongside havora_v2_gym_audit.py for physical boat-route validation.
"""
from pathlib import Path
import ctypes as c
import itertools, json, re, subprocess, sys
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools/havora'))
import overhead_lock_geometry as geo
from tidal_color_rules import apply_switch
from boat_routes import route,water_map
source=(R/'src/havora_gym.c').read_text()
def function(name):
    match=re.search(r'^(?:static )?(?:u8|bool8|void) '+name+r'\([^\n]*\)\n\{',source,re.M)
    assert match,name
    start=match.start();i=match.end();depth=1
    while depth:
        depth += (source[i]=='{')-(source[i]=='}');i+=1
    return source[start:i]+'\n'
D=R/'build/havora-tests';D.mkdir(parents=True,exist_ok=True)
preamble=r'''
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint8_t u8; typedef int8_t s8; typedef uint16_t u16; typedef int16_t s16; typedef uint32_t u32; typedef int bool8;
#define TRUE 1
#define FALSE 0
#define TASK_NONE 255
#define MAP_OFFSET 7
#define LOCK_WIDTH 80
#define LOCK_HEIGHT 27
#define LOCK_ENTRY_X 3
#define LOCK_ENTRY_Y 25
#define VERSION 0x8000
#define ALL_CREWS 251
#define ALL_SWITCHES 127
#define PARTY_SIZE 6
#define ARRAY_COUNT(x) (sizeof(x)/sizeof((x)[0]))
#define VAR_HAVORA_GYM_STATE 0x40d7
#define VAR_HAVORA_GYM_PROGRESS 0x40d8
#define VAR_VIDRA_CRESTS 0x40d9
#define VAR_HAVORA_GYM_SWITCHES 0x40da
#define MON_DATA_SPECIES 0
#define MON_DATA_IS_EGG 1
#define MON_DATA_HP 2
#define STR_CONV_MODE_LEFT_ALIGN 0
u16 vars[65536], grid[2160],gSpecialVar_0x8004,gSpecialVar_0x8005,gSpecialVar_0x8006,gSpecialVar_0x8008,gSpecialVar_0x8009,gSpecialVar_Result;
struct ObjectEvent {struct {s16 x,y;} currentCoords;};
struct ObjectEvent gObjectEvents[1];struct {u8 objectEventId;} gPlayerAvatar;
struct Pokemon {u16 species,egg,hp;} gPlayerParty[6];
struct Save {struct {s16 x,y;} pos;} save, *gSaveBlock1Ptr=&save;
u8 gStringVar1[200],gStringVar2[200],gStringVar3[200];
static const u8 sA[]="A ",sB[]=" B ",sC[]=" C ";
static const u8 *sLevels[]={(const u8*)"LOW",(const u8*)"MID",(const u8*)"HIGH"};
u16 VarGet(u16 n){return vars[n];} void VarSet(u16 n,u16 v){vars[n]=v;}
bool8 Here(void){return TRUE;}void AnimateTide(void){}void MoveBoat(void){}
u8 FindTaskIdByFunc(void (*f)(void)){(void)f;return TASK_NONE;}
bool8 StartTide(u8 next){vars[VAR_HAVORA_GYM_STATE]=VERSION|next;return TRUE;}
void Draw(bool8 redraw){(void)redraw;}
u16 MapGridGetMetatileIdAt(s16 x,s16 y){return grid[(y-7)*80+x-7]&1023;}
u8 MapGridGetCollisionAt(s16 x,s16 y){return (grid[(y-7)*80+x-7]>>10)&3;}
int boat_ok=1;
bool8 StartBoat(const u8 *src,const u8 *dst){(void)src;(void)dst;return boat_ok;}
u16 GetMonData(struct Pokemon *p,int f){return f==0?p->species:f==1?p->egg:p->hp;}
void HealPlayerParty(void){for(int i=0;i<6;i++)if(gPlayerParty[i].species)gPlayerParty[i].hp=100;}
void StringCopy(u8 *a,const u8 *b){strcpy((char*)a,(const char*)b);}
void StringAppend(u8 *a,const u8 *b){strcat((char*)a,(const char*)b);}
void ConvertIntToDecimalStringN(u8 *a,int b,int mode,int n){(void)mode;(void)n;a[0]='0'+b;a[1]=0;}
'''
code=preamble+(R/'src/data/havora_tidal_trial.h').read_text()
for name in ['Valid','Water','CountBits','HavoraGym_OnLoad','HavoraGym_OnResume','AtControl','Operate','Travel','CheckTrainer','HavoraGym_Control']:
    code+=function(name)
probe=D/'controller-host.c';probe.write_text(code)
shared=D/'controller-host.so'
subprocess.run(['gcc','-shared','-fPIC','-O2','-Wall','-Wextra','-Werror',str(probe),'-o',str(shared)],check=True)
h=c.CDLL(str(shared));vars=(c.c_uint16*65536).in_dll(h,'vars');grid=(c.c_uint16*2160).in_dll(h,'grid')
class Mon(c.Structure):_fields_=[('species',c.c_uint16),('egg',c.c_uint16),('hp',c.c_uint16)]
party=(Mon*6).in_dll(h,'gPlayerParty')
coords=(c.c_int16*2).in_dll(h,'gObjectEvents')
def setwater(w):
    vars[0x40d7]=0x8000+w[0]+3*w[1]+9*w[2]
    grid[:]=geo.draw((w,0,0,4,0,False))
def command(cmd,a=0,b=0,xy=(3,25)):
    coords[:]=[xy[0]+7,xy[1]+7]
    for key,value in [('gSpecialVar_0x8004',cmd),('gSpecialVar_0x8005',a),('gSpecialVar_0x8006',b)]:c.c_uint16.in_dll(h,key).value=value
    h.HavoraGym_Control();return c.c_uint16.in_dll(h,'gSpecialVar_Result').value
spec=json.loads((R/'tools/havora/tidal_trial.json').read_text());P=spec['platforms'];L=spec['links']
checks=0
for w in itertools.product(range(3),repeat=3):
    for n,p in enumerate(P):
        if n==6 and w[1]==2:continue
        for k,(x,y) in enumerate(p['switches']):
            setwater(w);vars[0x40d8]=251;vars[0x40da]=0
            nw=apply_switch(w,p['switch_colors'][k].lower());blocked=n==6 and nw[1]==2
            result=command(30,n,k,(x+1,y))
            assert result==(7 if blocked else 1),(w,n,k,result)
            expected=w if blocked else nw
            assert vars[0x40d7]==0x8000+expected[0]+3*expected[1]+9*expected[2]
            assert vars[0x40da]==(0 if blocked else 1<<n)
            setwater(w);vars[0x40d8]=251^p['victory'];vars[0x40da]=0
            assert command(30,n,k,(x+1,y))==2 and vars[0x40da]==0
            checks+=1
print('PASS actual C:',checks,'lever/water combinations; four colors, wraparound, island flood rejection and victory gates')
setwater((0,0,0));vars[0x40d8]=251
for n in range(7):assert command(30,n,2,(1,0))==3
assert command(30,0,0,(10,10))==3
for i in range(6):party[i]=Mon(131,0,100)
vars[0x40da]=127
assert command(24)==1
for p in P:
    vars[0x40d8]=251^p['victory'];assert command(24)==2
vars[0x40d8]=251
for n in range(7):
    vars[0x40da]=127^(1<<n);assert command(24)==2
vars[0x40da]=127
for i in range(6):
    for attr in ['species','egg','hp']:
        party[i]=Mon(131,0,100);setattr(party[i],attr,1 if attr=='egg' else 0)
        assert command(24)==3,(i,attr)
        party[i]=Mon(131,0,100)
setwater((1,1,1));assert command(24)==2
setwater((1,1,0));party[0].hp=0;assert command(25)==1 and command(24)==1
assert command(15)==1 and vars[0x40d7]==0x8000 and vars[0x40d8]==251 and vars[0x40da]==127
vars[0x40d8]=255;vars[0x40d9]=0;command(6);assert vars[0x40d9]==1
print('PASS actual C: removed/remote lever rejection; every missing crew/station blocked; six healthy non-egg Pokemon required; healing, reset retention and crest reward')
checks=0
for w in itertools.product(range(3),repeat=3):
    for i,l in enumerate(L):
        setwater(w);vars[0x40d8]=251;vars[0x40da]=127
        b=water_map(w);open_route=route(w,l['pad_from'],l['pad_to']) is not None
        c.c_int.in_dll(h,'boat_ok').value=open_route
        expected=not any(a>=0 and a!=z for a,z in zip(l['water'],w)) and not b[l['pad_to'][1]*80+l['pad_to'][0]]&0xc00 and open_route
        assert command(31,xy=l['pad_from'])==(1 if expected else 7),(w,i)
        vars[0x40da]=127^(1<<l['from'])
        assert command(31,xy=l['pad_from'])==2
        checks+=1
print('PASS actual C:',checks,'route/water predicates and outbound switch gates; physical hull path supplied by separate map model')
vars[0x40d8]=1;vars[0x40da]=1;vars[0x40d7]=0x4400;h.HavoraGym_OnLoad()
assert vars[0x40d7]==0x8000 and vars[0x40d8]==1 and vars[0x40da]==1
vars[0x40d8]=63;vars[0x40da]=0;vars[0x40d7]=0x8408;h.HavoraGym_OnLoad()
assert vars[0x40d7]==0x8000 and vars[0x40d8]==255 and vars[0x40da]==127
print('PASS actual C: unfinished and completed legacy state migration preserves clearance')
