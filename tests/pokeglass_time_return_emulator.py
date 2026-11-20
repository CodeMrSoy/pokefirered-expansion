"""Party's fast return must preserve field lighting without accumulating tint."""
import json, pathlib, struct
setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))

fixture = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_givegiftmon'] | 1) + 0x02000000)
fixture += struct.pack('<BBHHI', 0, 6, 25, 25, 0)
fixture += b'\x29' + struct.pack('<H', 0x829)
fixture += b'\x44' + struct.pack('<HH', 717, 1) + b'\x02'
m.inject(fixture)

def palette():
    # Map palettes, excluding tablet/dialogue slots 13..15.
    return m.read(m.symbols['gPlttBufferFaded'], 13 * 32)

groups = json.loads((m.root / 'data/maps/map_groups.json').read_text())
rain_group = next(i for i, key in enumerate(groups['group_order']) if 'VidraDraft_RainfallRoute' in groups[key])
rain_map = groups[groups['group_order'][rain_group]].index('VidraDraft_RainfallRoute')
for place, warp, hours in [('viridian', (3, 1, 30, 24), (12, 22, 19)),
                           ('bedroom', (4, 1, 6, 6), (12, 22, 19)),
                           ('rainfall', (rain_group, rain_map, 12, 10), (22,))]:
    group, number, x, y = warp
    m.inject(b'\x39' + struct.pack('<BBBHH', group, number, 255, x, y) + b'\x6b\x02')
    m.run(300)
    for hour in hours:
        m.write(m.symbols['sHoursOverride'], bytes([hour]))
        native('UpdateTimeOfDay')
        native('ApplyWeatherColorMapToPals', 0, 16)
        native('ApplyWeatherColorMapToPals', 16, 16)
        m.run(60)
        before = palette()
        m.snap(f'time-{place}-{hour}-before')
        for cycle in range(2):
            m.write(m.symbols['sHubCursor'], b'\0')
            m.press(3); m.press(7); m.press(8)
            m.snap(f'time-{place}-{hour}-party-{cycle}')
            assert struct.unpack('<I', m.read(m.symbols['gMain'] + 4, 4))[0] == m.symbols['CB2_UpdatePartyMenu'] | 1, (place, hour, cycle, m.read(m.symbols['gPlayerPartyCount'], 1))
            m.press(0, 240)
            m.snap(f'time-{place}-{hour}-hub-{cycle}')
            # Both the glass backdrop and the field underneath need the tint.
            assert palette() == before, (place, hour, cycle, 'Party return changed map lighting', [i for i in range(13) if palette()[i*32:(i+1)*32] != before[i*32:(i+1)*32]])
            m.press(0, 180)
            assert palette() == before, (place, hour, cycle, 'Closing glass changed map lighting')
            m.snap(f'time-{place}-{hour}-after-{cycle}')
        print('PASS', place, hour, 'two Party returns preserve field colors', flush=True)
print('PASS day/night/evening, outdoor/indoor/rain, repeated Party/hub/field transitions')
