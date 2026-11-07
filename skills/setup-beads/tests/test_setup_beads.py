"""Exercise activation, idempotency, and non-destructive refusal."""

import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/setup_beads.py"
SCAFFOLD = (
    Path(__file__).resolve().parents[2] / "scaffold-agent-project/scripts/scaffold.py"
)
VALUES = runpy.run_path(str(SCAFFOLD))["template_values"]


class SetupBeadsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.project = self.root / "rag-local"
        self.project.mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        bd = self.bin / "bd"
        bd.write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = init ]; then mkdir -p .beads; exit 0; fi\n"
            "if [ \"$1\" = prime ] && [ -d .beads ]; then exit 0; fi\n"
            "exit 3\n"
        )
        bd.chmod(0o755)
        self.env = {**os.environ, "PATH": str(self.bin) + os.pathsep + os.environ["PATH"]}
        self.create_scaffold()

    def create_scaffold(self, tracker="none"):
        v = VALUES("rag-local", tracker)
        files = {
            "AGENTS.md": (
                "# rag agent guide\n\n## Sources of truth\n\n"
                "Use `GLOSSARY.md` and docs/design/L1-PROJECT.md.\n\n"
                "## Delivery authority\n\n"
                f"- {v['TRACKER_NOTE']}\n"
                "- Do not commit, push, or sync without authorization.\n"
            ),
            ".agents/skills/application-delivery/SKILL.md": (
                "---\nname: application-delivery\n---\n"
                "\n## Read what the task needs\n"
                f"4. {v['TRACKER_ROUTE']}\n"
                "\n## Boundaries\n"
                f"- {v['TRACKER_BOUNDARY']}\n"
            ),
            ".agents/skills/application-delivery/references/workflow.md": (
                f"# {v['WORKFLOW_TITLE']}\n\n## Start durable work\n\n"
                f"{v['TRACKER_STEPS']}\n\n## Deliver work\n"
                "Do not commit without authorization.\n"
            ),
        }
        for name, content in files.items():
            dest = self.project / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)

    def run_setup(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--target", str(self.project), *args],
            env=self.env, capture_output=True, text=True,
        )

    def test_activation_and_idempotence(self):
        agents = self.project / "AGENTS.md"
        prior = agents.read_text()
        dry = self.run_setup("--dry-run")
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertEqual(prior, agents.read_text())
        self.assertFalse((self.project / ".beads").exists())

        first = self.run_setup()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertTrue((self.project / ".beads").exists())
        self.assertTrue((self.project / "docs/agents/issue-tracker.md").exists())
        self.assertNotIn("No durable tracker", agents.read_text())
        self.assertIn("GLOSSARY.md", agents.read_text())
        self.assertIn("Beads workflow", (
            self.project / ".agents/skills/application-delivery/references/workflow.md"
        ).read_text())
        self.assertIn("Beads is selected", agents.read_text())

        snapshot = [p.read_bytes() for p in (
            agents,
            self.project / "docs/agents/issue-tracker.md",
            self.project / ".agents/skills/application-delivery/SKILL.md",
            self.project / ".agents/skills/application-delivery/references/workflow.md",
        )]
        self.assertEqual(self.run_setup().returncode, 0)
        self.assertEqual(snapshot, [p.read_bytes() for p in (
            agents,
            self.project / "docs/agents/issue-tracker.md",
            self.project / ".agents/skills/application-delivery/SKILL.md",
            self.project / ".agents/skills/application-delivery/references/workflow.md",
        )])

    def test_preselected_beads_only_adds_tracker_contract(self):
        self.create_scaffold(tracker="beads")
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.project / "docs/agents/issue-tracker.md").exists())
        self.assertEqual((self.project / "AGENTS.md").read_text().count("Beads is selected"), 1)

    def test_missing_local_delivery_skill_refuses_before_init(self):
        (self.project / ".agents/skills/application-delivery/SKILL.md").unlink()
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.project / ".beads").exists())

    def test_modified_tracker_rule_refuses_before_init(self):
        agent = self.project / "AGENTS.md"
        agent.write_text(agent.read_text().replace("No durable tracker is configured.", "No issues please."))
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.project / ".beads").exists())

    def test_existing_custom_beads_contract_preserved(self):
        self.assertEqual(self.run_setup().returncode, 0)
        issue = self.project / "docs/agents/issue-tracker.md"
        issue.write_text("# Issue tracker\n\nBeads is tracked here with personal conventions.\n")
        self.assertEqual(self.run_setup().returncode, 0)
        self.assertIn("personal conventions", issue.read_text())

    def test_failed_beads_verification_does_not_patch_guidance(self):
        agent = self.project / "AGENTS.md"
        before = agent.read_text()
        (self.bin / "bd").write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = init ]; then mkdir -p .beads; exit 0; fi\n"
            "exit 6\n"
        )
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, agent.read_text())
        self.assertFalse((self.project / "docs/agents/issue-tracker.md").exists())

    def test_symlinked_beads_refused(self):
        (self.project / ".beads").symlink_to(self.root)
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symlink", result.stderr)


if __name__ == "__main__":
    unittest.main()
