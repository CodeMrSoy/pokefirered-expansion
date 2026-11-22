"""Build the portable SQLite catalog from audited Pokémon Quantum source data."""

import argparse
import json
from pathlib import Path
import re
import sqlite3
from tempfile import TemporaryDirectory

from bridge import LINE
from knowledge import SCHEMA
from kanto_source import write_catalog
from routines import KANTO
from social import SIGHTINGS

ROOT = Path(__file__).resolve().parents[2]
FAMILY = "src/data/pokemon/species_info/gen_1_families.h"
SPECIES_HEADER = "include/constants/species.h"
WILDS = "src/data/wild_encounters.json"
PALLET = "data/maps/PalletTown/map.json"
LAB = "data/maps/PalletTown_ProfessorOaksLab/scripts.inc"
DAISY = "data/maps/PalletTown_RivalsHouse/scripts.inc"
HARBOR = "data/maps/Havora_Harbor/scripts.inc"
TYPES = "src/data/types_info.h"
SPECIES = ("BULBASAUR", "CHARMANDER", "SQUIRTLE", "PIDGEOT", "PIKACHU", "RAICHU",
           "NIDORINO", "CLEFAIRY", "WARTORTLE", "CATERPIE", "WEEDLE", "CHANSEY",
           "VULPIX", "MAGNEMITE", "ODDISH", "NIDORAN_M", "IVYSAUR", "CHARMELEON")


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def db_rows():
    rows = []

    def add(key, topic, text, source, *, kind="canonical", species=None, area="",
            region="", access="public", required="", trust=0, progress="", priority=0, line=""):
        if line and not LINE.fullmatch(line):
            raise ValueError(f"GBA line too long or incompatible: {line!r}")
        file, _, anchor = source.partition("#")
        if anchor not in read(file):
            raise ValueError(f"Missing source anchor for {key}: {source}")
        rows.append((key, kind, topic, species, area, region, access, required,
                     trust, progress, priority, text, line, source))

    source = read(FAMILY)
    ids = {key: int(value) for key, value in re.findall(
        r"^#define SPECIES_(\w+)\s+(\d+)\b", read(SPECIES_HEADER), re.M)}
    for key in SPECIES:
        symbol = f"[SPECIES_{key}]"
        block = source.split(symbol, 1)[1].split("\n    },", 1)[0]
        name = re.search(r'\.speciesName = _\("([^"]+)"\)', block)[1]
        species = ids[key]
        typing = re.search(r"\.types = MON_TYPES\((TYPE_\w+(?:, TYPE_\w+)?)\)", block)
        if typing:
            names = [item.removeprefix("TYPE_").title() for item in typing[1].split(", ")]
            add(f"species:{key}:type", "species", f"{name} type: {' and '.join(names)}.",
                f"{FAMILY}#{symbol}", species=species, priority=35)
        abilities = re.search(r"\.abilities = \{ ([A-Z_, ]+) \}", block)
        if abilities:
            names = [item.removeprefix("ABILITY_").replace("_", " ").title()
                     for item in abilities[1].split(", ") if item != "ABILITY_NONE"]
            if names:
                add(f"species:{key}:ability", "abilities", f"{name} base species data lists {', '.join(names)}.",
                    f"{FAMILY}#{symbol}", species=species, access="expertise", required="biology", priority=55)
        add(f"witnessed:{species}", "discovery", f"You have seen this trainer with {name} before.",
            "src/living_world_bridge.c#gLivingWorldMailbox", kind="discovery", species=species,
            access="witnessed", required=str(species), priority=88)

    # Check precise evolution conditions in the respective source entries.
    for key, anchor, text, line in [
        ("PIKACHU", "EVO_ITEM, ITEM_THUNDER_STONE, SPECIES_RAICHU", "Pikachu can evolve into Raichu with a Thunder Stone.", "A Thunder Stone does it."),
        ("SQUIRTLE", "EVO_LEVEL, 16, SPECIES_WARTORTLE", "Squirtle can evolve into Wartortle at level 16.", "It could become Wartortle."),
        ("BULBASAUR", "EVO_LEVEL, 16, SPECIES_IVYSAUR", "Bulbasaur can evolve into Ivysaur at level 16.", ""),
        ("CHARMANDER", "EVO_LEVEL, 16, SPECIES_CHARMELEON", "Charmander can evolve into Charmeleon at level 16.", ""),
    ]:
        add(f"evolution:{key}", "evolutions", text, f"{FAMILY}#{anchor}",
            species=ids[key], access="expertise", required="biology", priority=105, line=line)

    electric = re.search(r"^    \[TYPE_ELECTRIC\] = \{([^}]+)\}", read(TYPES), re.M)[1].split(", ")
    if electric[12] != "X(2.0)" or electric[3] != "X(2.0)":
        raise ValueError("Electric type matchup changed")
    add("battle:electric", "battle", "Electric moves are strong against Water and Flying types.",
        f"{TYPES}#[TYPE_ELECTRIC]", species=25, access="expertise", required="battle",
        priority=105, line="Water teams hate sparks.")
    add("battle:water", "battle", "Electric moves are strong against Water types.",
        f"{TYPES}#[TYPE_ELECTRIC]", species=7, access="expertise", required="battle",
        priority=105, line="Watch out for sparks.")
    add("care:pikachu", "care", "Daisy advises taking a break to rest your Pokemon.",
        f"{DAISY}#PalletTown_RivalsHouse_EventScript_PleaseGiveMonsRest::", species=25,
        access="expertise", required="care", priority=105, line="Even sparks need a rest.")
    add("care:squirtle", "care", "Daisy advises taking a break to rest your Pokemon.",
        f"{DAISY}#PalletTown_RivalsHouse_EventScript_PleaseGiveMonsRest::", species=7,
        access="expertise", required="care", priority=105, line="Let Squirtle catch a break.")
    add("watts:pikachu", "electronics", "Watts handles PCs and takes extra care around Electric Pokemon.",
        "experiments/living_world/profiles.py#Keep the town's computers working.",
        kind="belief", species=25, access="personal", required="pc_resident", priority=105,
        line="Easy around my cables.")
    add("watts:squirtle", "electronics", "Watts compares Pokemon near the pond and keeps water away from PCs.",
        "experiments/living_world/profiles.py#Compare how different Pokemon behave near the pond.",
        kind="belief", species=7, access="personal", required="pc_resident", priority=105,
        line="The pond's nice and cool.")

    for folder, name, region, area in (
        ("PalletTown", "Pallet Town", "kanto", "pallet"),
        ("PalletTown_ProfessorOaksLab", "Oak's lab", "kanto", "oak_lab"),
        ("PalletTown_RivalsHouse", "the rival's house", "kanto", "rival_house"),
        ("PalletTown_PlayersHouse_1F", "the player's home", "kanto", "player_house"),
        ("ViridianCity", "Viridian City", "kanto", "viridian_city"),
        ("Route1", "Route 1", "kanto", "route_1"),
        ("ViridianForest", "Viridian Forest", "kanto", "viridian_forest"),
        ("MtMoon_1F", "Mt. Moon", "kanto", "mt_moon"),
        ("Havora_Harbor", "Havora Harbor", "vidra", "havora_harbor"),
        ("Havora_Market", "Havora Market", "vidra", "havora_market"),
        ("Corvala_Town", "Corvala Town", "vidra", "corvala"),
        ("Vidra_CoastalRoad", "the Coastal Road", "vidra", "coastal_road"),
        ("Eldervik_Woods", "Eldervik Woods", "vidra", "eldervik"),
        ("Frostfell_Mountains", "Frostfell Mountains", "vidra", "frostfell"),
    ):
        path = f"data/maps/{folder}/map.json"
        data = json.loads(read(path))
        add(f"map:{area}", "geography", f"This place is {name}, in {region.title()}.",
            f"{path}#{data['id']}", area=area, region=region, access="local", priority=10)
    if not any(link["map"] == "MAP_ROUTE1" and link["direction"] == "up"
               for link in json.loads(read(PALLET))["connections"]):
        raise ValueError("Pallet Town no longer connects north to Route 1")
    add("pallet:route1", "geography", "Route 1 heads north out of Pallet Town.",
        f"{PALLET}#MAP_ROUTE1", area="pallet", region="kanto", access="local", priority=20)
    add("pallet:oak", "characters", "Professor Oak runs the local lab.",
        f"{PALLET}#MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB", area="pallet", region="kanto",
        access="character", required="oak", priority=15)
    add("pallet:daisy-blue", "relationships", "Daisy is Blue's sister.",
        f"{DAISY}#PalletTown_RivalsHouse_Text_HiBrothersAtLab", area="rival_house", region="kanto",
        access="character", required="blue", priority=20)
    add("pallet:daisy-contest", "history", "Daisy once won the Spring Pokemon Contest.",
        "data/text/fame_checker.inc#PokemonJournal_Text_SpecialFeatureDaisyOak::",
        area="rival_house", region="kanto", access="personal", required="daisy", priority=30)
    add("kanto:lance-rumor", "rumors", "A journal speculates that Lance's grandfather leads a clan of Dragon masters.",
        "data/text/fame_checker.inc#PokemonJournal_Text_SpecialFeatureLance::",
        kind="rumor", area="oak_lab", region="kanto", access="conversation",
        required="lance-journal", progress="league_clear")
    add("pallet:daisy-care", "local_culture", "Daisy offers Pokemon grooming after the League.",
        f"{DAISY}#PalletTown_RivalsHouse_EventScript_GroomMon::", area="rival_house",
        region="kanto", access="personal", required="daisy", progress="league_clear")
    add("pallet:league", "world_events", "The trainer has returned after clearing the League.",
        f"{LAB}#PalletTown_ProfessorOaksLab_EventScript_PostgameBlue::", area="oak_lab",
        region="kanto", access="personal", required="blue", progress="league_clear", priority=25)
    add("vidra:koga", "world_events", "Koga was seen heading north toward Havora's market.",
        f"{HARBOR}#Havora_Harbor_Text_KogaClue::", area="havora_harbor", region="vidra",
        access="witnessed", required="koga-market", progress="vidra_koga_search")
    add("vidra:stellar-ticket", "quests", "A traveler in the Safari Zone Secret House gives the Stellar Ticket.",
        "data/maps/SafariZone_SecretHouse/scripts.inc#giveitem ITEM_STELLAR_TICKET", area="safari",
        region="kanto", access="local", progress="vidra_ticket_quest")
    add("survey:pond", "quests", "Watts has finished this trainer's pond survey.",
        "experiments/living_world/world.py#pond_survey", kind="discovery", area="pallet",
        region="kanto", access="witnessed", required="pond-survey", trust=2, priority=60)

    for species, name in SIGHTINGS.items():
        event = f"pallet-sighting:{species}"
        add(event, "local_news", f"Watts told the sign guide he saw the trainer's {name} in Pallet.",
            "experiments/living_world/social.py#INSERT OR IGNORE INTO npc_knowledge",
            kind="rumor", area="pallet", region="kanto", access="conversation",
            required=event, priority=90, line=f"Watts saw your {name}.")
        for resident, sender in ((KANTO.scout, "Pallet's sign guide"), (KANTO.researcher, "the Route 1 scout")):
            relay = f"relay:{resident.npc}:{species}"
            add(relay, "local_news", f"{sender} passed along a secondhand report of {name} originally seen by Watts.",
                "experiments/living_world/routines.py#def _transfer(", kind="rumor",
                area=resident.area, region="kanto", access="conversation",
                required=relay, priority=100, line=f"Watts reported a {name}.")

    wilds = json.loads(read(WILDS))["wild_encounter_groups"][0]["encounters"]
    forest = next(entry for entry in wilds if entry["map"] == "MAP_VIRIDIAN_FOREST")
    forest_species = {mon["species"] for mon in forest["land_mons"]["mons"]}
    for key in ("PIKACHU", "CATERPIE", "WEEDLE"):
        if f"SPECIES_{key}" not in forest_species:
            raise ValueError(f"{key} is no longer in Viridian Forest's base land encounter table")
        add(f"habitat:{key}", "habitats", f"{key.title()} appears in Viridian Forest's standard encounter table.",
            f"{WILDS}#MAP_VIRIDIAN_FOREST", species=ids[key], area="viridian_forest", region="kanto",
            access="expertise", required="research", priority=70)
    return rows


