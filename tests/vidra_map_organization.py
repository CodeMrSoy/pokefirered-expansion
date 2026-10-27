#!/usr/bin/env python3
"""Check Vidra directory/group references and preservation of authored map data."""
import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
groups=read('data/maps/map_groups.json');manifest=read('docs/vidra/map-renames.json')
listed=[n for g in groups['group_order'] for n in groups[g]]
assert len(listed)==len(set(listed))
maps={}
for name in listed:
 m=read(f'data/maps/{name}/map.json');assert m['name']==name
 assert m['id'] not in maps;maps[m['id']]=m
layouts=read('data/layouts/layouts.json')['layouts'];layout_ids={x['id'] for x in layouts}
for l in layouts:
 for key in ('blockdata_filepath','border_filepath'):assert (ROOT/l[key]).is_file(),l[key]
for m in maps.values():
 assert m['layout'] in layout_ids,m['layout']
 for conn in m.get('connections') or []:assert conn['map'] in maps,conn
 for warp in m.get('warp_events',[]):assert warp['dest_map'] in maps or warp['dest_map'] in ('MAP_NONE','MAP_UNDEFINED','MAP_DYNAMIC'),warp
# The base is the committed pre-reorganization map data in this isolated branch.
for entry in manifest['maps']:
 before=json.loads(subprocess.check_output(['git','show',f"{manifest['base_commit']}:data/maps/{entry['old']}/map.json"],cwd=ROOT))
 after=read(f"data/maps/{entry['new']}/map.json")
 for events in ('object_events','warp_events','coord_events','bg_events'):
  a,b=before.get(events,[]),after.get(events,[]);assert len(a)==len(b),(entry,events)
  for old,new in zip(a,b):
   for k in old:
    if not isinstance(old[k],str):assert old[k]==new[k],(entry,events,k)
 for key in ('width','height'):
  assert next(l for l in layouts if l['id']==after['layout'])[key] > 0
 before_layouts=json.loads(subprocess.check_output(['git','show',manifest['base_commit']+':data/layouts/layouts.json'],cwd=ROOT))['layouts']
 oldlayout=next(l for l in before_layouts if l['id']==before['layout'])
 newlayout=next(l for l in layouts if l['id']==after['layout'])
 for key in ('blockdata_filepath','border_filepath'):
  assert subprocess.check_output(['git','show',manifest['base_commit']+':'+oldlayout[key]],cwd=ROOT)==(ROOT/newlayout[key]).read_bytes(),entry
print(f"Validated {len(manifest['maps'])} renamed maps, all groups/warps/connections/layouts, unchanged geometry and event positions")
