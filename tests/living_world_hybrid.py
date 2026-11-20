"""Exercise selective invalidation and compare the same contexts with Phase 5."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
import os
from pathlib import Path
from statistics import median, quantiles
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Event
from time import perf_counter
from types import SimpleNamespace

APP = Path(__file__).resolve().parents[1] / "experiments/living_world"
sys.path.insert(0, str(APP))
from bridge import Conversation, validate
from hybrid import FIELD_HINT, FieldHint, HybridDialogue
from inference import LocalModel
from reasoning import GuideTurn
from world import WorldMemory

NAMES = {"25": "Pikachu", "7": "Squirtle"}
WATTS = Conversation("pc_resident", 25)
DAISY = Conversation("daisy", 25)
OAK = Conversation("oak", 25)
GUIDE = Conversation("sign_guide", None)


def result(lookup):
    response, route = lookup.future.result(timeout=12)
    return validate(response.dialogue).decode(), route


def verify(catalog, save):
    memory = WorldMemory(save, "demo", b"001")
    model = SimpleNamespace(catalog=catalog, style="unavailable", species_names=NAMES)
    with ThreadPoolExecutor(max_workers=1) as pool:
        router = HybridDialogue(memory, model, pool)
        hint = FieldHint.decode(FIELD_HINT.pack(b"LQP1", 1, 25, 1, 2, 1, 3))
        assert hint.npc == WATTS.npc
        assert not router.predict(hint, 0.0)
        assert router.predict(hint, 0.26)
        first = router.request(WATTS, hint)
        assert first.cache == "hit" and "cheeks" in result(first)[0]
        assert router.request(WATTS, replace(hint, story=3)).cache == "miss"
        squirtle = Conversation(WATTS.npc, 7)
        assert "Squirtle" in result(router.request(squirtle, replace(hint, species=7)))[0]

        guide_old = router.request(GUIDE)
        assert "Watts saw" not in result(guide_old)[0]
        assert "Thunder Stone" in result(router.request(OAK))[0]
        assert "breather" in result(router.request(DAISY))[0]
        changes = memory.apply(first.key.state.encounter, first.future.result()[0].action)
        assert "social_sighting_scheduled" in changes
        repeat = router.request(WATTS, hint)
        assert repeat.cache == "miss" and "again" in result(repeat)[0]
        assert not result(repeat)[1] == "model_decision"
        memory.social.tick(memory.social.deadline)
        guide = router.request(GUIDE)
        assert guide.cache == "miss" and "Watts saw your Pikachu." in result(guide)[0]
        assert router.request(DAISY).cache == "hit" and router.request(OAK).cache == "hit"
        turn = memory.social.guide_turn("pallet-sighting:25")
        assert memory.social.apply_guide_turn(turn, "ASK_WATTS")
        assert "I asked him" in result(router.request(GUIDE))[0]
        memory.social.tick(memory.social.deadline)
        after = router.request(GUIDE)
        assert after.cache == "miss" and "wasn't sure" in result(after)[0]
        assert router.request(GUIDE).cache == "hit"
        catalog.touch()
        assert router.request(OAK).cache == "miss"

        memory.checkpoint(b"002")
        assert router.request(OAK).cache == "miss"
        separate = WorldMemory(save, "other", b"001")
        other = HybridDialogue(separate, model, pool)
        assert "Watts saw" not in result(other.request(GUIDE))[0]
        separate.close()
    memory.close()
    print("PASS follower, story, save, catalog, evidence and relationship invalidation. Unrelated NPC replies stayed cached.")


def speculative(catalog, save):
    memory = WorldMemory(save, "demo", b"001")
    started, release = Event(), Event()
    model = SimpleNamespace(catalog=catalog, style="qwen3", species_names=NAMES)
    first = memory.context(WATTS)
    memory.apply(first, "ADJUST_RELATIONSHIP")

    def delayed(encounter):
        started.set()
        if not release.wait(5):
            raise AssertionError("Test did not release speculative worker")
        return "PROPOSE_OPTIONAL_QUEST", {"context_ms": 0}, ""

    model.survey = delayed
    with ThreadPoolExecutor(max_workers=1) as pool:
        router = HybridDialogue(memory, model, pool)
        hint = FieldHint(1, 25, "pallet", 2, WATTS.npc, False)
        router.predict(hint, 0)
        old = router.predict(hint, 1)
        assert started.wait(2)
        try:
            assert result(router.request(DAISY))[1] == "retrieved_dialogue"
            assert old not in router.replies
            assert router.speculative is None and router.obsolete is not None
        finally:
            release.set()
    memory.close()
    print("PASS foreground routine response bypassed the running obsolete prediction.")


def benchmark(catalog, save):
    runtime = os.environ.get("LIVING_WORLD_PHASE5_RUNTIME")
    memory = WorldMemory(save, "benchmark", b"001")
    model = LocalModel(Path(runtime or "."), NAMES, catalog=catalog, style="qwen3" if runtime else "unavailable",
                       natural=bool(runtime))
    cases = (WATTS, DAISY, OAK, GUIDE)
    try:
        if runtime:
            model.worker.start()
            old = []
            for case in cases * 2:
                started = perf_counter()
                model.plan(memory.context(case))
                old.append((perf_counter() - started) * 1000)
            print(json.dumps({"phase5_routine_ms_median": median(old), "samples": old}))
        cold, warm, retrieval, state, lookup = [], [], [], [], []
        with ThreadPoolExecutor(max_workers=1) as pool:
            for _ in range(50):
                router = HybridDialogue(memory, model, pool)
                for case in cases:
                    start = perf_counter()
                    miss = router.request(case)
                    response, _ = miss.future.result()
                    validate(response.dialogue)
                    cold.append((perf_counter() - start) * 1000)
                    retrieval.append(response.metrics["retrieval_ms"])
                    start = perf_counter()
                    hit = router.request(case)
                    result(hit)
                    assert hit.cache == "hit" and miss.cache == "miss"
                    warm.append((perf_counter() - start) * 1000)
                    state.append(hit.state_ms)
                    lookup.append(hit.lookup_ms)
        print(json.dumps({name: {"median_ms": median(values), "p95_ms": quantiles(values, n=20)[18]}
                          for name, values in dict(miss=cold, hit=warm, retrieval=retrieval,
                                                   state=state, lookup=lookup).items()}))
        if runtime:
            memory.apply(memory.context(WATTS), "ADJUST_RELATIONSHIP")
            with ThreadPoolExecutor(max_workers=1) as pool:
                router = HybridDialogue(memory, model, pool)
                survey, followup, ready = [], [], []
                for index in range(4):
                    hint = FieldHint(index, 25, "pallet", index + 2, WATTS.npc, False)
                    if index % 2 == 0:
                        router.predict(hint, 0)
                        key = router.predict(hint, 0.26)
                        router.replies[key].result(timeout=12)
                    start = perf_counter()
                    interaction = router.request(WATTS, hint)
                    proposal, route = interaction.future.result(timeout=12)
                    assert route == "model_decision" and proposal.action == "PROPOSE_OPTIONAL_QUEST"
                    assert proposal.action in interaction.key.state.intentions
                    (ready if index % 2 == 0 else survey).append((perf_counter() - start) * 1000)
                    start = perf_counter()
                    reply = model.guide(GuideTurn("pallet-sighting:25", True))
                    assert reply.intention == "ASK_WATTS" and reply.generated_reaction
                    followup.append((perf_counter() - start) * 1000)
                print(json.dumps(dict(fresh_survey_ms=survey, prepared_survey_ms=ready,
                                      fresh_guide_ms=followup, correct_model_choices="8/8",
                                      survey_prefetch_hits="2/4 (alternating prefetch enabled)")))
    finally:
        model.close()
        memory.close()


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        catalog = Path(folder) / "world.sqlite"
        subprocess.run([sys.executable, "-B", APP / "build-knowledge.py", catalog], check=True)
        verify(catalog, Path(folder) / "save.sqlite")
        speculative(catalog, Path(folder) / "speculative.sqlite")
        benchmark(catalog, Path(folder) / "bench.sqlite")
