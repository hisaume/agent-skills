"""Regression checks for baseline generation and preservation."""

import importlib.util
import json
import platform
import tempfile
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "scaffold.py"
SPEC = importlib.util.spec_from_file_location("scaffold", SCRIPT)
assert SPEC and SPEC.loader
scaffold = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scaffold)


class GeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / "My App"
        self.target.mkdir()
        self.inputs = {
            "python": platform.python_version(),
            "uv_build": "0.11.32",
            "dependencies": {"mypy": "2.4.0", "pytest": "9.1.1", "ruff": "0.17.0"},
        }

    def create(self) -> None:
        scaffold.execute("create", self.target, self.inputs)

    def test_create_verify_and_detect_drift(self) -> None:
        self.create()
        scaffold.execute("verify", self.target, self.inputs)
        config = tomllib.loads((self.target / "pyproject.toml").read_text())
        self.assertEqual(config["project"]["name"], "my-app")
        self.assertEqual(
            config["project"]["scripts"], {"my-app": "my_app.__main__:main"}
        )
        path = self.target / "src/my_app/__main__.py"
        path.write_text("changed\n")
        with self.assertRaisesRegex(ValueError, "Baseline changed"):
            scaffold.execute("verify", self.target, self.inputs)

    def test_preserve_gitignore_and_append_once(self) -> None:
        path = self.target / ".gitignore"
        path.write_text("custom/\n.venv/")
        self.create()
        text = path.read_text()
        self.assertTrue(text.startswith("custom/\n.venv/\n"))
        self.assertEqual(text.splitlines().count(".venv/"), 1)
        scaffold.execute("verify", self.target, self.inputs)

    def test_collision_prevents_all_baseline_writes(self) -> None:
        (self.target / "tests").mkdir()
        path = self.target / "tests/test_smoke.py"
        path.write_text("preserve")
        with self.assertRaisesRegex(ValueError, "Refusing existing"):
            self.create()
        self.assertFalse((self.target / "pyproject.toml").exists())
        self.assertEqual(path.read_text(), "preserve")

    def test_symlink_prevents_writes(self) -> None:
        (self.target / "src").symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.create()
        self.assertFalse((self.target / "pyproject.toml").exists())

    def test_symlink_gitignore_is_not_appended(self) -> None:
        outside = self.root / "outside"
        outside.write_text("preserve")
        (self.target / ".gitignore").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.create()
        self.assertEqual(outside.read_text(), "preserve")

    def test_prerelease_and_mismatched_runtime_rejected(self) -> None:
        for version in ["3.15.0b4", "3.15.0rc1", "99.0.0"]:
            with self.subTest(version=version):
                self.inputs["python"] = version
                with self.assertRaises(ValueError):
                    self.create()
                self.assertEqual(list(self.target.iterdir()), [])

    def test_actual_prerelease_runtime_rejected(self) -> None:
        with patch.object(
            scaffold.sys, "version_info", SimpleNamespace(releaselevel="beta")
        ):
            with self.assertRaisesRegex(ValueError, "selected final CPython"):
                self.create()

    def test_names_are_valid_imports(self) -> None:
        for name, package in [
            ("123 App", "app_123_app"),
            ("class", "class_app"),
            ("!!!", "python_app"),
        ]:
            with self.subTest(name=name):
                target = self.root / name
                target.mkdir()
                output = scaffold.render(target, self.inputs)
                self.assertIn(f"src/{package}/__main__.py", output)
                self.assertEqual(
                    compile(
                        output[f"src/{package}/__main__.py"], "entry", "exec"
                    ).co_name,
                    "<module>",
                )

    def test_parent_workspace_rejected_without_mutation(self) -> None:
        path = self.root / "pyproject.toml"
        path.write_text('[tool.uv.workspace]\nmembers = ["*"]\n')
        original = path.read_bytes()
        with self.assertRaisesRegex(ValueError, "parent uv workspace"):
            self.create()
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_verify_checks_executable_permission(self) -> None:
        self.create()
        (self.target / "check.sh").chmod(0o644)
        with self.assertRaisesRegex(ValueError, "executable"):
            scaffold.execute("verify", self.target, self.inputs)

    def test_json_formatting_is_not_baseline_drift(self) -> None:
        self.create()
        path = self.target / ".vscode/launch.json"
        path.write_text(json.dumps(json.loads(path.read_text()), sort_keys=True))
        scaffold.execute("verify", self.target, self.inputs)


if __name__ == "__main__":
    unittest.main()
