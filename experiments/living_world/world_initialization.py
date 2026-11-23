"""Initialize a versioned native world in a separate emulator process."""
import argparse
from contextlib import closing
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter_ns
from uuid import uuid4

from native_world import Replica, read_context, snapshot
from platform_io import atomic_write
from world_manifest import catalog_check, encoded, import_world, native_manifest, validate_manifest


def read_json(path):
    return json.loads(path.read_bytes())


def write_json(path, document):
    atomic_write(path, encoded(document).encode("ascii") + b"\n")


def initialize(args):
    timings = {}

    def progress(stage, done, total, **extra):
        write_json(args.progress, dict(stage=stage, done=done, total=total,
                                       world_uuid=args.uuid, **extra))

    try:
        started = perf_counter_ns()
        catalog = read_json(args.catalog)
        with closing(Replica(args.rom, args.core, catalog, args.snapshot.read_bytes(),
                             read_json(args.context) if args.context else None)) as replica:
            timings["replica_startup"] = perf_counter_ns() - started
            started = perf_counter_ns()
            world = native_manifest(catalog, replica.context, replica, args.uuid, progress,
                                    timings=timings)
            timings["manifest_assembly"] = (perf_counter_ns() - started
                                            - timings["native_resolution"]
                                            - timings["resolution_progress"])
        progress("commit", 0, 1)
        started = perf_counter_ns()
        with closing(import_world(args.database, world)):
            pass
        timings["database_initialization"] = perf_counter_ns() - started
        if args.manifest:
            write_json(args.manifest, world)
        progress("ready", 1, 1, timings_ms={stage: duration / 1e6 for stage, duration in timings.items()})
    except (ValueError, RuntimeError, OSError, TimeoutError, sqlite3.Error) as error:
        progress("error", 0, 0)
        print(str(error), file=sys.stderr)
        return 1
    return 0


class WorldStartup:
    """Drive native handoffs without running a single frame on the player core."""

    def __init__(self, directory, rom_path, core_path, catalog_path):
        self.directory = directory
        directory.mkdir(exist_ok=True)
        self.rom = rom_path
        self.core = core_path
        self.catalog_path = catalog_path
        self.catalog = read_json(catalog_path)
        catalog_check(self.catalog, rom_path.read_bytes())
        self.generation = None
        self.task = None
        self.database = None
        self.context = None
        self.pending_flash = None

    def poll(self, game, battery):
        try:
            return self._poll(game, battery)
        except (ValueError, RuntimeError, OSError, TimeoutError, sqlite3.Error) as error:
            self.close()
            self.database = None
            write_json(self.directory / "progress.json", dict(stage="error", detail=str(error),
                                                                native_play=True))
            return None

    def _poll(self, game, battery):
        if self.task is not None and self.task.poll() is not None:
            succeeded = self.task.returncode == 0
            self.task = None
            if not succeeded:
                raise RuntimeError("Isolated world initialization failed")
            write_json(self.directory / "active.json", dict(database=self.database.name,
                       generation=self.generation, world_uuid=self.world_uuid))
            self.staging.cleanup()
            self.staging = None
            if self.pending_flash is not None:
                self.record_save(self.pending_flash)
                self.pending_flash = None
        native = read_context(lambda kind: (game.memory(kind), game.memory_size(kind)), self.catalog)
        if native is None:
            self.generation = None
            return
        if native["generation"] == self.generation:
            return
        self.close()
        self.generation = native["generation"]
        self.database = None
        self.context = native
        self.pending_flash = None
        write_json(self.directory / "active.json", dict(database=None, generation=self.generation))
        if native["origin"] == 2:
            if hasattr(game, "save_bytes"):
                battery = game.save_bytes()
            pair = self.directory / "checkpoints.sqlite3"
            if pair.exists():
                try:
                    with closing(PairedCheckpoints(pair)) as checkpoints:
                        self.database = checkpoints.restore(battery, native, self.catalog, self.directory)
                except ValueError:
                    write_json(self.directory / "progress.json",
                               dict(stage="continue_unpaired", native_play=True))
            if self.database is None:
                write_json(self.directory / "progress.json",
                           dict(stage="continue_unpaired", native_play=True))
            else:
                write_json(self.directory / "progress.json", dict(stage="restored", done=1, total=1,
                           database=self.database.name))
                write_json(self.directory / "active.json", dict(database=self.database.name,
                           generation=self.generation, restored=True))
            return
        self.world_uuid = str(uuid4())
        self.database = self.directory / f"{self.world_uuid}.sqlite3"
        self.staging = TemporaryDirectory(dir=self.directory)
        staging = Path(self.staging.name)
        (staging / "snapshot.bin").write_bytes(snapshot(game.core))
        write_json(staging / "context.json", native)
        write_json(self.directory / "progress.json", dict(stage="starting", done=0, total=0,
                                                           world_uuid=self.world_uuid))
        self.task = subprocess.Popen([sys.executable, "-B", str(Path(__file__).resolve()), "initialize",
                                      str(self.rom), str(self.core), str(self.catalog_path),
                                      str(staging / "snapshot.bin"), str(self.database),
                                      str(self.directory / "progress.json"), "--uuid", self.world_uuid,
                                      "--context", str(staging / "context.json")])

    def record_save(self, flash):
        # Admit only a complete native Flash save for this context.
        if self.context is None or not valid_flash_identity(flash, self.context, self.catalog["save"]):
            return
        if self.task is not None:
            self.pending_flash = flash
            return
        if self.database is None or not self.database.exists():
            return
        with closing(PairedCheckpoints(self.directory / "checkpoints.sqlite3")) as checkpoints:
            checkpoints.store(flash, self.database)

    def close(self):
        task = self.task
        if task is not None:
            if task.poll() is None:
                task.kill()
            task.wait()
            self.task = None
        staging = getattr(self, "staging", None)
        if staging is not None:
            staging.cleanup()
            self.staging = None


