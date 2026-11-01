# Investigation modes

Use the relevant branch alongside the main debugging workflow.

## Intermittent failures

Record failures and attempts, environment, inputs, seed, concurrency, and timing where observable. Repeated runs can estimate the failure rate; choose a bounded run count and cost appropriate to the system. Seed randomness or control scheduling when possible.

Increase the reproduction rate in an isolated environment if useful. Stress or injected delays can change the failure mechanism, so confirm that the resulting symptom matches the original. Rare failures remain investigable through logs, traces, and code reasoning. Zero failures in a small number of attempts does not prove a fix; report before/after counts and residual uncertainty.

## Performance regressions

Define the metric, workload, and comparison before changing code: latency, throughput, memory, or another reported symptom. Compare under similar hardware, versions, data volumes, cache/warm-up conditions, and concurrency. Repeat measurements enough to distinguish the signal from run-to-run noise; include counts and spread rather than only the best run.

Use profiling or query plans to locate the work behind the regression. Confirm correctness alongside speed. If the environment cannot support a representative benchmark, report the limitation instead of asserting a performance improvement.

## Historical comparisons and bisection

Confirm a known-good and known-bad state using the same meaningful check. Work in isolation so the user's branch, index, and working files remain intact. Historical builds may need different dependencies or configuration; mark untestable revisions as skipped rather than treating build failures as the reported defect. Bisection identifies a candidate change; inspect and verify its causal connection.

## Human-assisted or unavailable reproduction

When only the user can perform a step, give a short sequence and request the specific observable result, with redaction guidance. Use the available interaction channel; a particular shell or template is not required. Avoid repeatedly asking the user to repeat an unchanged experiment.

With only logs, traces, or source, separate direct observations from inferences. Explain what each proposed check would distinguish. Ask for the smallest missing artifact or access needed to advance, and continue useful investigation with the evidence already available. Production-only instrumentation requires authorization and a bounded collection and cleanup plan.
