"""Filesystem integration shared by the host, launcher and diagnostics."""

from contextlib import closing, contextmanager
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import time
from zipfile import ZIP_DEFLATED, ZipFile


def profile_directory(version):
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / ".local/share")
    return base / ("LivingQuantumWorldPhase11" if version == 11 else "LivingQuantumWorld")


def atomic_write(path, data, *, durable=True):
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
        temporary = Path(output.name)
        try:
            output.write(data)
            output.flush()
            if durable:
                os.fsync(output.fileno())
            output.close()
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


@contextmanager
def profile_lock(profile):
    """One game or backup writer per profile, released by the OS on exit."""
    profile.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(profile / "profile-lock.sqlite3", timeout=0)) as lock:
        try:
            lock.execute("BEGIN EXCLUSIVE")
        except sqlite3.OperationalError as error:
            raise RuntimeError("Cannot lock the save profile. Close any running game and retry.") from error
        yield


def backup_profile(profile):
    with profile_lock(profile):
        saves = sorted((*profile.glob("*.sav"), *profile.glob("*.bak")))
        if not saves:
            raise RuntimeError("No saved games to back up yet.")
        destination = profile / "Backups"
        destination.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=destination, delete=False) as temporary:
            staging = Path(temporary.name)
        target = staging.with_name(f"Quantum-{time.time_ns()}.zip")
        try:
            with tempfile.TemporaryDirectory() as directory, ZipFile(staging, "w", ZIP_DEFLATED) as archive:
                database = profile / "living-world.sqlite3"
                if database.is_file():
                    copy = Path(directory) / database.name
                    with (closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as reader,
                          closing(sqlite3.connect(copy)) as writer):
                        reader.backup(writer)
                    archive.write(copy, database.name)
                for path in saves:
                    archive.write(path, path.name)
            staging.rename(target)
        finally:
            staging.unlink(missing_ok=True)
    return target


def publish_monitor(profile, memory, hint, population, pending, decisions, slot, *, running=True):
    regional = population.state if population else {}
    society = memory.society.state
    requests = regional.get("requests", {})
    events = sorted(regional.get("events", {}).items(),
                    key=lambda row: (row[1]["updated"], row[0]))[-12:]
    objective = regional.get("objective")
    survey_event = regional.get("events", {}).get(objective["event"]) if objective else None
    data = {
        "updated": time.time(), "running": running, "save_slot": slot,
        "bridge": {"area": hint.area, "frame": hint.frame, "busy": hint.busy,
                   "rom_reported_nearby_npc": hint.npc, "game_second": hint.local_second,
                   "dialogue_pending": pending} if hint else None,
        "rom_actor_projections": {
            "brock": {"location": memory.director.location, "goal": memory.director.state.get("goal"),
                      "plan": memory.director.state.get("plan")},
            **{id_: {key: actor.get(key) for key in ("location", "activity", "active", "bonds", "facts")}
               for id_, actor in society["agents"].items()},
        },
        "host_only_residents": [
            {"name": population.people[id_].name, "shift_seconds": population.people[id_].shift,
             "days_off": population.people[id_].days_off,
             **{key: actor.get(key) for key in ("location", "activity", "goal", "due", "bonds", "facts")}}
            for id_, actor in regional.get("actors", {}).items() if id_ in population.people
        ],
        "recent_events": events + list(society.get("log", ()))[-8:],
        "pending_resident_requests": requests,
        "survey_event": survey_event,
        "dynamic_quests": {"Survey Notes": objective,
                           "Museum Follow-up": society.get("museum_objective"),
                           "Locate Brock": memory.director.state.get("quest")},
        "decisions_and_failures": list(decisions),
    }
    atomic_write(profile / "monitor.json", (json.dumps(data, indent=2) + "\n").encode(), durable=False)
