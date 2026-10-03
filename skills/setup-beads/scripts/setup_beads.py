#!/usr/bin/env python3
"""Initialize Beads without generated guidance or Git hooks, then add durable-work policy."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


POLICY_START = "<!-- BEGIN PERSONAL BEADS POLICY -->"
POLICY_END = "<!-- END PERSONAL BEADS POLICY -->"
POLICY = f"""{POLICY_START}
## Durable work

This repository uses Beads for durable project work. Run `bd prime` when
tracker context is needed; use Beads rather than markdown TODO files; and
follow the repository's delivery-authority policy for commits, pushes, and
synchronization.
{POLICY_END}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Project root (default: current directory).")
    parser.add_argument(
        "--mode",
        choices=("local", "shared"),
        default="local",
        help="Use local-only stealth storage (default) or repository-managed tracker state.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show intended changes without writing.")
    return parser.parse_args()


def policy_state(agents_text: str) -> str:
    """Return whether the policy needs adding, is present, or needs human review."""
    if POLICY_START in agents_text and POLICY_END in agents_text:
        return "present"
    if POLICY_START in agents_text or POLICY_END in agents_text:
        return "conflict"
    if "BEGIN BEADS" in agents_text or "END BEADS" in agents_text:
        return "conflict"
    if "## Durable work" in agents_text:
        return "present"
    if "Run `bd prime`" in agents_text and "markdown TODO" in agents_text:
        return "present"
    return "add"


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    agents_path = target / "AGENTS.md"

    if not target.is_dir():
        print(f"Target is not a directory: {target}", file=sys.stderr)
        return 2
    if not agents_path.is_file():
        print(
            f"{agents_path} is required. Add repository guidance first; this skill does not create it.",
            file=sys.stderr,
        )
        return 2
    if shutil.which("bd") is None:
        print("'bd' was not found on PATH.", file=sys.stderr)
        return 2

    agents_text = agents_path.read_text(encoding="utf-8")
    state = policy_state(agents_text)
    if state == "conflict":
        print(
            "AGENTS.md contains a partial or generated Beads section. Resolve it manually before running this skill.",
            file=sys.stderr,
        )
        return 1

    command = ["bd", "init", "--skip-agents", "--skip-hooks", "--non-interactive", "--init-if-missing"]
    already_initialized = (target / ".beads").exists()
    if args.mode == "local":
        command.append("--stealth")
    elif not already_initialized:
        git = shutil.which("git")
        if git is None:
            print("Git is required for shared Beads setup.", file=sys.stderr)
            return 2
        status = subprocess.run(
            [git, "status", "--porcelain"],
            cwd=target,
            check=False,
            capture_output=True,
            text=True,
        )
        if status.returncode != 0:
            print("Shared Beads setup requires a Git repository.", file=sys.stderr)
            return 2
        if status.stdout:
            print(
                "Shared Beads setup refuses a dirty Git worktree because current bd init can commit its setup.",
                file=sys.stderr,
            )
            return 1
    if args.dry_run:
        if already_initialized:
            print("Beads already exists; init will be idempotent.")
        else:
            print(
                "Would initialize .beads/ locally with no generated AGENTS.md content or Git hooks."
                if args.mode == "local"
                else "Would initialize repository-managed .beads/ with no generated AGENTS.md content or Git hooks."
            )
        print("Would run: " + " ".join(command))
        if state == "add":
            print("Would append the managed ## Durable work policy to AGENTS.md.")
        else:
            print("AGENTS.md already has equivalent Beads policy; no guidance text would be added.")
        return 0

    try:
        subprocess.run(command, cwd=target, check=True)
    except subprocess.CalledProcessError as exc:
        return exc.returncode or 1

    if state == "add":
        separator = "" if agents_text.endswith("\n\n") else "\n"
        agents_path.write_text(agents_text + separator + POLICY, encoding="utf-8")
        print("Added durable-work policy to AGENTS.md.")
    else:
        print("AGENTS.md already has equivalent Beads policy; left unchanged.")
    print(f"Beads is initialized in {args.mode} mode without generated AGENTS.md guidance or Git hooks.")
    subprocess.run(["bd", "hooks", "list"], cwd=target, check=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
