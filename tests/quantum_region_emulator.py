#!/usr/bin/env python3
"""Real map navigation, names, region switching, location icon and Fly safety."""
import json
import os
import pathlib
import struct
import subprocess
import quantum_qol_emulator as m
m.d = m.d / 'quantum_region_emulator'
m.d.mkdir(exist_ok=True)

source = (m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])

def ptr(name):
    return struct.unpack('<I', m.read(m.symbols[name], 4))[0]

def selected_region():
    return m.read(ptr('sRegionMap') + 38 + 5*600*2 + 3*2048*2 + 5, 1)[0]

def text(address):
    return m.read(address, 24).split(b'\xff')[0]

def move_to(x, y):
    for _ in range(50):
        cx, cy = struct.unpack('<hh', m.read(ptr('sMapCursor'), 4))
        if (cx, cy) == (x, y):
            return
        m.press(7 if cx < x else 6 if cx > x else 5 if cy < y else 4, 18)
    raise AssertionError(('Cursor did not arrive', x, y))

def choose_quantum():
    move_to(21, 11)
    m.press(8)
    m.snap('quantum-region-picker')
    m.press(5, 30)
    m.press(5, 30)
    m.press(8)
    assert selected_region() == 2
    assert text(ptr('sRegionMap')) == text(m.symbols['sMapName_PORT_CITY'])

m.inject(b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')
m.press(3)
m.press(8)
m.press(7, 20)
m.press(5, 20)
m.press(8)
assert selected_region() == 0
m.snap('quantum-kanto-preserved')
choose_quantum()
m.snap('quantum-island-map')
points = [('PORT_CITY',15,12),('COASTAL_CITY',4,10),('FOREST_TOWN',6,7),
          ('LAKE_TOWN',14,7),('SNOW_TOWN',10,2),('HOT_SPRINGS',13,2),
          ('COASTAL_ROAD',5,9),('FOREST_PATH',8,6),('MOUNTAIN_PASS',10,3),
          ('SNOW_TRAIL',11,2),('LAKE_ROAD',13,5),('HARBOR_ROAD',15,10),
          ('RIVER_ROAD',9,10),('WOODLAND_LINK',11,7)]
for name,x,y in points:
    move_to(x,y)
    assert text(ptr('sRegionMap')) == text(m.symbols['sMapName_'+name]), name
    if name in ('SNOW_TOWN','HOT_SPRINGS'):
        m.snap('quantum-'+name.lower())
# Previewing another page and cancelling retains the chosen island page.
move_to(21,11)
m.press(8)
m.press(4,30)
m.press(0)
assert selected_region()==2
move_to(21,11)
m.press(8)
m.press(4,30)
m.press(4,30)
m.press(8)
assert selected_region()==0
m.press(0)
m.press(0)
assert ptr('sRegionMap')==0

# Exercise future map-header location support independently of the new landing maps.
header=m.read(m.symbols['gMapHeader'],28)
# Enum values come from the actual generated order, keeping the old NONE stable.
entries=json.loads((m.root/'src/data/region_map/region_map_sections.json').read_text())['map_sections']
snow=next(i for i,e in enumerate(entries) if e['id']=='MAPSEC_QUANTUM_SNOW_TOWN')
m.write(m.symbols['gMapHeader']+20,bytes([snow]))
m.write(m.symbols['gMapHeader']+23,b'\x01') # MAP_TYPE_TOWN
native('InitRegionMapWithExitCB',0,m.symbols['CB2_ReturnToField']|1)
m.run(240)
assert selected_region()==2
assert struct.unpack('<hh',m.read(ptr('sMapCursor'),4))==(10,2)
assert text(ptr('sRegionMap'))==text(m.symbols['sMapName_SNOW_TOWN'])
m.snap('quantum-current-location')
m.write(m.symbols['gMapHeader'],header)
m.press(0)

native('CB2_OpenFlyMapWithExitCB',m.symbols['CB2_ReturnToField']|1)
m.run(240)
choose_quantum()
m.snap('quantum-fly-map')
m.press(8)
assert ptr('sRegionMap')!=0, 'Fly selected a town before its Center visit'
assert m.read(ptr('sFlyMap')+2,1)==b'\x00'
m.press(0)
assert ptr('sRegionMap')==0
print('Native island rendering, 14 location names, picker confirm/cancel, Kanto return, player-location cursor and unavailable Fly destinations passed')
