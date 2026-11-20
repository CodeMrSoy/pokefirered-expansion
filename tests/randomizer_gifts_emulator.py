"""Exercise compiled gift commands, previews, storage, and independent toggles."""
import pathlib
import re
import struct

setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))

def inject_done(blob):
    address = m.symbols['gDecompressionBuffer']
    m.write(address, blob)
    context = m.symbols['sGlobalScriptContext']
    m.write(context, b'\x00\x01\x00\x00')
    m.write(context + 8, struct.pack('<I', address))
    m.write(m.symbols['sGlobalScriptContextStatus'], b'\x00')
    for _ in range(300):
        m.run(1)
        if m.read(m.symbols['sGlobalScriptContextStatus'], 1) == b'\x02':
            return
    raise AssertionError('Gift test script did not finish')

m.inject = inject_done
rom = (m.root / 'pokefirered.gba').read_bytes()
grant_prefix = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_givegiftmon'] | 1) + 0x02000000)

def grant_command(label):
    start = m.symbols[label] - 0x08000000
    offset = rom.index(grant_prefix, start, start + 160)
    command = rom[offset:offset + 15]
    assert command[5:7] == b'\x00\x06'
    assert struct.unpack_from('<H', command, 7)[0] == 0x4001
    return command

rewards = [
    (129, 'Route4_PokemonCenter_1F_EventScript_TryBuyMagikarp', 5),
    (133, 'CeladonCity_Condominiums_RoofRoom_EventScript_EeveeBall', 25),
    (106, 'SaffronCity_Dojo_EventScript_GiveHitmon', 25),
    (107, 'SaffronCity_Dojo_EventScript_GiveHitmon', 25),
    (131, 'SilphCo_7F_EventScript_LaprasGuy', 25),
    (138, 'CinnabarIsland_PokemonLab_ExperimentRoom_EventScript_GiveOmanyte', 5),
    (140, 'CinnabarIsland_PokemonLab_ExperimentRoom_EventScript_GiveKabuto', 5),
    (142, 'CinnabarIsland_PokemonLab_ExperimentRoom_EventScript_GiveAerodactyl', 5),
    (63, 'CeladonCity_GameCorner_PrizeRoom_EventScript_GiveAbra', 9),
    (35, 'CeladonCity_GameCorner_PrizeRoom_EventScript_GiveClefairy', 8),
    (147, 'CeladonCity_GameCorner_PrizeRoom_EventScript_GiveDratini', 18),
    (123, 'CeladonCity_GameCorner_PrizeRoom_EventScript_GiveScyther', 25),
    (137, 'CeladonCity_GameCorner_PrizeRoom_EventScript_GivePorygon', 26),
    (127, 'CeladonCity_GameCorner_PrizeRoom_EventScript_GivePinsir', 18),
]
commands = {label: grant_command(label) for _, label, _ in rewards}
party = m.symbols['gPlayerParty']
save = struct.unpack('<I', m.read(m.symbols['gSaveBlock2Ptr'], 4))[0]
table = struct.unpack('<11H', m.read(m.symbols['gStarterAndGiftMonTable'], 22))
baseline = {}
changed = 0
fields = re.findall(r'\bMON_DATA_\w+', (m.root / 'include/pokemon.h').read_text().split('// Property labels')[1].split('};')[0])
species_field, level_field = fields.index('MON_DATA_SPECIES'), fields.index('MON_DATA_LEVEL')
for mode in (0, 1):
    native('AdventureMode_SelectNewGame', mode); native('AdventureMode_NewGame')
    for seed in (0x13579BDF, 0x2468ACE0):
        m.write(save + 3756, struct.pack('<I', seed))
        for bits in (0, 2, 4, 1, 7):
            native('GameModes_Set', 0x7F, 0); native('GameModes_Set', bits, 1)
            for original, label, level in rewards:
                m.write(party, bytes(600)); m.write(m.symbols['gPlayerPartyCount'], b'\0')
                expected = native('RandomizeGiftSpecies', original)
                if not bits & 1:
                    assert expected == original, 'Moves/abilities alone randomized a gift species'
                else:
                    assert 0 < expected < 0xFFFF
                    changed += expected != original
                    key = (seed, original)
                    assert baseline.setdefault(key, expected) == expected, 'Mode/toggle changed gift mapping'
                    if original in table:
                        old = native('RandomizeStarterAndGiftMon', table.index(original), m.symbols['gStarterAndGiftMonTable'], 11)
                        assert expected == native('QuantumCanonicalSpecies', old), 'Existing seed mapping changed'
                native('VarSet', 0x4001, original)
                # Preview buffer must agree, without consuming or rewriting the source.
                preview = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_buffergiftname'] | 1) + 0x02000000)
                m.inject(preview + struct.pack('<BH', 0, 0x4001) + b'\x02')
                assert native('VarGet', 0x4001) == original
                before = m.read(m.symbols['gStringVar1'], 13)
                m.inject(commands[label] + b'\x02')
                assert m.read(m.symbols['gPlayerPartyCount'], 1) == b'\x01'
                actual = native('GetMonData3', party, species_field, 0)
                assert actual == expected, (mode, hex(seed), bits, original, expected, actual)
                assert native('GetMonData3', party, level_field, 0) == level
                assert native('VarGet', 0x4001) == expected
                # Plain species-name buffering after receipt must match its preview.
                m.inject(b'\x7d' + struct.pack('<BH', 0, 0x4001) + b'\x02')
                assert m.read(m.symbols['gStringVar1'], 13) == before

assert changed > 0
# A full party sends the same mapped species to PC without replacing a member.
native('GameModes_Set', 1, 1)
m.write(party, m.read(party, 100) * 6); m.write(m.symbols['gPlayerPartyCount'], b'\x06')
storage = struct.unpack('<I', m.read(m.symbols['gPokemonStoragePtr'], 4))[0]
box_count = int(re.search(r'#define TOTAL_BOXES_COUNT\s+(\d+)', (m.root / 'include/pokemon_storage_system.h').read_text()).group(1))
m.write(storage + 4, bytes(box_count * 30 * 80))
native('VarSet', 0x4001, 133)
expected = native('RandomizeGiftSpecies', 133)
before = m.read(party, 600)
m.inject(commands[rewards[1][1]] + b'\x02')
assert native('GetBoxMonData3', storage + 4, species_field, 0) == expected
assert m.read(party, 600) == before
# With party and storage full, report failure without overwriting any Pokémon.
m.write(storage + 4, m.read(party, 80) * (box_count * 30))
boxes = m.read(storage + 4, box_count * 30 * 80)
native('VarSet', 0x4001, 133)
m.inject(commands[rewards[1][1]] + b'\x02')
assert native('VarGet', 0x800D) == 2
assert m.read(party, 600) == before
after_boxes = m.read(storage + 4, len(boxes))
assert after_boxes == boxes, [(i, a, b) for i, (a, b) in enumerate(zip(boxes, after_boxes)) if a != b][:20]
print('PASS both adventures; 2 seeds; independent species/moves/ability toggles; 14 compiled gift/prize grants; matching previews/names; stable starter mappings; PC delivery and full-storage failure')
