"""Compare real offline workers on identical initial worlds. Writes JSONL to stdout."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments/living_world"))
import agency
from inference import non_thinking_chat, windows_launcher_environment
from worker import ResidentWorker
from world import WorldMemory


def gemma(system, context):
    return f"<bos><start_of_turn>user\n{system}\n{context}<end_of_turn>\n<start_of_turn>model\n"


def peak(worker):
    if sys.platform == "win32":
        script = (f"$p=Get-CimInstance Win32_Process -Filter 'ParentProcessId={worker.process.pid}'; "
                  "(Get-Process -Id $p.ProcessId).PeakWorkingSet64")
        return int(subprocess.check_output(["powershell", "-NoProfile", "-Command", script], text=True))
    status = Path(f"/proc/{worker.process.pid}/status").read_text()
    return int(next(l.split()[1] for l in status.splitlines() if l.startswith("VmHWM:"))) * 1024


def benchmark(runtime, weights, style):
    with weights.open("rb") as f:
        print(json.dumps(dict(weights=weights.name, bytes=weights.stat().st_size,
                              sha256=hashlib.file_digest(f, "sha256").hexdigest())), flush=True)
    worker = ResidentWorker(runtime, windows_launcher_environment, model=weights)
    model = SimpleNamespace(render_prompt=gemma if style == "gemma" else non_thinking_chat, worker=worker)
    try:
        for case in ("ordinary", "player_intervenes", "peer_needs_help"):
            world = WorldMemory(":memory:", "benchmark", case.encode())
            rules = world.rules
            rules.observe(0, True)
            if case == "peer_needs_help":
                rules.observe(50, True)
                assert agency.submit(rules, agency.ticket(rules), "Learn shop routines|ask stock")
            for t in (100, 200, 300):
                rules.observe(t, True)
                request = agency.ticket(rules)
                if request is None:
                    continue
                raw, timing = agency.generate(model, request)
                if case == "player_intervenes" and t == 100:
                    assert rules.endorse()
                accepted = agency.submit(rules, request, raw, timing)
                print(json.dumps(dict(case=case, actor=request.actor, context=request.context,
                    raw=raw, accepted=accepted, validator=rules.state["agency"]["audit"][-1],
                    peak_bytes=peak(worker))), flush=True)
            world.close()
    finally:
        worker.close()


if __name__ == "__main__":
    benchmark(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3])
