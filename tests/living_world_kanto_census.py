"""Verify that the catalog accounts for the actual ROM object tables."""

import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "experiments" / "living_world"


def main():
    with TemporaryDirectory() as directory:
        catalog = Path(directory) / "catalog.sqlite3"
        subprocess.run([sys.executable, "-B", APP / "build-knowledge.py", catalog], check=True)
        with sqlite3.connect(catalog) as db:
            assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
            assert not db.execute("PRAGMA foreign_key_check").fetchall()
            maps = dict(db.execute("SELECT id, token FROM kanto_map"))
            ids = {id_: json.loads(data) for id_, data in db.execute("SELECT id, data FROM kanto_identity")}
            objects = {(name, slot): json.loads(data)
                       for name, slot, data in db.execute("SELECT map, slot, data FROM kanto_appearance")}
            assert {"PalletTown", "Route1", "ViridianCity", "Route2", "ViridianForest", "PewterCity",
                    "Route3", "MtMoon_1F", "MtMoon_B1F", "MtMoon_B2F", "Route4", "CeruleanCity",
                    "Route24", "Route25", "Route25_SeaCottage"} <= maps.keys()
            for name, token in maps.items():
                path = ROOT / "data" / "maps" / name / "map.json"
                source = json.loads(path.read_bytes())
                assert source["id"] == token
                for i, row in enumerate(source["object_events"], 1):
                    obj = objects[name, i]
                    assert obj["position"] == [row["x"], row["y"]]
                    assert obj["graphics"] == row["graphics_id"]
                    if obj["kind"] == "person":
                        assert obj["identity"] in ids
                        assert obj["scripts"], obj
                assert len(source["object_events"]) == sum(key[0] == name for key in objects)
            for key, count in (("oak", 2), ("blue", 2), ("brock", 2), ("bill", 2),
                               ("society_researcher", 3)):
                assert len(ids[key]["appearances"]) == count
            for name, slot, trainer in (("CeruleanCity_Gym", 3, "TRAINER_LEADER_MISTY"),
                                        ("PewterCity_Gym", 1, "TRAINER_LEADER_BROCK"),
                                        ("MtMoon_1F", 1, "TRAINER_LASS_IRIS")):
                assert trainer in objects[name, slot]["trainer_data"]
            assert objects["Route4", 7]["identity"] == objects["CeruleanCity", 12]["identity"]
            assert ids["misty"]["tier"] == 3 and ids["misty"]["protected"]
            assert {x["kind"] for x in objects.values()} == {
                "person", "pokemon", "prop", "clone", "story_marker", "remote_avatar"
            }
            assert all(x["memory_capacity"] <= 8 for x in ids.values())
            print(f"Validated {len(maps)} maps, {len(objects)} object records, {len(ids)} identities")


if __name__ == "__main__":
    main()
