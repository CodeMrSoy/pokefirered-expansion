"""Bounded transport to the existing isolated local worker."""

from pathlib import Path
from queue import Empty, Queue
import subprocess
import sys
from threading import Thread
from time import perf_counter


class ResidentWorker:
    def __init__(self, runtime, windows_environment, timeout=8, model=None):
        self.runtime = Path(runtime).resolve()
        self.model = Path(model).resolve() if model else self.runtime / "model.gguf"
        self.windows_environment = windows_environment
        self.timeout = timeout
        self.startup_timeout = max(timeout, 30)
        self.process = None
        self.load_ms = None
        self.launch_ms = None

    @staticmethod
    def _read(stream, records):
        try:
            for record in iter(lambda: stream.readline(1200), b""):
                records.put(record.rstrip(b"\r\n"))
        finally:
            records.put(None)

    def _receive(self, timeout, stage):
        try:
            line = self.records.get(timeout=timeout)
        except Empty as error:
            raise TimeoutError(f"Offline worker timed out during {stage} ({timeout:g}s)") from error
        if line is None:
            raise RuntimeError(f"Offline worker closed the pipe, exit {self.process.poll()}")
        return line

    def start(self):
        if self.process is not None:
            return
        if sys.platform == "win32":
            launcher, env = "sandbox.exe", self.windows_environment()
        elif sys.platform == "linux":
            launcher, env = "offline-worker", {}
        else:
            raise RuntimeError("No inference isolation backend for this platform")
        start = perf_counter()
        self.records = Queue()
        self.process = subprocess.Popen(
            [str(self.runtime / launcher), str(self.model), "--serve"],
            cwd=self.runtime, env=env, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        self.reader = Thread(target=self._read, args=(self.process.stdout, self.records), daemon=True)
        self.reader.start()
        try:
            line = self._receive(self.startup_timeout, "startup")
            if sys.platform == "linux":
                if line != b"LQW isolation active":
                    raise RuntimeError(f"Linux isolation did not initialize: {line[:240]!r}")
                line = self._receive(self.startup_timeout, "startup")
            marker, separator, time_ms = line.partition(b" ")
            if not separator or marker != b"ready":
                raise RuntimeError(f"Worker startup failed: {line[:240]!r}")
            self.load_ms = float(time_ms)
            self.launch_ms = (perf_counter() - start) * 1000
        except Exception:
            self.close()
            raise

    def generate(self, grammar, prompt, *, timeout=None):
        fields = [field.encode("utf-8") for field in (grammar, prompt)]
        if any(not field or len(field) > 4096 or b"\0" in field for field in fields):
            raise ValueError("Inference request outside protocol limits")
        self.start()
        start = perf_counter()
        try:
            self.process.stdin.write(b"\t".join(field.hex().encode("ascii") for field in fields) + b"\n")
            self.process.stdin.flush()
            record = self._receive(self.timeout if timeout is None else timeout, "generation")
            parts = record.split(b" ", 2)
            if len(parts) != 3 or parts[0] != b"ok":
                raise RuntimeError(f"Worker did not generate a complete response: {record[:240]!r}")
            text = bytes.fromhex(parts[2].decode("ascii")).decode("utf-8")
            return text, {
                "load_ms": round(self.load_ms, 3),
                "launcher_overhead_ms": round(max(0, self.launch_ms - self.load_ms), 3),
                "inference_ms": float(parts[1]),
                "pipe_ms": round(max(0, (perf_counter() - start) * 1000 - float(parts[1])), 3),
            }
        except Exception:
            self.close()
            raise

    def close(self):
        if self.process is None:
            return
        process, self.process = self.process, None
        try:
            process.stdin.close()
        except BrokenPipeError:
            pass
        try:
            process.wait(timeout=0.3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        self.reader.join(timeout=1)
        process.stdout.close()
