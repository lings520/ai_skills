# Debug behaviour checks

Run each case in a fresh session with `engineering/debug/SKILL.md`, an isolated workspace, and the stated request. Score observable actions and evidence, not exact wording. These are manual scenarios, not an automated benchmark. Keep expected behaviour separate from the evaluating agent's prompt.

| Case | Setup and request | Expected behaviour |
| --- | --- | --- |
| Diagnosis only | Python `elapsed(start, end)` returns `(end-start).seconds`. Ask: “Diagnose why a 25-hour job is reported as 3600 seconds. Do not change project files.” | Reproduces with a suitable input, explains day truncation, recommends a correction, preserves all project files. No invented hypothesis quota. |
| Focused fix | Same fixture. Ask: “Fix elapsed duration reporting and add a regression test.” | Captures the failure before fixing; checks the full duration and nearby behaviour; verifies the original scenario; avoids unrelated changes. |
| Logs only | No application or environment. Supply: `12:00 deploy v2; 12:01 request a: pool wait timeout; 12:02 request b: pool wait timeout`. Ask for diagnosis and next checks. | Uses logs without demanding a runnable reproduction first; distinguishes observed timeouts from possible causes; proposes checks that separate hypotheses; does not invent a confirmed root cause or fix. |
| Intermittent failure | Supply baseline 2 failures / 100 runs and post-change 0 / 10, with no runnable system. Ask whether it is fixed. | Reports insufficient evidence, retains uncertainty, and proposes bounded comparable follow-up; no claim that zero observed failures proves success. |
| Performance | Supply a cold baseline run of 800 ms and a warm post-change run of 300 ms. Ask whether the change improved performance. | Flags incomparable conditions and a single sample per condition; proposes comparable repeated measurements and correctness checks. |

For diagnosis-only checks, compare project-file hashes before and after. For fixes, inspect the diff and observe both failing and passing test results. Record model, date, skill revision, commands/results, and limitations when retaining an evaluation result.
