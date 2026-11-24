"""Immutable ROM-derived starting world and Phase 16 database import."""
from collections import Counter
from hashlib import sha256
import json
from time import perf_counter_ns
from uuid import UUID

from simulation.engine import Simulation

VERSION = 1


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return sha256(encoded(value).encode("ascii")).hexdigest()


def verify_digest(document, field):
    if document.get(field) != digest({k: v for k, v in document.items() if k != field}):
        raise ValueError(f"{field} mismatch")


def catalog_check(catalog, rom=None):
    if catalog.get("version") != VERSION:
        raise ValueError("Unsupported catalog version")
    verify_digest(catalog, "catalog_sha256")
    if rom is not None and sha256(rom).hexdigest() != catalog["build"]["rom_sha256"]:
        raise ValueError("Catalog belongs to another ROM")


def static_specs(catalog):
    for location in catalog["maps"]:
        for obj in location["objects"]:
            binding = obj["binding"]
            if binding and binding.get("opcode") == 0xB6:
                yield location["id"], obj["local"], binding


def native_manifest(catalog, context, resolver, world_id, progress=lambda *args: None,
                    *, timings=None):
    """Resolve a frozen context. The resolver is an isolated native query client."""
    catalog_check(catalog)
    if context["version"] != VERSION or context["origin"] not in (1, 2) or not context["generation"]:
        raise ValueError("Missing committed native context")
    UUID(world_id)
    wild = [(table["header"], (table["variant"] << 16) | (table["method"] << 8) | slot["slot"])
            for table in catalog["encounters"] for slot in table["slots"]]
    supported = [row for row in catalog["species"] if row["enabled"]]
    species = [(row["id"], 0) for row in supported]
    trainers = [(record["id"], slot) for record in catalog["trainers"]
                for slot in range(record["party_count"])]
    specs = list(static_specs(catalog))
    static = [((map_id[0] << 16) | (map_id[1] << 8) | local, slot["species"] | (slot["level"] << 16))
              for map_id, local, binding in specs for slot in binding["party"]]
    # Native randomization caps its result at 20 moves. Authored learnsets can
    # be longer and are paged independently when Moves is disabled.
    pages = [1 if context["features"] & 128 else max(1, (len(row["learnset"])+19)//20)
             for row in supported]
    moves_queries = [(row["id"], page) for row, count in zip(supported, pages)
                     for page in range(count)]
    total = len(wild) + len(species) + len(moves_queries) + len(trainers) + len(static)
    completed = 0
    native_ns = 0
    progress_ns = 0

    def report_progress():
        nonlocal progress_ns
        started = perf_counter_ns()
        progress("resolve", completed, total)
        progress_ns += perf_counter_ns() - started

    report_progress()

    def rows(command, queries):
        nonlocal completed, native_ns
        for i in range(0, len(queries), resolver.page):
            batch = queries[i:i+resolver.page]
            started = perf_counter_ns()
            values = list(resolver.query(command, batch))
            native_ns += perf_counter_ns() - started
            if len(values) != len(batch):
                raise ValueError("Truncated native results")
            for value in values:
                if value[0] not in (1, 2):
                    raise ValueError(f"Catalog query rejected by native command {command}")
                yield value
            completed += len(batch)
            report_progress()

    wild_values = iter(rows(2, wild))
    encounter_data = []
    for table in catalog["encounters"]:
        slots = []
        for authored in table["slots"]:
            status, species_id, low, high, weight, *_ = next(wild_values)
            if status == 2:
                slots.append(dict(authored=authored, status="deferred_to_gameplay", reason="hidden_path"))
            else:
                if weight != authored["weight"]:
                    raise ValueError("Native and catalog slot weights differ")
                slots.append(dict(authored=authored, status="resolved", species=species_id, level=[low, high],
                                  individual="deferred_to_gameplay"))
        encounter_data.append(dict(table={k:v for k,v in table.items() if k != "slots"}, slots=slots))

    ability_values = list(rows(3, species))
    learnsets = iter(rows(4, moves_queries))
    species_by_id = {}
    for row, abilities, count in zip(supported, ability_values, pages, strict=True):
        if abilities[0] != 1:
            raise ValueError("Invalid native ability response")
        learnset = []
        for _ in range(count):
            moves = next(learnsets)
            if moves[0] != 1 or not 0 <= moves[1] <= len(moves) - 2:
                raise ValueError("Invalid native learnset response")
            learnset.extend([word & 0xFFFF, word >> 16] for word in moves[2:2+moves[1]])
        species_by_id[row["id"]] = dict(id=row["id"], authored=row, status="resolved",
                                       abilities=list(abilities[1:1+len(row["abilities"])]), learnset=learnset)
    species_data = [species_by_id.get(row["id"], dict(id=row["id"], authored=row,
                    status="deferred_to_gameplay", reason="native_species_disabled")) for row in catalog["species"]]

    trainer_values = iter(rows(5, trainers))
    trainer_data = []
    for row in catalog["trainers"]:
        party = []
        for _ in range(row["party_count"]):
            status, species_id, level, item, protected, ability, ability_slot, uses_learnset, *rest = next(trainer_values)
            if status == 2:
                party.append(dict(status="deferred_to_gameplay", reason="pool_or_rival_evolution"))
            else:
                party.append(dict(status="resolved", species=species_id, level=level, held_item=item,
                                  ability=ability, ability_slot=ability_slot, uses_learnset=bool(uses_learnset),
                                  moves=list(rest[:4]), individual="deferred_to_gameplay"))
        trainer_data.append(dict(id=row["id"], authored=row, status="conditional", protected=bool(protected),
                                 context="normal_native_row_single_trainer", party=party))

    fixed_values = iter(rows(6, static))
    static_data = []
    for map_id, local, binding in specs:
        party = []
        for authored in binding["party"]:
            status, species_id, level, *_ = next(fixed_values)
            if status != 1:
                raise ValueError("Invalid scripted species response")
            party.append(dict(authored=authored, status="resolved", species=species_id, level=level,
                              individual="deferred_to_gameplay"))
        static_data.append(dict(map=map_id, local=local, status="conditional", binding=binding, party=party))
    for stream in (wild_values, learnsets, trainer_values, fixed_values):
        assert next(stream, None) is None
    manifest = dict(version=VERSION, world_uuid=world_id, build=catalog["build"], catalog_sha256=catalog["catalog_sha256"],
                    context=context, maps=catalog["maps"], encounters=encounter_data, species=species_data,
                    trainers=trainer_data, static_encounters=static_data, gyms=catalog["gyms"],
                    services=catalog["services"], rules=catalog["rules"])
    if "ecology_protected" in catalog:
        manifest["ecology_protected"] = catalog["ecology_protected"]
    manifest["manifest_sha256"] = digest(manifest)
    validate_manifest(manifest)
    if timings is not None:
        timings.update(native_resolution=native_ns, resolution_progress=progress_ns)
    return manifest


def compatible_catalog(manifest, catalog):
    if manifest["catalog_sha256"] == catalog["catalog_sha256"]:
        return True
    # Reproduce the precise catalog digest that a prior launcher stored.
    # Allow only the exact pre-ecology metadata and pre-trainer script layout.
    if (not catalog.get("ecology_protected")
            or manifest["build"]["rom_sha256"] != catalog["build"]["rom_sha256"]):
        return False
    original = {k: v for k, v in catalog.items() if k != "catalog_sha256"}
    original["build"] = manifest["build"]
    if "ecology_protected" not in manifest:
        original.pop("ecology_protected")
    if digest(original) == manifest["catalog_sha256"]:
        return True
    # Phase 19 read the local-object byte and low trainer byte as one word.
    maps = []
    for row in original.get("maps", ()):
        if not isinstance(row, dict) or not isinstance(row.get("objects"), list):
            return False
        objects = []
        for obj in row["objects"]:
            binding = obj.get("binding") or {}
            if "trainer_local" in binding and binding.get("opcode") == 0x5C:
                binding = dict(binding)
                binding["trainer"] = binding.pop("trainer_local") | ((binding["trainer"] & 255) << 8)
                obj = dict(obj, binding=binding)
            objects.append(obj)
        maps.append(dict(row, objects=objects))
    return digest(dict(original, maps=maps)) == manifest["catalog_sha256"]


def validate_manifest(manifest):
    if manifest.get("version") != VERSION:
        raise ValueError("Unsupported manifest version")
    verify_digest(manifest, "manifest_sha256")
    UUID(manifest["world_uuid"])
    context = manifest["context"]
    if (context["version"] != VERSION or context["origin"] not in (1, 2) or context["mode"] not in (0, 1)
            or type(context["seed"]) is not int or not 0 <= context["seed"] <= 0xFFFFFFFF
            or not 1 <= context["generation"] <= 0xFFFFFFFF or not 0 <= context["features"] <= 255):
        raise ValueError("Invalid committed ROM context")
    for value in (manifest["catalog_sha256"], manifest["build"]["rom_sha256"]):
        if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError("Invalid build digest")
    maps = {tuple(m["id"]) for m in manifest["maps"]}
    if len(maps) != len(manifest["maps"]) or not maps:
        raise ValueError("Duplicate or missing map")
    species = {row["id"] for row in manifest["species"]}
    if "ecology_protected" in manifest:
        protection = manifest["ecology_protected"]
        if (not isinstance(protection, list)
                or any(type(item) is not int or item not in species for item in protection)
                or protection != sorted(set(protection))):
            raise ValueError("Invalid native ecology protection list")
    trainers = {row["id"] for row in manifest["trainers"]}
    if len(species) != len(manifest["species"]) or len(trainers) != len(manifest["trainers"]):
        raise ValueError("Duplicate species or trainer IDs")
    tables = set()
    for encounter in manifest["encounters"]:
        table = encounter["table"]
        key = (table["header"], table["variant"], table["method"])
        if key in tables or tuple(table["map"]) not in maps:
            raise ValueError("Duplicate or unknown encounter table")
        tables.add(key)
        weights = Counter()
        for index, row in enumerate(encounter["slots"]):
            if row["authored"]["slot"] != index or row["status"] not in {"resolved","deferred_to_gameplay"}:
                raise ValueError("Invalid encounter resolution")
            if row["status"] == "resolved":
                check_mon(row, species, ranges=True)
            if row["authored"]["weight"] is not None:
                weights[row["authored"]["rod"]] += row["authored"]["weight"]
        if any(weight != 100 for weight in weights.values()):
            raise ValueError("Invalid slot weights")
    for trainer in manifest["trainers"]:
        if len(trainer["party"]) != trainer["authored"]["party_count"]:
            raise ValueError("Trainer party size mismatch")
        for member in trainer["party"]:
            if member["status"] == "resolved":
                check_mon(member, species)
            elif member["status"] != "deferred_to_gameplay":
                raise ValueError("Invalid trainer resolution")
    for spawn in manifest["static_encounters"]:
        if tuple(spawn["map"]) not in maps:
            raise ValueError("Unknown static map")
        for member in spawn["party"]:
            check_mon(member, species)


def check_mon(row, species, *, ranges=False):
    levels = row["level"] if ranges else [row["level"]]
    if (row["species"] not in species or levels != sorted(levels)
            or any(not 1 <= level <= 100 for level in levels)):
        raise ValueError(f"Invalid resolved Pokémon: {row}, known={row['species'] in species}")


def world_state(manifest):
    """Initial simulation entities. Native availability remains a separate fact."""
    validate_manifest(manifest)
    locations, people, habitats = {}, {}, {}
    for row in sorted(manifest["maps"], key=lambda m: m["id"]):
        group, number = row["id"]
        place = f"{group}:{number}"
        locations[place] = dict(town=place, kind="native_map", accessible=True, owner=None,
                                capacity=0, name=row["name"], native=row["id"])
        for obj in row["objects"]:
            binding = obj["binding"]
            if not binding or binding.get("opcode") != 0x5C:
                continue
            actor = f"{place}:{obj['local']}"
            people[actor] = dict(name=f"Trainer {binding['trainer']}", native_trainer=binding["trainer"],
                                 location=place, home=None, employer=None, money=0, goods={}, skills={},
                                 relationships={}, known={}, memories=[], traits=[], controller="npc", goal=None,
                                 plan=[], ready=0, transit=None, energy=5)
    for table in manifest["encounters"]:
        source = table["table"]
        group, number = source["map"]
        key = f"{group}:{number}"
        habitats.setdefault(key, []).append(dict(header=source["header"], variant=source["variant"],
                                                 method=source["method"], abundance=None))
    return dict(version=1, seed=manifest["context"]["seed"], tick=0, revision=0,
                habitats=habitats, native_services=manifest["services"], native_gyms=manifest["gyms"],
                world_uuid=manifest["world_uuid"], manifest_sha256=manifest["manifest_sha256"],
                locations=locations, routes={}, people=people, firms={}, pokemon={}, requirements={},
                requests={}, pending=[], events={}, wake={}, issued_money=0, focus=[], case="native_manifest")


def import_world(path, manifest):
    """Atomically seed a simulation and its immutable manifest, or reopen the same world."""
    state = world_state(manifest)
    return Simulation(path, state, manifest=manifest)
