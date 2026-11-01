---
name: debug
description: Investigate software failures, incorrect behaviour, intermittent bugs, and performance regressions. Use when the user asks to debug or diagnose a problem, or fix a reported bug; match diagnosis and changes to the requested scope.
---

# Debug

Establish the cause with evidence, then verify any authorized fix against the reported symptom. Scale the investigation to the uncertainty and impact: a clear defect may need one targeted check; a difficult incident may need repeated experiments.

## Establish scope and the failure

- Identify expected versus actual behaviour, relevant inputs, environment/version, and any recent change. Inspect applicable repository instructions, nearby tests, and relevant glossary or architecture decisions. Ask only for missing information that materially blocks progress.
- Honour the requested outcome. For diagnosis-only requests, investigate and recommend without changing project files. Use disposable artifacts for experiments. If a fix is requested, proceed with the necessary focused changes. For an ambiguous “debug this”, begin diagnosis; clarify before modifying project files if repair intent remains unclear.
- Preserve existing work. Use an isolated copy or worktree for historical comparisons and bisection. Keep production instrumentation, traffic replay, stress tests, and external writes within the user's authorization; a debugging request alone does not authorize those actions.
- Redact credentials and personal data from commands, logs, traces, and shared artifacts. Inspect captured requests before replaying them; they can contain secrets and trigger side effects.

## Build evidence

Seek the smallest practical check that distinguishes the reported failure from correct behaviour: an existing test, CLI invocation, request, browser action, or disposable harness. Record what was actually run and its observed result. A setup error is not reproduction of the user's bug.

Read code, logs, and configuration as needed to design that check. A runnable reproduction is preferred, not a prerequisite for useful investigation. If execution is unavailable, continue with available evidence, label hypotheses as unconfirmed, and identify the next discriminating check or missing artifact. Do not claim reproduction or a verified fix without observing it.

Once the failure is reproduced, remove inputs or steps when doing so helps distinguish causes or produce a maintainable regression test. Preserve the original scenario. Stop reducing when further minimization costs more than it adds; a mathematically minimal reproduction is not required.

For intermittent failures, performance regressions, historical bisection, or human-assisted reproduction, consult [investigation-modes.md](references/investigation-modes.md).

## Test explanations

- Start with the best-supported explanation. Consider alternatives when evidence is ambiguous or an experiment contradicts it; there is no required hypothesis count.
- Tie each candidate cause to a prediction and a check that could refute it. Change one relevant variable at a time where practical, and record which explanations the result supports or weakens.
- Use a debugger, focused logging, or a profiler where it separates competing explanations. Track temporary instrumentation so only additions from this investigation are removed later.
- Distinguish the observed symptom, the causal mechanism, and contributing conditions. A correlation or passing check after an unrelated edit does not establish a cause.

For longer investigations, briefly explain the leading hypothesis and next check. If experiments stop producing new evidence, summarize what was ruled out and choose a different evidence source or ask for the specific missing access/input. Avoid open-ended retries of the same probe.

## Fix and verify when requested

1. Identify the smallest correction that addresses the supported cause. Keep unrelated refactoring separate.
2. For a code defect with a suitable test boundary, capture the actual failure in a regression test and observe it fail before applying the fix. If the fix is already present, compare against the failing version in isolation. Verify that the test fails for the intended reason.
3. Apply the focused fix. Run the regression test, repeat the original scenario, and run relevant nearby checks. Confirm the test exercises the triggering interactions and would catch a recurrence; a shallow test can give false confidence.
4. If an automated regression test is impractical, document the limitation and the strongest available verification, such as a configuration check or manual reproduction. Do not expand into architectural redesign solely to create a test.
5. Remove temporary instrumentation and disposable artifacts created for this investigation, retaining useful regression fixtures. Preserve pre-existing diagnostics and user changes. Inspect the final diff for accidental edits and sensitive data.

## Report

Lead with the cause and outcome, or the leading hypothesis if unresolved. Include the decisive evidence and relevant file locations, changes made when applicable, checks actually performed, and any remaining uncertainty or next step. Keep straightforward fixes short. Distinguish **diagnosed**, **fixed**, and **verified**; report partial verification explicitly. Commit, publication, and deployment follow the user's authorization, not this skill's invocation alone.

Adapted from [Matt Pocock's diagnosing-bugs skill](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/diagnosing-bugs/SKILL.md). Upstream copyright and permission notice: [LICENSE](LICENSE).
