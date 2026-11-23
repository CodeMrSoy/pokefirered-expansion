# Phase 16 offline planner results

The three Q4_K_M workers saw identical starting conditions for six 72-hour
trials. Each model had up to nine decisions per trial and used greedy
decoding. Each decision journal records perceived facts, output, offered
primitives, forecast effects, and validation. Timings measure a complete
decision including all its inference calls and setup when a worker started.
Peak memory measures the model worker's resident bytes. The Linux host was
an AMD EPYC 9V74 with the existing single-threaded worker.

| Model | Decisions | Nonempty plans | Plans with multiple actions | Newly reached goal predicates | Median | Peak RSS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen3 0.6B | 52 | 36 | 3 | 6 | 3.87 s | 738 MiB |
| Gemma 3 1B IT | 45 | 41 | 9 | 11 | 7.54 s | 1,003 MiB |
| Qwen3 1.7B | 53 | 21 | 0 | 9 | 10.07 s | 1,860 MiB |

A newly reached predicate was false when its plan was queued. Counts include
goals satisfied across planning turns or by other residents' actions.
The benchmark distinguishes this mechanical achievement from the larger
scenario objective. No worker errors occurred in these Linux cases. None
of the queued multi-action plans reached a previously unmet predicate.
The successful longer sequences used distinct planning turns with new
observations in between.

| Starting condition and measured result | Qwen3 0.6B | Gemma 3 1B IT | Qwen3 1.7B |
| --- | --- | --- | --- |
| Ordinary shift, at least one declared predicate reached | Reached | Reached | Reached |
| Potion shortage, lead obtains Potion or Mart gains tradeable stock | Missed | Missed | Missed |
| Jobless with no cash, lead takes a job | Reached | Missed | Reached |
| Unskilled lead, another actor answers the lead's request and teaches retail | Missed | Missed | Missed |
| Unhoused lead, obtains a new home | Reached | Missed | Missed |
| Optional route closure, lead departs for Cerulean | Missed | Missed | Missed |

**Goal quality and follow-through.** Access, skill and resource constraints
filtered infeasible steps, which explains mechanically valid plans. Qwen3
0.6B often used its identity as its ambition. Qwen3 1.7B sometimes wrote an
employment ambition but picked a shopping predicate. Gemma completed more
predicates, including incidental trips and purchases, while meeting fewer
scenario objectives. On one extended run a resident bought and sold the
same Potion several times, losing money while pursuing an Antidote.

**Adaptation and cooperation.** Requests without responses expired and
triggered new decisions. The six-case benchmark failed to resolve cooperation
within its decision budget. The 30-day trace, with a different budget, records
a successful teaching exchange and its employment consequence. In the route
closure case, the direct route disappeared from the local action choices
until reopening. No model demonstrated that it could maintain and reroute a
trip to Cerulean. Nobody resolved the shortage objective within the standard
budget.

In a [separate route closure trial](route-closure-replan.jsonl.gz), a
Qwen3 0.6B resident selected travel to its intended guest house. An event
closed the optional lane before the queued trip executed. The validator
rejected the step, and the resident immediately selected a different
destination. It arrived there and abandoned its original housing goal.
The lane reopened at hour 13. All 82 revisions replayed.

**Knowledge.** Private cash, skills and intentions of other residents were
excluded from their neighbors' observations. Forecasts stop at hypothetical
travel until the actor actually arrives. No benchmark exposed private peer
state, but constrained inputs and the grammar make this a simulator boundary
test. They provide limited evidence about a model's independent ability to
respect epistemic limits.

The data support keeping the existing bundled weights. This small benchmark
shows concrete success on employment and relocation under local constraints
and significant weaknesses in open-ended planning. The larger tested models
cost more time and memory, with mixed improvements on declared predicates and
weaker results on the defined outcomes.

## Native Windows check

The [Windows CI report](phase16-windows-report.zip) contains the native
package smoke result, the Phase 15 inference regression, and the Phase 16
cooperation case for all three models. The same checked package and its
offline worker ran each model on Windows Server 2022. This narrower trial
used four decisions before reload and two after reload.

| Model | Nonempty plans / decisions | Median decision | Peak working set | Cooperation objective |
| --- | ---: | ---: | ---: | --- |
| Qwen3 0.6B | 4 / 6 | 11.86 s | 512 MiB | Missed |
| Gemma 3 1B IT | 6 / 6 | 33.33 s | 892 MiB | Missed |
| Qwen3 1.7B | 3 / 6 | 36.11 s | 1,199 MiB | Missed |

All three completed inference within this trial's per-call budget. Median
decision time includes multiple inference calls where the planner chose
multiple steps. The package smoke and all companion CI jobs passed.
[GitHub Actions run](https://github.com/CodeMrSoy/pokefirered-expansion/actions/runs/45154275224)
