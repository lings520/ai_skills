"""Regression tests for Git scope semantics, not model review quality.

Run: python3 -m unittest discover -s tests -p 'test_code_review_scopes.py' -v
"""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


def git(repo, *args, allowed=(0,)):
    result = subprocess.run(
        ["git", "--no-optional-locks", "-c", "core.autocrlf=false", "-c", "core.hooksPath=" + os.devnull, *args],
        cwd=repo, capture_output=True, text=True, encoding="utf-8",
        env={**{k: v for k, v in os.environ.items() if not k.startswith("GIT_")},
             "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull},
    )
    if result.returncode not in allowed:
        raise AssertionError(f"git {args!r}: {result.returncode}\n{result.stderr}")
    return result.stdout


def write(repo, name, content):
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def commit(repo, message):
    git(repo, "-c", "user.name=Scope Test", "-c", "user.email=scope@example.invalid",
        "commit", "-qm", message)
    return git(repo, "rev-parse", "HEAD").strip()


def init(repo):
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, "init", "-q", "-b", "main")


def build_fixture(repo):
    """A mixed local-state fixture, also usable for an independent review."""
    init(repo)
    write(repo, ".gitignore", "*.secret\n")
    write(repo, "discount.py", "def discounted_total(amount):\n    return amount * 0.9\n")
    write(repo, "docs/spec.md", "Apply a 10% discount: an amount of 100 must return 90.\n")
    write(repo, "notes.txt", "Original notes\n")
    write(repo, "old name.txt", "Rename this content without changing it.\n")
    write(repo, "deleted.txt", "This file is removed in the local changes.\n")
    git(repo, "add", "--", ".")
    root = commit(repo, "Initial version")
    git(repo, "switch", "-q", "-c", "feature")
    write(repo, "feature.txt", "Feature-only addition\n")
    git(repo, "add", "--", "feature.txt")
    tip = commit(repo, "Add feature")
    git(repo, "switch", "-q", "main")
    write(repo, "base-only.txt", "Change on base after the branch diverged\n")
    git(repo, "add", "--", "base-only.txt")
    base = commit(repo, "Advance base")
    git(repo, "switch", "-q", "feature")
    write(repo, "discount.py", "def discounted_total(amount):\n    return amount * 0.1\n")
    write(repo, "staged only.txt", "Staged addition\n")
    git(repo, "add", "--", "discount.py", "staged only.txt")
    git(repo, "mv", "--", "old name.txt", "new name.txt")
    git(repo, "rm", "-q", "--", "deleted.txt")
    write(repo, "discount.py", "def discounted_total(amount):\n    return amount * 0.9\n")
    write(repo, "notes.txt", "Unstaged notes\n")
    write(repo, "untracked helper.py", "VALUE = 42\n")
    write(repo, "ignored.secret", "SYNTHETIC_PLACEHOLDER\n")
    return {"root": root, "tip": tip, "base": base}


class GitIsolation(unittest.TestCase):
    def test_inherited_git_environment_does_not_redirect_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            caller = Path(tmp) / "caller"
            fixture = Path(tmp) / "fixture"
            init(caller)
            init(fixture)
            write(caller, "sentinel.txt", "keep")
            git(caller, "add", "sentinel.txt")
            before = git(caller, "ls-files", "--stage")
            overrides = {"GIT_DIR": str(caller / ".git"),
                         "GIT_WORK_TREE": str(caller),
                         "GIT_INDEX_FILE": str(caller / ".git" / "index")}
            with patch.dict(os.environ, overrides):
                self.assertEqual(Path(git(fixture, "rev-parse", "--show-toplevel").strip()), fixture)
                write(fixture, "fixture.txt", "fixture")
                git(fixture, "add", "fixture.txt")
            self.assertEqual(git(caller, "ls-files", "--stage"), before)
            self.assertEqual(git(fixture, "ls-files").strip(), "fixture.txt")


