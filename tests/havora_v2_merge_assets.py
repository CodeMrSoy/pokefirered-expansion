"""Preserve Havora maps/art and V2's latest QOL implementations in the merge."""
import subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
H='3a4217c7b1ad72a04c246efdd61f34911a94f395'
Q='1df9e1212555b1ec3616d53a7bc572875ec94f29'
V='5ecfc051c22c4f82f9b6c6b6e3c1d0c0dec12bac'
def contents(ref,path):return subprocess.check_output(['git','show',ref+':'+path],cwd=R)
def equal(ref,path):
 old=contents(ref,path);new=(R/path).read_bytes()
 if path.endswith('.pal'):old=old.replace(b'\r\n',b'\n');new=new.replace(b'\r\n',b'\n')
 assert new==old,path
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',H,'--','data/maps','data/layouts','data/tilesets'],cwd=R,text=True).splitlines();count=0
for p in paths:
 if '/Havora' in p or '/havora_' in p or p.startswith('data/layouts/') or p.startswith('data/maps/') and p.endswith('/map.json'):
  equal(H,p);count+=1
# The nurse fix, window fix, shared art and native puzzle controller are kept.
for p in ['data/scripts/pkmn_center_nurse.inc','include/config/debug.h','src/start_menu.c','src/havora_puzzle.c','data/tilesets/window_lighting.json']:
 equal(H,p)
# These are QOL's actual traversal/case/lighting implementations, not copied
# substitutes. Shared hook files intentionally combine both branches.
for prefix in ['src/field_tools.c','src/field_item_case.c','src/lantern_glow.c','graphics/field_effects/field_tools','graphics/items/icons/field_item_case','data/scripts/field_moves.inc']:
 for p in subprocess.check_output(['git','ls-tree','-r','--name-only',Q,'--',prefix],cwd=R,text=True).splitlines():equal(Q,p)
assert subprocess.run(['git','merge-base','--is-ancestor',Q,V],cwd=R).returncode==0,'Latest QOL not contained by V2'
for file in ['src/scrcmd.c','src/field_control_avatar.c']:
 s=(R/file).read_text();assert '#include "field_tools.h"' in s and '#include "havora_puzzle.h"' in s
assert 'HavoraPuzzle_RecordCut(localId' in (R/'src/scrcmd.c').read_text()
assert 'HavoraPuzzle_CanEnterPit' in (R/'src/field_player_avatar.c').read_text()
print(f'PASS {count} Havora map/art/layout/event files preserved, all service fixes retained, latest QOL case/tools/lighting retained, both hook headers combined, and QOL ancestry confirmed')
