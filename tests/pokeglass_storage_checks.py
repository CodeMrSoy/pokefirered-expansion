"""Shared real-input checks; caller supplies the post-Oak three-mon fixture."""

def check_storage(m, native, wait_task, task_active, original):
    import struct
    injected_native = native
    def native(name, *args):
        # Test-only native calls must not replace the tablet's waiting script.
        context = m.read(m.symbols['sGlobalScriptContext'], 116)
        status = m.read(m.symbols['sGlobalScriptContextStatus'], 1)
        inject = m.inject
        def suspended_inject(script):
            # END intentionally tears down a real Pokeglass session. A native
            # test probe must suspend instead, then restore its waiting script.
            inject(script[:-2] + b'\x27' if script.endswith(b'\x6b\x02') else script)
        m.inject = suspended_inject
        try:
            result = injected_native(name, *args)
        finally:
            m.inject = inject
        m.write(m.symbols['sGlobalScriptContext'], context)
        m.write(m.symbols['sGlobalScriptContextStatus'], status)
        return result
    m.press(8)
    wait_task('Task_PokeGlassStorage')
    m.run(30)
    assert 'Task_PCMainMenu' not in m.symbols or not task_active('Task_PCMainMenu')
    if 'gStorage' in m.symbols:
        assert struct.unpack('<I', m.read(m.symbols['gStorage'], 4))[0] == 0
    box = struct.unpack('<I', m.read(m.symbols['gPokemonStoragePtr'], 4))[0]
    def party_count(n):
        assert m.read(m.symbols['gPlayerPartyCount'], 1) == bytes([n])
    def party_payload(slot):
        return m.read(m.symbols['gPlayerParty'] + slot * 100, 80)
    def box_payload(slot):
        return m.read(box + 4 + slot * 80, 80)
    m.snap('pokeglass-storage-six-boxes')
    # Pick party slot 0, deposit into first empty box slot; party compacts.
    m.press(8, 20); m.press(7, 20); m.press(8, 20)
    party_count(2)
    assert box_payload(0) == original[:80]
    assert party_payload(0) == original[100:180]
    # Withdraw to party slot 2, without opening a native PC screen.
    m.press(8, 20); m.press(6, 20); m.press(5, 20); m.press(5, 20); m.press(8, 20)
    party_count(3)
    assert party_payload(2) == original[:80]
    assert box_payload(0) == bytes(80)
    # Cancellation leaves both sides unchanged.
    before = m.read(m.symbols['gPlayerParty'], 600) + m.read(box, 14404)
    m.press(8, 20); m.press(0, 20)
    assert m.read(m.symbols['gPlayerParty'], 600) + m.read(box, 14404) == before
    # Release has a separate confirmation; B keeps the selected mon intact.
    m.press(8,20); m.press(2,20); m.press(0,20); m.press(0,20)
    assert m.read(m.symbols['gPlayerParty'], 600) + m.read(box, 14404) == before
    # Deposit party slot 2, then swap party slot 0 with that boxed mon.
    m.press(8, 20); m.press(7, 20); m.press(4, 20); m.press(4, 20); m.press(8, 20)
    m.press(6, 20); m.press(8, 20); m.press(7, 20); m.press(8, 20)
    party_count(2)
    assert party_payload(0) == original[:80]
    assert box_payload(0) == original[100:180]
    # Box switches wrap over precisely six boxes. Pages wrap over 30 slots.
    for _ in range(6): m.press(11, 20)
    for _ in range(5): m.press(3, 20)
    t = next(i for i in range(16) if struct.unpack('<I', m.read(m.symbols['gTasks']+40*i,4))[0] == m.symbols['Task_PokeGlassStorage'] | 1)
    data = m.symbols['gTasks'] + 40*t + 8
    assert struct.unpack('<hh', m.read(data, 4)) == (0, 0)
    # Give and take a real Bag item on a boxed mon, preserving its payload.
    assert native('AddBagItem', 13, 1) == 1  # Potion
    m.press(2, 20)
    assert struct.unpack('<h', m.read(data+18,2))[0] == 1
    m.snap('pokeglass-storage-held-items')
    m.press(8, 20)
    held = native('GetBoxMonData2', box + 4, 19)  # MON_DATA_HELD_ITEM
    assert held != 0
    # Fill the relevant pocket: a rejected Take must preserve the held item.
    pocket = native('GetPocketByItemId', held)
    record = m.symbols['gBagPockets'] + pocket*8
    items = struct.unpack('<I',m.read(record,4))[0]
    capacity = m.read(record+4,1)[0]
    bag_before = m.read(items,capacity*4)
    full = struct.pack('<HH',held,999)*capacity
    m.write(items,full)
    m.press(2,20)
    assert native('GetBoxMonData2',box+4,19) == held
    assert m.read(items,capacity*4) == full
    m.write(items,bag_before)
    m.press(2, 20)
    assert native('GetBoxMonData2', box + 4, 19) == 0
    assert box_payload(0) == original[100:180]
    # Restrict to one able party mon, then attempt a deposit into an empty slot.
    m.write(m.symbols['gPlayerParty'], original[:100] + bytes(500))
    m.write(m.symbols['gPlayerPartyCount'], b'\x01')
    m.press(6,20); m.press(8,20); m.press(7,20); m.press(5,20); m.press(8,20)
    party_count(1)
    assert party_payload(0) == original[:80]
    assert box_payload(1) == bytes(80)
    m.snap('pokeglass-storage-last-mon-protected')
    # The same protection applies to the explicit Release confirmation.
    m.press(2,20); m.press(8,20)
    party_count(1)
    assert party_payload(0) == original[:80]
    m.press(0,20); m.press(0,20)
    wait_task('Task_PokeGlassHub'); m.run(30); m.press(0)
    assert m.read(m.symbols['sGlobalScriptContextStatus'],1) == b'\x02'
    assert native('TrySavingData',0) == 1
    m.lib.retro_reset(); m.run(360); m.press(3); m.press(8,240); m.press(0,60)
    box = struct.unpack('<I', m.read(m.symbols['gPokemonStoragePtr'],4))[0]
    assert box_payload(0) == original[100:180]
    party_count(1)
    assert party_payload(0) == original[:80]
    # Release an actual boxed mon through the separate confirmation.
    m.press(3); wait_task('Task_PokeGlassHub'); m.run(30)
    m.press(7,20); m.press(7,20); m.press(8)
    wait_task('Task_PokeGlassStorage'); m.run(30)
    m.press(7,20); m.press(8,20); m.press(2,20); m.press(8,20)
    assert box_payload(0) == bytes(80)
    party_count(1)
    m.press(0,20); wait_task('Task_PokeGlassHub'); m.run(30); m.press(0)
    print('PASS native Pokeglass storage, shared window/no PC allocation, atomic deposits/withdrawals/swaps/cancel, six-box/page bounds, real held-item give/take, last-mon protection and flash reset/Continue', flush=True)
