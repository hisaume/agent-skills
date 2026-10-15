#!/usr/bin/env python3
"""Create a non-destructive standard agent-guidance layout in a project root."""

from __future__ import annotations

import argparse
import os
import re
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
    parser.add_argument(
        "--tracker",
        choices=("beads", "repository", "none"),
        help="Tracker policy (default: none, or beads with --with-beads).",
    )
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
            "TRACKER_BOUNDARY": "Keep durable state in Beads; temporary execution notes are not a project tracker.",
            "TRACKER_NOTE": "Beads is selected for durable work; selection alone does not initialize it. Run `bd prime` to confirm initialization before tracker operations; do not use markdown TODO files as the project tracker.",
            "TRACKER_ROUTE": "For durable Beads work, read `references/workflow.md`.",
            "WORKFLOW_TITLE": "Beads workflow",
            "TRACKER_STEPS": "1. Run `bd prime`.\n2. Find work with `bd ready`, inspect it with `bd show <id>`, and claim it with `bd update <id> --claim`.\n3. Record follow-up work and dependencies in Beads.\n4. Close an issue only after its repository-defined completion and integration gates pass.",
        }
    if tracker == "none":
        return {
            "PROJECT_NAME": project_name,
            "TRACKER_NOTE": "No durable tracker is configured. Do not require issue creation, claiming, or closure, or invent a markdown TODO tracker. Report remaining work in the handoff.",
            "TRACKER_ROUTE": "Read `references/workflow.md` for delivery without a tracker.",
            "WORKFLOW_TITLE": "Delivery without a tracker",
            "TRACKER_STEPS": "1. Confirm the requested scope and relevant repository guidance.\n2. Implement the approved change without issue creation, claiming, or closure requirements.\n3. Report unresolved follow-up work in the handoff; introduce a durable tracker only when requested.",
            "TRACKER_BOUNDARY": "No durable tracker is configured. Keep temporary execution notes separate from the project documentation and report follow-up work in the handoff.",
        }
    return {
        "PROJECT_NAME": project_name,
        "TRACKER_BOUNDARY": "Keep durable state in the repository-declared tracker; do not introduce a competing tracker.",
        "TRACKER_NOTE": "Record durable work in the tracker declared by this repository. Do not create a second markdown TODO system.",
        "TRACKER_ROUTE": "Read `references/workflow.md` for the delivery lifecycle.",
        "WORKFLOW_TITLE": "Delivery workflow",
        "TRACKER_STEPS": "1. Read the repository's tracker guidance.\n2. Inspect and claim work before implementation.\n3. Record follow-up work and dependencies in that tracker.\n4. Close work only after its repository-defined completion and integration gates pass.",
    }


def render(template_path: Path, values: dict[str, str]) -> str:
    content = template_path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise ValueError(f"Unknown template token: {key}")
        return values[key]

    return re.sub(r"\{\{([A-Z_]+)\}\}", replace, content)


def preflight(target: Path) -> None:
    for relative in TARGETS:
        path = target / relative
        current = target
        for component in Path(relative).parts:
            current = current / component
            if current.is_symlink():
                raise ValueError(f"Refusing symlink destination: {current}")
            if current.exists():
                if current == path:
                    raise ValueError(f"Refusing to overwrite existing entry: {current}")
                if not current.is_dir():
                    raise ValueError(
                        f"Destination parent is not a directory: {current}"
                    )
        parent = path.parent
        while not parent.exists():
            parent = parent.parent
        if not os.access(parent, os.W_OK | os.X_OK):
            raise PermissionError(f"Destination parent is not writable: {parent}")


def main() -> int:
    args = parse_args()
    target_arg = Path(args.target).expanduser()
    if target_arg.is_symlink():
        print(f"Refusing symlink target: {target_arg}", file=sys.stderr)
        return 2
    target = target_arg.resolve()
    if not target.is_dir():
        print(f"Target is not a directory: {target}", file=sys.stderr)
        return 2
    tracker = args.tracker or ("beads" if args.with_beads else "none")
    if args.with_beads and tracker != "beads":
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

    try:
        preflight(target)
        values = template_values(args.project_name or target.name, tracker)
        rendered = {
            relative: render(TEMPLATE_ROOT / template, values)
            for relative, template in TARGETS.items()
        }
    except (OSError, ValueError) as error:
        print(f"Scaffold blocked before writing: {error}", file=sys.stderr)
        return 1
    if args.dry_run:
        print(f"Would scaffold {target} with tracker={tracker}:")
        for relative in rendered:
            print(f"  {relative}")
        if args.with_beads:
            print(
                f"  then delegate to: {sys.executable} {SETUP_BEADS_SCRIPT} --target {target}"
            )
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
        print(
            "Created entries (the last may be incomplete): "
            + (", ".join(created) or "none"),
            file=sys.stderr,
        )
        print(
            "Not created: "
            + ", ".join(relative for relative in rendered if relative not in created),
            file=sys.stderr,
        )
        print(
            "Preserve existing content; inspect partial output before retrying.",
            file=sys.stderr,
        )
        return 1

    if args.with_beads:
        try:
            result = subprocess.run(
                [sys.executable, str(SETUP_BEADS_SCRIPT), "--target", str(target)],
                check=False,
            )
        except OSError as error:
            print(
                f"Guidance created; Beads setup could not start: {error}",
                file=sys.stderr,
            )
            return 1
        if result.returncode:
            print(
                "Guidance created; Beads setup failed. Inspect tracker state and retry setup-beads separately; do not rerun the scaffold.",
                file=sys.stderr,
            )
            return result.returncode
    print(
        f"Scaffold-only layout created with tracker={tracker}; project commands and domain details remain unconfigured."
    )
    if tracker == "beads" and not args.with_beads:
        print(
            "Beads setup was not run; confirm existing initialization or request setup-beads separately."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
