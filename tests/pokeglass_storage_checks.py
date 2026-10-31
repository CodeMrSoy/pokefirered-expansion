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
    from collections import deque
    task = next(i for i in range(16) if struct.unpack('<I',m.read(m.symbols['gTasks']+40*i,4))[0] == (m.symbols['Task_PokeGlassStorage']|1))
    data = m.symbols['gTasks'] + 40*task + 8
    def next_cursor(cursor,key):
        party = cursor < 6
        slot = cursor if party else cursor-6
        if key==4:return (cursor+4)%6 if party else 6+(slot+24)%30
        if key==5:return (cursor+2)%6 if party else 6+(slot+6)%30
        if key==6:return (cursor-1 if cursor%2 else 6+cursor//2*12+5) if party else (cursor-1 if slot%6 else min(slot//6//2,2)*2+1)
        return (6+cursor//2*12 if cursor%2 else cursor+1) if party else (cursor+1 if slot%6<5 else min(slot//6//2,2)*2)
    def cursor_to(target):
        current=struct.unpack('<h',m.read(data+4,2))[0]
        queue=deque([(current,[])])
        visited={current}
        while queue:
            cursor,path=queue.popleft()
            if cursor==target:
                for key in path:m.press(key,25)
                assert struct.unpack('<h',m.read(data+4,2))[0]==target
                return
            for key in [4,5,6,7]:
                following=next_cursor(cursor,key)
                if following not in visited:visited.add(following);queue.append((following,path+[key]))
        raise AssertionError(('Unreachable PC slot',target))
    def confirm_at(target):cursor_to(target);m.press(8,30)
    icons=struct.unpack('<I',m.read(m.symbols['sGlassStorageIcons'],4))[0]
    assert icons and sum(i<64 for i in m.read(icons,36))==3
    m.snap('pokeglass-storage-six-boxes')
    m.press(3,30);assert struct.unpack('<h',m.read(data+18,2))[0]==3
    m.snap('pokeglass-storage-inspect');m.press(0,30)
    assert struct.unpack('<h',m.read(data+18,2))[0]==0
    confirm_at(0);confirm_at(6)
    party_count(2);assert box_payload(0)==original[:80]
    confirm_at(6);confirm_at(2)
    party_count(3);assert box_payload(0)==bytes(80)
    assert party_payload(2)==original[:80]
    before=m.read(m.symbols['gPlayerParty'],600)+m.read(box,14864)
    confirm_at(0);m.press(0,30)
    assert before==m.read(m.symbols['gPlayerParty'],600)+m.read(box,14864)
    confirm_at(2);confirm_at(6)
    confirm_at(0);confirm_at(6)
    assert party_payload(0)==original[:80] and box_payload(0)==original[100:180]
    for _ in range(6):m.press(11,30)
    assert struct.unpack('<h',m.read(data,2))[0]==0
    for slot in range(36):cursor_to(slot)
    cursor_to(6)
    assert native('AddBagItem',13,1)==1
    m.press(2,30);m.snap('pokeglass-storage-held-items');m.press(8,30)
    held=native('GetBoxMonData2',box+4,19);assert held
    pocket=native('GetPocketByItemId',held);record=m.symbols['gBagPockets']+pocket*8
    items=struct.unpack('<I',m.read(record,4))[0];capacity=m.read(record+4,1)[0]
    bag_before=m.read(items,capacity*4);full=struct.pack('<HH',held,999)*capacity
    m.write(items,full);m.press(2,30)
    assert native('GetBoxMonData2',box+4,19)==held and m.read(items,capacity*4)==full
    m.write(items,bag_before);m.press(2,30)
    assert box_payload(0)==original[100:180]
    m.write(m.symbols['gPlayerParty'],original[:100]+bytes(500));m.write(m.symbols['gPlayerPartyCount'],b'\x01')
    confirm_at(0);confirm_at(7)
    party_count(1);assert box_payload(1)==bytes(80)
    m.press(2,30);m.press(8,30)
    party_count(1);assert party_payload(0)==original[:80]
    m.press(0,30);m.press(0,30);wait_task('Task_PokeGlassHub');m.run(40)
    assert m.read(m.symbols['sGlassStorageIcons'],4)==bytes(4)
    m.press(0)
    assert native('TrySavingData',0)==1
    m.lib.retro_reset();m.run(360);m.press(3);m.press(8,240);m.press(0,60)
    box=struct.unpack('<I',m.read(m.symbols['gPokemonStoragePtr'],4))[0]
    assert box_payload(0)==original[100:180] and party_payload(0)==original[:80]
    print('PASS 36-slot sprite PC navigation, atomic moves/swaps/cancel, held items/full Bag, last-mon and release guards, resource cleanup and flash Continue',flush=True)
