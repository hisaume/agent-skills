#!/usr/bin/env python3
"""Create a non-destructive standard agent-guidance layout in a project root."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "assets"
SETUP_BEADS_SCRIPT = (
    Path(__file__).resolve().parents[2] / "setup-beads" / "scripts" / "setup_beads.py"
)
TARGETS = {
    "AGENTS.md": "AGENTS.md.template",
    "CONTEXT.md": "CONTEXT.md.template",
    "docs/specs/README.md": "specs-README.md.template",
    ".agents/skills/application-delivery/SKILL.md": "application-delivery-SKILL.md.template",
    ".agents/skills/application-delivery/references/workflow.md": "workflow.md.template",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        default=".",
        help="Project root to scaffold (default: current directory).",
    )
    parser.add_argument(
        "--project-name", help="Display name; defaults to the target directory name."
    )
    parser.add_argument("--tracker", choices=("beads", "none"), default="beads")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned files without writing them.",
    )
    beads = parser.add_mutually_exclusive_group()
    beads.add_argument(
        "--with-beads",
        action="store_true",
        help="After scaffolding, run the standalone local Beads setup. Requires --tracker beads.",
    )
    beads.add_argument(
        "--initialize-beads",
        dest="with_beads",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def template_values(project_name: str, tracker: str) -> dict[str, str]:
    if tracker == "beads":
        return {
            "PROJECT_NAME": project_name,
            "TRACKER_LABEL": "Beads",
            "TRACKER_NOTE": "This project uses Beads for durable work. Run `bd prime` when tracker context is needed; do not use markdown TODO files as the project tracker.",
            "TRACKER_ROUTE": "For durable Beads work, read `references/workflow.md`.",
            "WORKFLOW_TITLE": "Beads workflow",
            "TRACKER_STEPS": "1. Run `bd prime`.\n2. Find work with `bd ready`, inspect it with `bd show <id>`, and claim it with `bd update <id> --claim`.\n3. Record follow-up work and dependencies in Beads.\n4. Close an issue only after its repository-defined completion and integration gates pass.",
        }
    return {
        "PROJECT_NAME": project_name,
        "TRACKER_LABEL": "the repository-declared tracker",
        "TRACKER_NOTE": "Record durable work in the tracker declared by this repository. Do not create a second markdown TODO system.",
        "TRACKER_ROUTE": "Read `references/workflow.md` for the delivery lifecycle.",
        "WORKFLOW_TITLE": "Delivery workflow",
        "TRACKER_STEPS": "1. Read the repository's tracker guidance.\n2. Inspect and claim work before implementation.\n3. Record follow-up work and dependencies in that tracker.\n4. Close work only after its repository-defined completion and integration gates pass.",
    }


def render(template_path: Path, values: dict[str, str]) -> str:
    content = template_path.read_text(encoding="utf-8")
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        print(f"Target is not a directory: {target}", file=sys.stderr)
        return 2
    if args.with_beads and args.tracker != "beads":
        print("--with-beads requires --tracker beads.", file=sys.stderr)
        return 2
    if args.with_beads and not SETUP_BEADS_SCRIPT.is_file():
        print(
            f"The standalone Beads setup script was not found: {SETUP_BEADS_SCRIPT}",
            file=sys.stderr,
        )
        return 2
    if args.with_beads and shutil.which("bd") is None:
        print(
            "'bd' was not found; install Beads before using --with-beads.",
            file=sys.stderr,
        )
        return 2

    planned = [target / relative for relative in TARGETS]
    collisions = [path for path in planned if path.exists()]
    if collisions:
        print("Refusing to overwrite existing files:", file=sys.stderr)
        for path in collisions:
            print(f"  {path}", file=sys.stderr)
        return 1

    project_name = args.project_name or target.name
    values = template_values(project_name, args.tracker)
    if args.dry_run:
        print(f"Would scaffold {target} with tracker={args.tracker}:")
        for path in planned:
            print(f"  {path.relative_to(target)}")
        if args.with_beads:
            print(
                f"  then delegate to: {sys.executable} {SETUP_BEADS_SCRIPT} --target {target}"
            )
        return 0

    for relative, template_name in TARGETS.items():
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            render(TEMPLATE_ROOT / template_name, values), encoding="utf-8"
        )
        print(f"Created {destination.relative_to(target)}")

    if args.with_beads:
        result = subprocess.run(
            [sys.executable, str(SETUP_BEADS_SCRIPT), "--target", str(target)],
            check=False,
        )
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