def flash_identity(flash, abi, *, include_counter=False):
    """Read the newest fully checksummed logical Flash slot."""
    from struct import unpack_from

    size = 4096
    lengths = abi["sections"]
    if len(flash) != 128 * 1024 or len(lengths) != 14:
        return None
    valid = []
    for slot in range(2):
        members = {}
        for i in range(len(lengths)):
            base = (slot * len(lengths) + i) * size
            section, check, signature, counter = unpack_from("<HHII", flash, base + 4084)
            if section >= len(lengths) or section in members or signature != 0x08012025:
                break
            total = sum(unpack_from(f"<{lengths[section]//4}I", flash, base)) & 0xFFFFFFFF
            actual = ((total >> 16) + (total & 0xFFFF)) & 0xFFFF
            if actual != check:
                break
            members[section] = (counter, base)
        if len(members) == len(lengths) and len({c for c, _ in members.values()}) == 1:
            valid.append(members[0])
    if not valid:
        return None
    counter, block = max(valid)
    seed = unpack_from("<I", flash, block + abi["seed"])[0]
    trainer = unpack_from("<I", flash, block + abi["trainer"])[0]
    modes = flash[block + abi["modes"]]
    tag = flash[block + abi["adventure"]:block + abi["adventure"] + 8]
    if len(tag) != 8 or tag[:5] != b"QADV\x01" or tag[5] not in (0,1) or tag[6] != (tag[5] ^ 255) or tag[7] != 167:
        return None
    identity = dict(seed=seed, trainer_id=trainer, modes=modes, mode=tag[5])
    if include_counter:
        identity["counter"] = counter
    return identity


def valid_flash_identity(flash, context, abi):
    identity = flash_identity(flash, abi)
    return bool(identity and all(context[k] == v for k,v in identity.items()))


class PairedCheckpoints:
    """Single-transaction publication of immutable Flash + world snapshots."""
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS paired ("
                        "battery TEXT PRIMARY KEY, flash BLOB NOT NULL, world BLOB NOT NULL, "
                        "world_digest TEXT NOT NULL, manifest TEXT NOT NULL)")

    def store(self, flash, database, *, before_commit=lambda: None):
        with TemporaryDirectory() as directory:
            staging = Path(directory) / "checkpoint.sqlite3"
            with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as current:
                with closing(sqlite3.connect(staging)) as saved:
                    current.backup(saved)
                    row = saved.execute("SELECT document FROM starting_manifest WHERE slot=1").fetchone()
            manifest = json.loads(row[0])
            validate_manifest(manifest)
            world = staging.read_bytes()
        key = sha256(flash).hexdigest()
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            prior = self.db.execute("SELECT manifest FROM paired WHERE battery=?", (key,)).fetchone()
            if prior and prior[0] != encoded(manifest):
                raise ValueError("Flash is already paired with another world")
            self.db.execute("INSERT OR IGNORE INTO paired VALUES (?,?,?,?,?)",
                            (key, flash, world, sha256(world).hexdigest(), encoded(manifest)))
            before_commit()
        return key

    def restore(self, flash, context, catalog, directory):
        key = sha256(flash).hexdigest()
        row = self.db.execute("SELECT flash,world,world_digest,manifest FROM paired WHERE battery=?",
                              (key,)).fetchone()
        if row is None or row[0] != flash or sha256(row[1]).hexdigest() != row[2]:
            raise ValueError("No valid paired checkpoint")
        manifest = json.loads(row[3])
        validate_manifest(manifest)
        prior = manifest["context"]
        if (manifest["catalog_sha256"] != catalog["catalog_sha256"]
                or any(prior[k] != context[k] for k in ("seed","mode","modes","features","trainer_id"))):
            raise ValueError("Incompatible paired checkpoint")
        # Restore to a fresh database so an unmanaged rollback cannot overwrite
        # the current world or its immutable historic checkpoint.
        destination = directory / f"{manifest['world_uuid']}-resume-{uuid4()}.sqlite3"
        atomic_write(destination, row[1])
        with closing(sqlite3.connect(destination.as_uri() + "?mode=ro", uri=True)) as saved:
            actual = saved.execute("SELECT document FROM starting_manifest WHERE slot=1").fetchone()
            if actual != (encoded(manifest),):
                raise ValueError("Checkpoint database identity mismatch")
        return destination

    def close(self):
        self.db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="command", required=True)
    init = modes.add_parser("initialize")
    for name in ("rom","core","catalog","snapshot","database","progress"):
        init.add_argument(name, type=Path)
    init.add_argument("--uuid", default=str(uuid4()))
    init.add_argument("--context", type=Path)
    init.add_argument("--manifest", type=Path)
    return initialize(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
