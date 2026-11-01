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

### `visualization-design`

A technology-agnostic visualization design layer that helps the agent:

- choose charts based on analytical purpose, audience, and data structure;
- represent uncertainty with error bars, intervals, and uncertainty bands;
- surface caveats such as small samples, sampling bias, unstable estimates, and short backtest histories;
- preserve honest scales, labels, units, denominators, and comparisons;
- design for accessibility and the requested end product; and
- route implementation choices to Python, notebooks, static HTML, TypeScript, dashboards, reports, or presentations.

### Engineering: `code-review`

Adapted from [Matt Pocock's code-review skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/code-review), with its [MIT notice](engineering/code-review/LICENSE) preserved. It reviews:

- staged, unstaged, and all uncommitted changes, including untracked files where requested;
- exact commit-to-commit differences or branch/PR changes since their merge base;
- project standards and intended behaviour as separate axes, with evidence-backed findings; and
- the correct staged or historical file versions without changing the working tree.

No issue tracker is required. Review requests do not authorize fixes, commits, or posted reviews. Examples: “review staged changes”, “review all my local changes”, or “compare commits A and B”.

Scope-command regression tests: `python3 -m unittest discover -s tests -p 'test_code_review_scopes.py' -v`. These verify Git selection semantics, not model review quality.

## Installation

Copy the individual skill folder into the Codex skills directory. For example, copy `engineering/code-review` as `code-review`:

```text
%USERPROFILE%\\.codex\\skills\\<skill-name>
```

Invoke a skill explicitly with its name, for example:

```text
$html-research-report
```

Skills may also be discovered automatically when a request matches their descriptions.
