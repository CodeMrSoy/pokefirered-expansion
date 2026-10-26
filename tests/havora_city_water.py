"""Actual city tileset DMA animation at the city/harbor boundary."""
import struct,json
import havora_emulator_support as m
m.inject(b'\x39'+struct.pack('<BBBHH',43, 14,255,23,63)+b'\x6b\x02');m.run(240)
callback=struct.unpack('<I',m.read(m.symbols['sSecondaryTilesetAnimCallback'],4))[0]
assert callback&~1==m.symbols['TilesetAnim_Havora_Harbor']&~1
frames=[];screens=[]
for _ in range(8):
 m.run(16);frames.append(m.read(0x06000000+896*32,128*32));screens.append(m.screen.tobytes())
m.snap('terrace-city-harbor-seam')
assert len(set(frames))==8 and len(set(screens))==8,(len(set(frames)),len(set(screens)))
print('PASS: city callback and eight animated sea phases in actual VRAM and gameplay at the harbor boundary',flush=True)
