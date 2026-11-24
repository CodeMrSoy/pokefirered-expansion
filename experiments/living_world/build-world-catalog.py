"""Extract an offline catalog from the exact linked GBA ROM and its ELF."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from struct import Struct, unpack_from
import subprocess

from world_manifest import digest, encoded
from world_rules import CENTERS, MARTS, KANTO_GYMS, CLASSIC_CAPS, QUANTUM_CAPS, RESERVED_CRESTS

ROOT = Path(__file__).resolve().parents[2]
ROM_BASE = 0x08000000
COUNTS = (12, 5, 5, 10, 3)
METHODS = ("land", "surf", "rock_smash", "fishing", "hidden")
RODS = ("old",) * 2 + ("good",) * 3 + ("super",) * 5


class LinkedRom:
    def __init__(self, rom, elf, nm):
        self.rom = rom.read_bytes()
        exe = elf.read_bytes()
        if exe[:7] != b"\x7fELF\x01\x01\x01" or unpack_from("<H", exe, 18)[0] != 40:
            raise ValueError("Expected a little-endian ARM ELF")
        header = unpack_from("<16sHHIIIIIHHHHHH", exe)
        program_table, entry_size, count = header[5], header[9], header[10]
        if entry_size != 32 or count > 64:
            raise ValueError("Invalid ELF program headers")
        compared = 0
        for i in range(count):
            kind, offset, _, physical, size, *_ = unpack_from("<8I", exe, program_table + i * entry_size)
            if kind == 1 and size and physical >= ROM_BASE:
                start = max(0, 192 + ROM_BASE - physical)
                if self.read(physical + start, size - start) != exe[offset + start:offset + size]:
                    raise ValueError("ROM bytes differ from the linked ELF")
                compared += size - start
        if compared < 1024 or self.rom[0xAC:0xB0] != b"BPRE":
            raise ValueError("Expected the compiled FireRed image")
        self.symbols = {}
        self.labels = {}
        for row in subprocess.check_output([nm, "-S", str(elf)], text=True).splitlines():
            fields = row.split()
            if len(fields) in (3, 4):
                address, size, name = int(fields[0], 16), int(fields[1], 16) if len(fields) == 4 else 0, fields[-1]
                self.symbols[name] = (address, size)
                self.labels.setdefault(address, []).append(name)

    def read(self, address, size):
        start = address - ROM_BASE
        if size < 0 or start < 0 or start + size > len(self.rom):
            raise ValueError(f"Invalid ROM range 0x{address:08x}+{size}")
        return self.rom[start:start + size]

    def unpack(self, fmt, address):
        packing = Struct("<" + fmt)
        return packing.unpack(self.read(address, packing.size))

    def value(self, fmt, address):
        return self.unpack(fmt, address)[0]

    def address(self, name):
        return self.symbols[name][0]


def script_binding(rom, ptr):
    """Decode a bounded compiled prefix and retain conditional fallthrough predicates."""
    visited = set()
    branches = []
    for _ in range(20):
        if not ROM_BASE <= ptr < ROM_BASE + len(rom.rom) or ptr in visited:
            break
        visited.add(ptr)
        op = rom.value("B", ptr)
        if op in (0x00, 0x5A, 0x69, 0x6A):
            ptr += 1
        elif op == 0x05:
            ptr = rom.value("I", ptr + 1)
        elif op in (0x25, 0x26, 0x21, 0x22, 0x16):
            ptr += {0x25: 3, 0x26: 5, 0x21: 5, 0x22: 5, 0x16: 5}[op]
        elif op == 0x06:
            condition, target = rom.unpack("BI", ptr + 1)
            branches.append(dict(address=ptr, condition=condition, alternate=target, assumed="fallthrough"))
            ptr += 6
        elif op == 0x5C:
            flags, local, trainer = rom.unpack("BBH", ptr + 1)
            return dict(status="conditional", opcode=op, address=ptr, trainer=trainer,
                        battle_script_mode=flags, trainer_local=local, branches=branches)
        elif op == 0xB6:
            a, l1, i1, b, l2, i2 = rom.unpack("HBHHBH", ptr + 1)
            return dict(status="conditional", opcode=op, address=ptr,
                        branches=branches, party=[dict(species=x, level=l, held_item=i) for x, l, i in ((a,l1,i1),(b,l2,i2)) if x])
        else:
            break
    return dict(status="deferred_to_gameplay", reason="script_prefix_unsupported")


def catalog_maps(rom, layout):
    counts = rom.read(rom.address("gWorldMapCounts"), layout["map_groups"])
    maps = []
    for group, count in enumerate(counts):
        base = rom.value("I", rom.address("gMapGroups") + 4 * group)
        for number in range(count):
            address = rom.value("I", base + 4 * number)
            _, events, script, connections, _, layout_id, section, _, _, map_type = rom.unpack("IIIIHHBBBB", address)
            name = next((s for s in rom.labels.get(address, ()) if not s.startswith((".", "$"))), None)
            if not name:
                raise ValueError(f"Unlabeled map {group}:{number}")
            warps, edges, objects = [], [], []
            if events:
                object_count, warp_count, _, _, object_ptr, warp_ptr = rom.unpack("4B2I", events)
                for i in range(warp_count):
                    x, y, z, warp, target, target_group = rom.unpack("hh4B", warp_ptr + 8 * i)
                    warps.append(dict(x=x, y=y, elevation=z, destination_warp=warp,
                                      target=[target_group, target], status="conditional"))
                for i in range(object_count):
                    obj = object_ptr + i * layout["object_size"]
                    local = rom.value("B", obj + layout["object_local"])
                    hook = rom.value("I", obj + layout["object_script"])
                    x, y = (rom.value("h", obj + layout["object_" + k]) for k in ("x", "y"))
                    graphics = rom.value("H", obj + layout["object_graphics"])
                    kind = rom.value("B", obj + 3)
                    flag = rom.value("H", obj + layout["object_script"] + 4)
                    binding = script_binding(rom, hook) if hook and kind == 0 else None
                    objects.append(dict(local=local, coordinates=[x,y], graphics=graphics, kind=kind, flag=flag,
                                        script=hook, labels=rom.labels.get(hook, []) if hook else [], binding=binding,
                                        status="conditional"))
            if connections:
                length, ptr = rom.unpack("iI", connections)
                if not 0 <= length <= 256:
                    raise ValueError("Invalid map connections")
                for i in range(length):
                    direction, offset, g, n = rom.unpack("B3xi2B", ptr + 12 * i)
                    edges.append(dict(direction=direction, offset=offset, target=[g,n], status="conditional"))
            maps.append(dict(id=[group,number], name=name, section=section, layout=layout_id, map_type=map_type,
                             address=address, script=script, warps=warps, connections=edges, objects=objects,
                             access=dict(status="conditional", vidra_section=section >= layout["vidra_section"],
                                         reason="native_flags_tools_scripts_and_mode")))
    return maps


def catalog_encounters(rom, layout):
    weights = rom.read(rom.address("gWorldEncounterWeights"), 60)
    base, size = rom.symbols["gWildMonHeaders"]
    records = []
    row_size = layout["wild_size"]
    for index in range(size // row_size):
        address = base + index * row_size
        group, number = rom.unpack("BB", address)
        if group == 0xFF:
            break
        for variant in range(layout["wild_variants"]):
            array = address + layout["wild_types"] + variant * 20
            for method, label in enumerate(METHODS):
                pointer = rom.value("I", array + 4 * method)
                if not pointer:
                    continue
                rate = rom.value("B", pointer)
                mons = rom.value("I", pointer + layout["wild_info_mons"])
                slots = []
                for slot in range(COUNTS[method]):
                    low, high, species = rom.unpack("BBH", mons + 4 * slot)
                    slots.append(dict(slot=slot, species=species, level=[low,high],
                                      weight=None if method == 4 else weights[12*method+slot],
                                      rod=RODS[slot] if method == 3 else None))
                records.append(dict(header=index, map=[group,number], variant=variant, method=method, kind=label,
                                    table=rom.labels.get(pointer, []), rate=rate, slots=slots,
                                    status="conditional", reason="native_availability_and_variant_selection"))
    else:
        raise ValueError("Encounter header sentinel missing")
    return records


def terminated(rom, pointer, width, fmt, sentinel, limit):
    if not pointer:
        return []
    rows = []
    for i in range(limit):
        record = rom.unpack(fmt, pointer + width * i)
        if record[0] == sentinel:
            return rows
        rows.append(record)
    raise ValueError(f"Unterminated ROM records at {pointer:#x}")


def catalog_species(rom, layout):
    base, total = rom.symbols["gSpeciesInfo"]
    width = layout["species_size"]
    if total < width * layout["species_count"]:
        raise ValueError("Species metadata outside compiled table")
    species = []
    for id_ in range(1, layout["species_count"]):
        address = base + id_ * width
        stats = list(rom.read(address, 6))
        evos = []
        for row in terminated(rom, rom.value("I", address + layout["species_evolutions"]),
                              layout["evolution_size"], "HHH", 0xFFFF, 80):
            off = rom.value("I", address + layout["species_evolutions"])
            params = rom.value("I", off + len(evos) * layout["evolution_size"] + layout["evolution_params"])
            evos.append(dict(method=row[0], parameter=row[1], target=row[2],
                             conditions=terminated(rom, params, 8, "4H", layout["evolution_param_end"], 48)))
        forms = rom.value("I", address + layout["species_forms"])
        species.append(dict(id=id_, status="authored", enabled=bool(stats[0]), stats=stats, types=list(rom.read(address+6,2)),
                            catch_rate=rom.value("B",address+8),
                            name_bytes=rom.read(address+layout["species_name"],layout["species_name_size"]).hex(),
                            held_items=rom.unpack("HH",address+layout["species_items"]),
                            abilities=rom.unpack(str(layout["ability_count"])+"H", address+layout["species_abilities"]),
                            evolutions=evos, forms=rom.labels.get(forms, []) if forms else [],
                            learnset=terminated(rom, rom.value("I", address+layout["species_learnset"]),
                                                4, "HH", layout["learnset_end"], 256)))
    return species


def ecology_protection(rom, layout):
    # ABI v1 packs the species flags immediately before the four shadow
    # bytes and the learnset pointer. Fail closed if a build changes layout.
    base = rom.address("gSpeciesInfo")
    width = layout["species_size"]
    offset = layout["species_learnset"] - 8
    def flags(species):
        return rom.value("H", base + species * width + offset)
    expected = {1: 0, 150: 1, 151: 2, 803: 4, 906: 32, 1380: 8}
    if any(flags(species) & 0x3f != value for species, value in expected.items()):
        raise ValueError("Unsupported species flags layout for ecology safety")
    # Legendary, mythical, Ultra Beast, Paradox and temporary battle forms.
    return [species for species in range(1, layout["species_count"]) if flags(species) & 0x43ff]


def catalog_trainers(rom, layout):
    base = rom.value("I", rom.address("gTrainers") + 4 * layout["difficulty"])
    names = {}
    for name, id_ in re.findall(r"^#define\s+(TRAINER_\w+)\s+(\d+)\s*$",
                                (ROOT / "include/constants/opponents.h").read_text(), re.M):
        names.setdefault(int(id_), name)
    trainers = []
    for id_ in range(1, layout["trainers_count"]):
        address = base + id_ * layout["trainer_size"]
        ptr = rom.value("I",address+layout["trainer_party"])
        count = rom.value("B",address+layout["trainer_party_size"])
        pool = rom.value("B",address+layout["trainer_pool_size"])
        if not ptr or not count:
            continue
        battle_type = rom.value("B",address+layout["trainer_pool_size"]-3) & 3
        entries = []
        for slot in range(pool or count):
            row = ptr + slot * layout["trainer_mon_size"]
            species, item, ability = rom.unpack("3H",row+layout["trainer_mon_species"])
            ev = rom.value("I",row+layout["trainer_mon_ev"])
            entries.append(dict(slot=slot, species=species, held_item=item, ability=ability,
                                moves=rom.unpack("4H",row+layout["trainer_mon_moves"]),
                                level=rom.value("B",row+layout["trainer_mon_level"]),
                                nature=rom.value("B",row+layout["trainer_nature_byte"]) & 31,
                                iv_word=rom.value("I",row+layout["trainer_mon_iv"]),
                                evs=list(rom.read(ev,6)) if ev else None))
        trainers.append(dict(id=id_, address=address, symbol=names.get(id_), difficulty=layout["difficulty"],
                             battle_type=battle_type, ai_flags=rom.value("Q",address), party_count=count,
                             pool_size=pool, trainer_class=rom.value("B",address+layout["trainer_class"]),
                             status="authored", party=entries))
    return trainers


def build_catalog(rom_path, elf_path, nm, revision):
    rom = LinkedRom(rom_path, elf_path, nm)
    fields = re.findall(r"^WORLD_LAYOUT\((\w+),", (ROOT/"include/world_catalog_layout.inc").read_text(), re.M)
    address, size = rom.symbols["gWorldCatalogLayout"]
    if size != 4 * len(fields):
        raise ValueError("Catalog ABI size mismatch")
    layout = dict(zip(fields, rom.unpack(str(len(fields))+"I",address)))
    if layout["abi"] != 1:
        raise ValueError("Unsupported catalog ABI")
    maps = catalog_maps(rom, layout)
    trainers = catalog_trainers(rom, layout)
    named = {m["name"]: m["id"] for m in maps}
    services = [{"map": map_id, "town": town, "kind": kind, "status": "conditional"}
                for kind, pairs in (("healing", ((t,t+"_PokemonCenter_1F") for t in CENTERS)),
                                    ("shopping", MARTS.items()))
                for town, label in pairs if (map_id := named.get(label)) is not None]
    gyms = [dict(leader=leader, map=named.get(town+"_Gym"), status="conditional",
                 battle_format="singles", progression="native_story_and_badges",
                 trainer_symbols=[symbol]) for (leader,town),symbol in zip(KANTO_GYMS.items(),
                     ("TRAINER_LEADER_BROCK","TRAINER_LEADER_MISTY","TRAINER_LEADER_LT_SURGE",
                      "TRAINER_LEADER_ERIKA","TRAINER_LEADER_KOGA","TRAINER_LEADER_SABRINA",
                      "TRAINER_LEADER_BLAINE","TRAINER_LEADER_GIOVANNI"))]
    gyms.append(dict(leader="eirik", map=named["Havora_Gym"], status="conditional",
                     battle_format="doubles", protection="native_GameModes_PreserveGymTeam",
                     trainer_symbols=[r["symbol"] for r in trainers if (r["symbol"] or "").startswith("TRAINER_HAVORA_")]))
    result = dict(version=1, build=dict(revision=revision, rom_sha256=sha256(rom.rom).hexdigest(),
                                       elf_sha256=sha256(elf_path.read_bytes()).hexdigest(), code="BPRE"),
                  provenance=dict(tables=["gMapGroups","gWildMonHeaders","gSpeciesInfo","gTrainers"],
                                  script_scope="bounded_object_prefix_with_explicit_fallthrough_conditions", services="phase16_reviewed_registry"),
                  save=dict(sections=[rom.value("H",rom.address("sSaveSlotLayout")+4*i+2) for i in range(14)],
                            **{k:layout["save_"+k] for k in ("seed","trainer","modes","adventure")}),
                  ports=dict(context=rom.address("gWorldExportContext"), query=rom.address("gWorldExportPort")),
                  maps=maps, encounters=catalog_encounters(rom, layout), species=catalog_species(rom, layout),
                  trainers=trainers, services=services, gyms=gyms,
                  rules=dict(classic_caps=CLASSIC_CAPS, quantum_caps=QUANTUM_CAPS, reserved_crests=RESERVED_CRESTS,
                             time_variants=layout["wild_times"], season_time_variants=layout["wild_variants"],
                             nuzlocke_key="region_map_section", disposition="native_authoritative"))
    if "gWorldObservationPort" in rom.symbols:
        result["ports"]["observation"] = rom.address("gWorldObservationPort")
    result["ecology_protected"] = ecology_protection(rom, layout)
    result["catalog_sha256"] = digest(result)
    return result


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("rom", type=Path)
    cli.add_argument("elf", type=Path)
    cli.add_argument("output", type=Path)
    cli.add_argument("--nm", default="arm-none-eabi-nm")
    cli.add_argument("--revision")
    args = cli.parse_args()
    revision = args.revision or subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    args.output.write_text(encoded(build_catalog(args.rom,args.elf,args.nm,revision))+"\n", encoding="utf-8")
