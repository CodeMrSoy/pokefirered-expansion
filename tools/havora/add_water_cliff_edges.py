#!/usr/bin/env python3
"""Add animated-water cliff edges to both Havora outdoor tileset pairs.

The harbor atlas is at the normal GBA tile limit. This adds four corner/edge
orientations by reusing the existing city cliff-face overlay, the animated
water base, and four unallocated harbor graphic slots. It leaves all authored
maps, events, warps, connections, and existing Harbor art untouched.
"""
from __future__ import annotations

import json
import struct
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WATER_META = 0x282
# General 0x036 is the one-sided cliff edge with transparent quadrants, so
# its cliff graphic can sit over the animated water instead of hiding it.
CLIFF_FACE_META = 0x036
FLIPS = {"water_cliff": 0, "water_cliff_h": 0x400,
         "water_cliff_v": 0x800, "water_cliff_hv": 0xC00}
ATTRIBUTE_FLIPS = {
    "water_cliff": (0, 1, 2, 3),
    "water_cliff_h": (1, 0, 3, 2),
    "water_cliff_v": (2, 3, 0, 1),
    "water_cliff_hv": (3, 2, 1, 0),
}


def words(path: Path) -> list[int]:
    data = path.read_bytes()
    return list(struct.unpack("<" + "H" * (len(data) // 2), data))


def packed(values: list[int]) -> bytes:
    return struct.pack("<" + "H" * len(values), *values)


def get_tile(sheet: Image.Image, tile_id: int) -> Image.Image:
    x, y = tile_id % 16 * 8, tile_id // 16 * 8
    return sheet.crop((x, y, x + 8, y + 8))


def first_empty_meta(meta: list[int], attrs: bytes) -> int:
    for i in range(640):
        if not any(meta[i * 8:(i + 1) * 8]) and not any(attrs[i * 4:(i + 1) * 4]):
            return i
    raise RuntimeError("No blank primary metatile slots remain.")


def add_variants(label: str, directory: str, water: list[int], wall: list[int],
                 water_attrs: bytes, wall_attrs: bytes,
                 source_tiles: Image.Image | None = None,
                 target_tiles: Image.Image | None = None,
                 graphic_slots: list[int] | None = None,
                 target_tiles_path: Path | None = None,
                 target_tile_offset: int = 0) -> dict[str, int]:
    base = ROOT / f"data/tilesets/primary/{directory}"
    meta_path = base / "metatiles.bin"
    attr_path = base / "metatile_attributes.bin"
    meta = words(meta_path)
    attrs = bytearray(attr_path.read_bytes())
    tiles_path = base / "tiles.png" if target_tiles_path is None else target_tiles_path
    tiles = Image.open(tiles_path).copy() if target_tiles is None else target_tiles
    wall_overlay = list(wall[4:8])
    if source_tiles is not None:
        assert graphic_slots is not None and len(graphic_slots) == 4
        source_graphics = list(dict.fromkeys(word & 0x3FF for word in wall_overlay))
        graphic_map = {old: graphic_slots[i]
                       for i, old in enumerate(source_graphics)}
        for old, new in graphic_map.items():
            target = new - target_tile_offset
            tiles.paste(get_tile(source_tiles, old), (target % 16 * 8, target // 16 * 8))
        wall_overlay = [(word & ~0x3FF) | graphic_map[word & 0x3FF]
                        for word in wall_overlay]

    result: dict[str, int] = {}
    for name, flip in FLIPS.items():
        mid = first_empty_meta(meta, bytes(attrs))
        entries = list(water[:4]) + [word ^ flip for word in wall_overlay]
        meta[mid * 8:(mid + 1) * 8] = entries
        order = ATTRIBUTE_FLIPS[name]
        # Preserve cliff collision where the cliff occupies a quadrant, and
        # use the native water behavior for the exposed animated-water area.
        merged_attrs = bytes(wall_attrs[i] if wall_attrs[i] else water_attrs[i]
                             for i in range(4))
        attrs[mid * 4:(mid + 1) * 4] = bytes(merged_attrs[i] for i in order)
        result[name] = mid
    meta_path.write_bytes(packed(meta))
    attr_path.write_bytes(attrs)
    if source_tiles is not None:
        tiles.save(tiles_path)
    return result


def main() -> None:
    manifest_path = ROOT / "tools/havora/cliff-tiles.json"
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text())
        if "city_water_cliff_variants" in existing and "harbor_water_cliff_variants" in existing:
            print(json.dumps(existing, indent=2))
            return
    city_p = ROOT / "data/tilesets/primary/havora_city"
    harbor_p = ROOT / "data/tilesets/primary/havora_harbor"
    city_s = ROOT / "data/tilesets/secondary/havora_city"
    harbor_s = ROOT / "data/tilesets/secondary/havora_harbor"
    city_p_meta, city_attrs = words(city_p / "metatiles.bin"), \
        (city_p / "metatile_attributes.bin").read_bytes()
    city_s_meta = words(city_s / "metatiles.bin")
    harbor_s_meta = words(harbor_s / "metatiles.bin")
    city_water = city_s_meta[(WATER_META - 640) * 8:(WATER_META - 639) * 8]
    harbor_water = harbor_s_meta[(WATER_META - 640) * 8:(WATER_META - 639) * 8]
    city_water_attrs = (city_s / "metatile_attributes.bin").read_bytes()[
        (WATER_META - 640) * 4:(WATER_META - 639) * 4]
    harbor_water_attrs = (harbor_s / "metatile_attributes.bin").read_bytes()[
        (WATER_META - 640) * 4:(WATER_META - 639) * 4]
    assert city_water == harbor_water
    assert all((word & 0x3FF) >= 896 for word in city_water[:4]), \
        "Havora water floor does not use the animated tile range."

    wall = city_p_meta[CLIFF_FACE_META * 8:(CLIFF_FACE_META + 1) * 8]
    assert all((word & 0x3FF) == 8 for word in wall[:4]), \
        "Shared city cliff face is not an alpha overlay."
    wall_attrs = city_attrs[CLIFF_FACE_META * 4:(CLIFF_FACE_META + 1) * 4]

    city_variants = add_variants("city", "havora_city", city_water, wall,
                                 city_water_attrs, wall_attrs)

    # These tiles are unused by all Harbor metatiles and are outside the
    # primary General animation destinations. Keep all existing Harbor art.
    harbor_meta = words(harbor_p / "metatiles.bin")
    harbor_secondary_all = words(harbor_s / "metatiles.bin")
    harbor_attrs = (harbor_p / "metatile_attributes.bin").read_bytes()
    used_graphics = {word & 0x3FF for sheet in (harbor_meta, harbor_secondary_all)
                     for word in sheet if (word & 0x3FF) < 896}
    free_graphics = [i for i in range(640, 896) if i not in used_graphics]
    assert len(free_graphics) >= 4, "Harbor has fewer than four safe graphic slots."

    harbor_variants = add_variants(
        "harbor", "havora_harbor", harbor_water, wall,
        harbor_water_attrs, wall_attrs,
        source_tiles=Image.open(city_p / "tiles.png"),
        target_tiles=Image.open(harbor_s / "tiles.png").copy(),
        graphic_slots=free_graphics[:4],
        target_tiles_path=harbor_s / "tiles.png", target_tile_offset=640)

    city_cliff_sources = json.loads(
        (ROOT / "tools/havora/city-tileset.json").read_text())["native_general_ids"]
    city_cliff_sources = {f"0x{int(source):03X}": dest
                          for source, dest in city_cliff_sources.items()
                          if 0x68 <= int(source) <= 0xAF}
    manifest = {
        "city_primary_tileset": "gTileset_HavoraCityPrimary",
        "harbor_primary_tileset": "gTileset_HavoraPrimary",
        "animated_water_graphic_tile_ids": [896, 1023],
        "source_water_cliff_edge_metatile": CLIFF_FACE_META,
        "city_fire_red_cliff_metatiles": city_cliff_sources,
        "city_water_cliff_variants": city_variants,
        "harbor_water_cliff_variants": harbor_variants,
        "harbor_graphic_tiles_added": free_graphics[:len(set(
            word & 0x3FF for word in wall[4:8]))],
        "behavior": "Water underlay uses the animated Havora water tile range; cliff overlay stays impassable.",
        "harbor_note": "The harbor atlas is nearly full; its new water-cliff pieces use four free graphic tiles. The complete regular cliff catalog remains on HavoraCityPrimary.",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
