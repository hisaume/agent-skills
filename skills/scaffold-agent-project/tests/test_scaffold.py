"""Verify destination safety, defaults, and generated delivery policy."""

import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "scaffold", Path(__file__).resolve().parents[1] / "scripts/scaffold.py"
)
assert SPEC and SPEC.loader
scaffold = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scaffold)


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / "project"
        self.target.mkdir()

    def run_scaffold(self, *options):
        output, errors = io.StringIO(), io.StringIO()
        argv = ["scaffold", "--target", str(self.target), *options]
        with (
            patch.object(sys, "argv", argv),
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(errors),
        ):
            status = scaffold.main()
        return status, output.getvalue(), errors.getvalue()

    def test_default_is_tracker_free_and_deterministic(self):
        self.assertEqual(self.run_scaffold("--dry-run")[0], 0)
        self.assertEqual(list(self.target.iterdir()), [])
        self.assertEqual(self.run_scaffold()[0], 0)
        expected = {
            name: (self.target / name).read_bytes() for name in scaffold.TARGETS
        }
        workflow = expected[
            ".agents/skills/application-delivery/references/workflow.md"
        ].decode()
        guide = expected["AGENTS.md"].decode()
        self.assertIn("No durable tracker is configured", guide)
        self.assertNotIn("bd prime", workflow)
        self.assertNotIn("Inspect and claim work", workflow)
        self.assertNotIn("Close work", workflow)
        self.assertIn("Check: not configured", guide)
        self.assertIn("Do not commit, push, open pull requests", guide)
        self.target = self.root / "second" / "project"
        self.target.mkdir(parents=True)
        self.assertEqual(self.run_scaffold()[0], 0)
        self.assertEqual(
            expected,
            {name: (self.target / name).read_bytes() for name in scaffold.TARGETS},
        )

    def test_tracker_modes(self):
        for mode, phrase in [
            ("beads", "Run `bd prime`"),
            ("repository", "repository's tracker guidance"),
        ]:
            self.target = self.root / mode
            self.target.mkdir()
            self.assertEqual(self.run_scaffold("--tracker", mode)[0], 0)
            text = (
                self.target
                / ".agents/skills/application-delivery/references/workflow.md"
            ).read_text()
            self.assertIn(phrase, text)
            self.assertFalse((self.target / ".beads").exists())

    def test_symlink_parents_and_dangling_entries_refused(self):
        for kind in ["parent", "dangling", "target"]:
            self.target = self.root / kind
            self.target.mkdir()
            outside = self.root / f"outside-{kind}"
            if kind == "parent":
                outside.mkdir()
                (self.target / "docs").symlink_to(outside, target_is_directory=True)
            elif kind == "dangling":
                (self.target / "AGENTS.md").symlink_to(outside)
            else:
                self.target.rmdir()
                outside.mkdir()
                self.target.symlink_to(outside, target_is_directory=True)
            for options in [("--dry-run",), ()]:
                self.assertNotEqual(self.run_scaffold(*options)[0], 0)
            self.assertFalse((self.target / "CONTEXT.md").exists())
            if outside.exists():
                self.assertEqual(list(outside.iterdir()), [])

    def test_parent_file_refused_before_writes(self):
        (self.target / ".agents").write_text("preserve")
        self.assertNotEqual(self.run_scaffold("--dry-run")[0], 0)
        self.assertNotEqual(self.run_scaffold()[0], 0)
        self.assertEqual([p.name for p in self.target.iterdir()], [".agents"])

    def test_unwritable_parent_refused_before_writes(self):
        with patch.object(scaffold.os, "access", return_value=False):
            status, _, error = self.run_scaffold("--dry-run")
        self.assertEqual(status, 1)
        self.assertIn("not writable", error)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_existing_guidance_preserved(self):
        (self.target / "AGENTS.md").write_text("preserve")
        self.assertEqual(self.run_scaffold()[0], 1)
        self.assertEqual((self.target / "AGENTS.md").read_text(), "preserve")
        self.assertEqual([p.name for p in self.target.iterdir()], ["AGENTS.md"])

    def test_missing_template_refused_before_writes(self):
        with patch.object(scaffold, "TEMPLATE_ROOT", self.root / "missing"):
            self.assertEqual(self.run_scaffold()[0], 1)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_exclusive_creation_preserves_racing_file(self):
        real_open = Path.open
        raced = False

        def open_with_race(path, mode="r", *args, **kwargs):
            nonlocal raced
            if mode == "x" and path.name == "CONTEXT.md" and not raced:
                raced = True
                with real_open(path, "w") as stream:
                    stream.write("concurrent content")
            return real_open(path, mode, *args, **kwargs)

        with patch.object(Path, "open", open_with_race):
            status, _, error = self.run_scaffold()
        self.assertEqual(status, 1)
        self.assertEqual((self.target / "CONTEXT.md").read_text(), "concurrent content")
        self.assertIn("Created entries", error)
        self.assertIn("AGENTS.md", error)
        self.assertIn("Not created: CONTEXT.md", error)
        self.assertNotIn("Traceback", error)

    def test_with_beads_implies_beads_and_reports_failed_delegation(self):
        setup = self.root / "setup.py"
        setup.write_text("# fixture")
        with (
            patch.object(scaffold, "SETUP_BEADS_SCRIPT", setup),
            patch.object(scaffold.shutil, "which", return_value="bd"),
            patch.object(
                scaffold.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 7),
            ) as run,
        ):
            status, _, error = self.run_scaffold("--with-beads")
        self.assertEqual(status, 7)
        self.assertIn("Beads setup failed", error)
        self.assertIn("setup-beads separately", error)
        self.assertTrue(all((self.target / name).exists() for name in scaffold.TARGETS))
        run.assert_called_once_with(
            [sys.executable, str(setup), "--target", str(self.target)], check=False
        )

    def test_beads_preview_and_compatibility_alias_do_not_initialize(self):
        setup = self.root / "setup.py"
        setup.write_text("# fixture")
        with (
            patch.object(scaffold, "SETUP_BEADS_SCRIPT", setup),
            patch.object(scaffold.shutil, "which", return_value="bd"),
            patch.object(scaffold.subprocess, "run") as run,
        ):
            status, output, _ = self.run_scaffold("--initialize-beads", "--dry-run")
        self.assertEqual(status, 0)
        self.assertIn("tracker=beads", output)
        self.assertEqual(list(self.target.iterdir()), [])
        run.assert_not_called()

    def test_incompatible_tracker_and_beads_setup_refused(self):
        self.assertEqual(self.run_scaffold("--tracker", "none", "--with-beads")[0], 2)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_proportionality_keeps_validation_and_consequential_planning(self):
        self.assertEqual(self.run_scaffold()[0], 0)
        text = (
            self.target / ".agents/skills/application-delivery/SKILL.md"
        ).read_text()
        self.assertIn("small, well-understood changes with bounded impact", text)
        self.assertIn("do not create a specification or vertical-slice", text)
        self.assertIn("consequential contract changes", text)
        self.assertIn("Escalate uncertainty or risk", text)
        self.assertIn("validation command before handoff", text)
        self.assertNotIn("{{", text)


if __name__ == "__main__":
    unittest.main()
