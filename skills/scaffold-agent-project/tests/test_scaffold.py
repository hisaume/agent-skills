"""Smoke-test generated files and non-destructive scaffold behaviour."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/scaffold.py"
EXPECTED = {
    "AGENTS.md",
    "GLOSSARY.md",
    "docs/specs/README.md",
    ".agents/skills/application-delivery/SKILL.md",
}


class ScaffoldTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "example"
        self.project.mkdir()

    def run_scaffold(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--target", str(self.project), *extra],
            capture_output=True, text=True, check=False,
        )

    def test_preview_and_generation(self) -> None:
        self.assertEqual(self.run_scaffold("--dry-run").returncode, 0)
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(self.run_scaffold().returncode, 0)
        self.assertTrue(all((self.project / x).is_file() for x in EXPECTED))
        self.assertFalse((self.project / ".beads").exists())
        self.assertFalse((self.project / ".agents/skills/application-delivery/references").exists())
        agent = (self.project / "AGENTS.md").read_text()
        delivery = (self.project / ".agents/skills/application-delivery/SKILL.md").read_text()
        self.assertNotIn("Beads", agent + delivery)
        self.assertIn("If `AGENTS.md` declares a tracker", delivery)
        self.assertIn("relevant contract or issue", delivery)

    def test_new_project_has_same_outputs(self) -> None:
        self.assertEqual(self.run_scaffold("--project-name", "Shared name").returncode, 0)
        original = {x: (self.project / x).read_bytes() for x in EXPECTED}
        self.project = Path(self.temp.name) / "second"
        self.project.mkdir()
        self.assertEqual(self.run_scaffold("--project-name", "Shared name").returncode, 0)
        self.assertEqual(original, {x: (self.project / x).read_bytes() for x in EXPECTED})

    def test_existing_file_blocks_before_writes(self) -> None:
        (self.project / "AGENTS.md").write_text("custom")
        result = self.run_scaffold()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.project / "AGENTS.md").read_text(), "custom")
        self.assertFalse((self.project / "GLOSSARY.md").exists())

    def test_symlinked_parent_blocks_before_writes(self) -> None:
        outside = Path(self.temp.name) / "elsewhere"
        outside.mkdir()
        (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.run_scaffold().returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_repeat_refuses_without_modification(self) -> None:
        self.assertEqual(self.run_scaffold().returncode, 0)
        before = {x: (self.project / x).read_bytes() for x in EXPECTED}
        self.assertNotEqual(self.run_scaffold().returncode, 0)
        self.assertEqual(before, {x: (self.project / x).read_bytes() for x in EXPECTED})

    def test_removed_tracker_mode_is_rejected(self) -> None:
        result = self.run_scaffold("--tracker", "beads")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.project.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
