# AI Skills

Reusable Codex skills for focused, accurate, and well-presented work.

## Included skills

### `task-quality-control`

A general quality layer for task execution. It helps the agent:

- stay within scope and avoid unrelated work;
- surface material assumptions and ambiguities;
- distinguish facts, estimates, interpretations, and recommendations;
- verify important claims, calculations, dates, units, and comparisons; and
- review the result before presenting a concise, logical response.

### `html-research-report`

Guidance for research reports delivered as HTML. It provides conventions for:

- a linked table of contents and clear section hierarchy;
- concise bullet-point synthesis where appropriate;
- evidence-backed footnotes and references;
- purposeful, labeled, accessible figures and plots; and
- valid, self-contained, responsive HTML.

## Installation

Copy a skill folder into the Codex skills directory:

```text
%USERPROFILE%\\.codex\\skills\\<skill-name>
```

Invoke a skill explicitly with its name, for example:

```text
$html-research-report
```

Skills may also be discovered automatically when a request matches their descriptions.
