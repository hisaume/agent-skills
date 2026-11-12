#!/usr/bin/env python3
"""Generate tracker-neutral project guidance without overwriting existing files."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "assets"
TARGETS = {
    "AGENTS.md": "AGENTS.md.template",
    "GLOSSARY.md": "GLOSSARY.md.template",
    "docs/specs/README.md": "specs-README.md.template",
    ".agents/skills/application-delivery/SKILL.md": "application-delivery-SKILL.md.template",
}


def render(path: Path, project_name: str) -> str:
    content = path.read_text(encoding="utf-8")

    def substitute(match: re.Match[str]) -> str:
        if match.group(1) != "PROJECT_NAME":
            raise ValueError(f"Unknown template token: {match.group(1)}")
        return project_name

    return re.sub(r"\{\{([A-Z_]+)\}\}", substitute, content)


def preflight(target: Path) -> None:
    for relative in TARGETS:
        current = target
        for segment in Path(relative).parts:
            current = current / segment
            if current.is_symlink():
                raise ValueError(f"Refusing symlink destination: {current}")
            if current.exists():
                if current == target / relative:
                    raise ValueError(f"Refusing existing destination: {current}")
                if not current.is_dir():
                    raise ValueError(f"Destination parent is not a directory: {current}")
        parent = (target / relative).parent
        while not parent.exists():
            parent = parent.parent
        if not os.access(parent, os.W_OK | os.X_OK):
            raise PermissionError(f"Destination parent is not writable: {parent}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Project root")
    parser.add_argument("--project-name", help="Display name; defaults to directory name")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    supplied = Path(args.target).expanduser()
    if supplied.is_symlink() or not supplied.is_dir():
        print(f"Target must be an existing non-symlink directory: {supplied}", file=sys.stderr)
        return 2
    target = supplied.resolve()
    try:
        preflight(target)
        rendered = {
            relative: render(TEMPLATE_ROOT / asset, args.project_name or target.name)
            for relative, asset in TARGETS.items()
        }
    except (OSError, ValueError) as error:
        print(f"Scaffold blocked before writing: {error}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"Would scaffold {target}:")
        for relative in TARGETS:
            print(f"  {relative}")
        return 0

    created: list[str] = []
    try:
        for relative, content in rendered.items():
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("x", encoding="utf-8") as stream:
                created.append(relative)
                stream.write(content)
            print(f"Created {relative}")
    except OSError as error:
        print(f"Scaffold incomplete: {error}", file=sys.stderr)
        print("Created (last may be incomplete): " + (", ".join(created) or "none"), file=sys.stderr)
        print("Missing: " + ", ".join(x for x in TARGETS if x not in created), file=sys.stderr)
        return 1

    print("Project guidance scaffolded; project-specific configuration remains open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
