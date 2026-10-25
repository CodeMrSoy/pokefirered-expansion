# Terrace canopy and roof ordering

Havora's cliff terraces use physical elevations 4 and 6 (and other even heights).
FireRed interprets those values as an above-canopy bridge priority. People could
therefore appear in front of walkable tree tips and the rear edges of roofs.

Objects on the shared Havora city tileset's even terraces now use ordinary ground
sprite priority and subsprite ordering. Physical elevation, collision, map blocks,
cliffs, metatile IDs, graphics, events and connections are unchanged. The override
respects explicitly fixed sprite priorities, excludes ordinary dock elevation 2,
and does not affect other tilesets or native bridge behavior.

The development ROM compiled. `havora_occlusion_emulator.py` exercises actual tree
and roof overlap at elevations 4/6, unchanged physical elevation, harbor deck and
Kanto priorities. Its comparison reproduces the old sprite priority only in the
test fixture; the right panels show the corrected ROM. The full 37-action maze,
gate animation/collision, persistence, reset and fallback checks also pass.