def build(output):
    rows = db_rows()
    # Source references establish roles. These reviewed examples only add
    # character voice. Canonical claims still come from the permitted facts.
    pallet_script = "data/maps/PalletTown/scripts.inc"
    examples = (
        ("pc_resident", 25, 0, "Mind those cheeks, partner.", pallet_script, "PalletTown_EventScript_FatMan"),
        ("pc_resident", 7, 0, "Fancy a dip, Squirtle?", pallet_script, "PalletTown_EventScript_FatMan"),
        ("daisy", 25, 0, "Take a breather, you two.", DAISY, "PalletTown_RivalsHouse_EventScript_PleaseGiveMonsRest"),
        ("daisy", 25, 1, "Good to see you both again.", DAISY, "PalletTown_RivalsHouse_EventScript_PleaseGiveMonsRest"),
        ("daisy", 7, 0, "Rest a bit, Squirtle.", DAISY, "PalletTown_RivalsHouse_EventScript_PleaseGiveMonsRest"),
        ("oak", 7, 0, "Study that Squirtle closely.", LAB, "PalletTown_ProfessorOaksLab_EventScript_RatePokedex"),
        ("oak", 25, 1, "Back to compare notes?", LAB, "PalletTown_ProfessorOaksLab_EventScript_RatePokedex"),
        ("sign_guide", 0, 0, "You might find this handy.", pallet_script, "PalletTown_EventScript_SignLadyDone"),
    )
    for npc, species, remembered, line, source, label in examples:
        if not LINE.fullmatch(line) or f"{label}::" not in read(source):
            raise ValueError(f"Invalid voice example for {npc} ({species}, {remembered})")
    for map_name, slot, script in (
        ("PalletTown", 1, "PalletTown_EventScript_SignLady"),
        ("PalletTown", 2, "PalletTown_EventScript_FatMan"),
        ("PalletTown_RivalsHouse", 1, "PalletTown_RivalsHouse_EventScript_Daisy"),
        ("PalletTown_ProfessorOaksLab", 4, "PalletTown_ProfessorOaksLab_EventScript_ProfOak"),
        ("Route1", 2, "Route1_EventScript_Boy"),
        ("ViridianCity", 6, "ViridianCity_EventScript_Youngster"),
    ):
        objects = json.loads(read(f"data/maps/{map_name}/map.json"))["object_events"]
        if objects[slot - 1]["script"] != script:
            raise ValueError(f"Field prediction object slot changed for {map_name}")
    header = read("include/constants/living_world.h")
    for actor, token in ((KANTO.scout, "SCOUT"), (KANTO.researcher, "STUDENT")):
        for suffix, hour in (("START", actor.starts), ("END", actor.ends)):
            if not re.search(rf"^#define LIVING_WORLD_{token}_{suffix}\s+{hour}$", header, re.M):
                raise ValueError(f"ROM hours differ from {actor.npc}'s simulated schedule")
    with TemporaryDirectory(dir=output.parent) as directory:
        candidate = Path(directory) / output.name
        with sqlite3.connect(candidate) as db:
            db.executescript(SCHEMA)
            db.executemany("INSERT INTO fact VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
            db.executemany("INSERT INTO dialogue_example VALUES (?,?,?,?,?)", (
                (npc, species, remembered, line, source + "#" + label)
                for npc, species, remembered, line, source, label in examples
            ))
            write_catalog(db, ROOT)
        db.close()
        candidate.replace(output)
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(f"Built catalog with {build(args.output)} facts")