class ReviewScopes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="code-review-scope-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.refs = build_fixture(self.repo)

    def names(self, *args):
        return set(filter(None, git(self.repo, "diff", "--name-only", "-z", *args, "--").split("\0")))

    def test_staged_scope_uses_index_not_working_file(self):
        patch = git(self.repo, "diff", "--cached", "--")
        self.assertIn("+    return amount * 0.1", patch)
        self.assertIn("0.1", git(self.repo, "show", ":discount.py"))
        self.assertIn("0.9", (self.repo / "discount.py").read_text())
        self.assertIn("staged only.txt", self.names("--cached"))
        self.assertNotIn("notes.txt", self.names("--cached"))
        self.assertNotIn("untracked helper.py", self.names("--cached"))

    def test_unstaged_scope_is_index_to_working_tree(self):
        self.assertEqual(self.names(), {"discount.py", "notes.txt"})
        patch = git(self.repo, "diff", "--", "discount.py")
        self.assertIn("-    return amount * 0.1", patch)
        self.assertIn("+    return amount * 0.9", patch)

    def test_net_diff_can_hide_a_staged_defect(self):
        self.assertEqual(git(self.repo, "diff", "HEAD", "--", "discount.py"), "")
        self.assertNotEqual(git(self.repo, "diff", "--cached", "--", "discount.py"), "")
        self.assertNotEqual(git(self.repo, "diff", "--", "discount.py"), "")

    def test_untracked_inventory_preserves_spaces_and_excludes_ignored(self):
        names = git(self.repo, "ls-files", "--others", "--exclude-standard", "-z", "--")
        self.assertEqual(names.split("\0"), ["untracked helper.py", ""])
        patch = git(self.repo, "diff", "--no-index", "--", os.devnull,
                    "untracked helper.py", allowed=(1,))
        self.assertIn("+VALUE = 42", patch)

    def test_all_local_inventory_includes_layers_and_untracked(self):
        untracked = set(filter(None, git(self.repo, "ls-files", "--others",
                                        "--exclude-standard", "-z", "--").split("\0")))
        selected = self.names("--cached") | self.names() | untracked
        self.assertTrue({"discount.py", "notes.txt", "staged only.txt",
                         "new name.txt", "deleted.txt", "untracked helper.py"} <= selected)
        self.assertNotIn("ignored.secret", selected)

    def test_endpoint_and_merge_base_comparisons_differ(self):
        base, tip = self.refs["base"], self.refs["tip"]
        ancestor = git(self.repo, "merge-base", "--all", base, tip).strip()
        self.assertEqual(ancestor, self.refs["root"])
        self.assertEqual(self.names(base, tip), {"base-only.txt", "feature.txt"})
        self.assertEqual(self.names(ancestor, tip), {"feature.txt"})
        self.assertEqual(git(self.repo, "diff", f"{base}...{tip}", "--"),
                         git(self.repo, "diff", ancestor, tip, "--"))

    def test_committed_comparison_excludes_local_dirt(self):
        self.assertEqual(self.names(self.refs["root"], self.refs["tip"]), {"feature.txt"})
        self.assertIn("0.9", git(self.repo, "show", self.refs["tip"] + ":discount.py"))

    def test_path_filter_does_not_expand_scope(self):
        patch = git(self.repo, "diff", "--cached", "--", "staged only.txt")
        self.assertIn("+Staged addition", patch)
        self.assertNotIn("discount.py", patch)
        self.assertEqual(git(self.repo, "ls-files", "--others", "--exclude-standard",
                             "-z", "--", "docs/"), "")

    def test_rename_and_delete_remain_visible(self):
        status = git(self.repo, "diff", "--cached", "--name-status", "-M", "--")
        self.assertIn("D\tdeleted.txt", status)
        self.assertIn("R100\told name.txt\tnew name.txt", status)

    def test_empty_scope_and_unknown_ref_are_different(self):
        self.assertEqual(git(self.repo, "diff", self.refs["tip"], self.refs["tip"], "--"), "")
        self.assertEqual(git(self.repo, "rev-parse", "--verify", "--end-of-options",
                             "does-not-exist^{commit}", allowed=(128,)), "")

    def test_single_and_root_commits(self):
        tip, root = self.refs["tip"], self.refs["root"]
        parent = git(self.repo, "rev-parse", "--verify", "--end-of-options", tip + "^1^{commit}").strip()
        self.assertEqual(self.names(parent, tip), {"feature.txt"})
        root_patch = git(self.repo, "show", "--format=", "--root", root, "--")
        self.assertIn("+def discounted_total(amount):", root_patch)

    def test_local_review_commands_preserve_index_and_working_tree(self):
        # Compare staged entries, not cached stat metadata Git may refresh.
        before_index = git(self.repo, "ls-files", "--stage", "-z")
        before_files = {p.relative_to(self.repo): p.read_bytes()
                        for p in self.repo.rglob("*") if p.is_file() and ".git" not in p.parts}
        for args in [("diff", "--cached", "--"), ("diff", "--"), ("diff", "HEAD", "--"),
                     ("ls-files", "--others", "--exclude-standard", "-z", "--"),
                     ("show", ":discount.py")]:
            git(self.repo, *args)
        self.assertEqual(before_index, git(self.repo, "ls-files", "--stage", "-z"))
        after_files = {p.relative_to(self.repo): p.read_bytes()
                       for p in self.repo.rglob("*") if p.is_file() and ".git" not in p.parts}
        self.assertEqual(before_files, after_files)

    def test_unborn_repository(self):
        with tempfile.TemporaryDirectory(prefix="code-review-unborn-") as directory:
            repo = Path(directory)
            init(repo)
            write(repo, "new.py", "VALUE = 1\n")
            git(repo, "add", "--", "new.py")
            write(repo, "new.py", "VALUE = 2\n")
            self.assertIn("+VALUE = 1", git(repo, "diff", "--cached", "--"))
            self.assertIn("+VALUE = 2", git(repo, "diff", "--"))
            git(repo, "rev-parse", "--verify", "HEAD", allowed=(128,))


if __name__ == "__main__":
    unittest.main()
