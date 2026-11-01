# Git review scopes

Choose the comparison the user requested. Run from the repository root, pass paths after `--`, and quote revision/path arguments. Prefer `git --no-optional-locks` for read-only inspections to avoid optional lock-taking operations. The commands below abbreviate that prefix and omit optional path filters. Use `--no-ext-diff --no-textconv` on `git diff` and `git show` when inspecting an untrusted repository to avoid invoking configured diff helpers.

## Local changes

| Request | Evidence | Reviewed version |
| --- | --- | --- |
| Staged only | `git diff --cached --` | Index; read full files with `git show ':path/to/file'` |
| Unstaged only | `git diff --` | Working tree compared with index; excludes untracked files |
| All uncommitted/local changes | Both commands above, plus `git ls-files --others --exclude-standard -z --` | Review the staged snapshot and the subsequent working-tree changes; inspect eligible untracked files as additions |

For all-local reviews, `git diff HEAD --` gives a useful net tracked-file view, but is not sufficient by itself: an unstaged reversal can hide a defect still present in the next staged commit. Identify findings as staged-only or present in the final working tree, and do not report the same defect twice. If the user explicitly wants only the final working-tree result, use the net view plus eligible untracked files and say that intermediate staged content is excluded.

Untracked files do not appear in ordinary diffs. Read relevant non-ignored files directly, or use `git diff --no-index -- /dev/null "path/to/file"` (with the platform's null-device equivalent). Exit code 1 means differences, not failure. Honour path filters, treat names from `-z` output as NUL-delimited, and do not stage files merely to include them. Report any excluded generated, binary, sensitive, or large files rather than silently claiming full coverage. Untracked files enter an unstaged-only review only if the user also requests them.

On a repository with no commits, `git diff --cached --` still shows staged additions; `git diff --` still compares working files with the index. Skip the net `HEAD` command and state that there is no HEAD yet. If files are unmerged, flag those paths and the incomplete review; do not resolve the conflicts.

## Commits, branches, and PRs

Resolve each supplied ref with `git rev-parse --verify --end-of-options "${ref}^{commit}"`; use the resulting commit IDs below. An unknown ref is a blocker for that comparison, not permission to substitute HEAD.

| Request | Comparison |
| --- | --- |
| Between A and B; explicit `A..B` | `git diff "$A" "$B" --` — exact endpoint snapshots, in the requested direction |
| Changes introduced on a branch/PR relative to BASE | Find the common ancestor with `git merge-base --all "$BASE" "$TIP"`, then `git diff "$MERGE_BASE" "$TIP" --` |
| Explicit `A...B` | The merge-base comparison above, with A as BASE and B as TIP |
| Since A, up to the current commit | `git diff "$A" "$TIP" --`, where TIP is the captured HEAD |
| Since A, including current local work | Net `git diff "$A" --`, plus staged/unstaged patches and eligible untracked files to retain local-layer visibility |
| One ordinary commit C | Resolve C's parent, then `git diff "$PARENT" "$C" --` |

Endpoint comparison and merge-base comparison differ when histories diverge. Do not replace one with the other. For “since A” without an established meaning, state the endpoint-to-HEAD interpretation; ask if the conversation instead suggests branch-only or local-inclusive changes. For PRs, obtain the actual base/head from PR metadata; do not guess the base branch name or review a synthetic merge ref as though it were the head.

If no merge base exists, or multiple merge bases are returned, explain the ambiguity and ask for a baseline. For a merge commit reviewed alone, ask which parent/comparison is intended unless already specified. For a root commit, use `git show --format= --root "$C" --` to inspect its additions.

Read full historical files with `git show "${TIP}:path/to/file"` (B or C for other modes). Review deletions against the old side; use name/status output with rename detection when matching old/new paths. Local dirt is excluded from committed comparisons unless explicitly requested. A single endpoint diff describes the net result, not every intermediate commit; review each commit separately when the user asks for commit-by-commit review.

An empty selected diff is a valid result: report no changes in that scope. Check the selected local layers/untracked inventory before calling an all-local review empty. Missing history, unavailable PR metadata, submodule contents, or truncated patches require an explicit coverage caveat, not an inferred clean result.

Command semantics: [git diff](https://git-scm.com/docs/git-diff), [git ls-files](https://git-scm.com/docs/git-ls-files).
