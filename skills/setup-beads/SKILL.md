---
name: setup-beads
description: Initialize Beads in an existing repository without generated AGENTS.md text or Git hooks. Use when a project needs Beads as its durable tracker while preserving its own agent guidance and avoiding automatic hook-driven edits.
---

# Set up Beads

Set up Beads as the repository's durable work tracker without delegating the
project's instructions to Beads and without installing Git hooks.

This skill is standalone. It does not require the agent-project scaffold and
does not invoke it. It does require an existing project-root `AGENTS.md`: the
repository, not this skill, owns the rest of its guidance.

## Boundaries

- Never run `bd init` without `--skip-agents --skip-hooks`.
- Do not run `bd setup ...` or `bd hooks install` unless the user explicitly
  asks for Beads-managed instruction text or hooks.
- Do not remove pre-existing hooks automatically. Report them and let the user
  choose whether to run `bd hooks uninstall`.
- Do not alter delivery-authority rules for commits, pushes, pull requests, or
  tracker synchronisation.
- Normal `bd` writes will still update `.beads/`; the safe default only avoids
  *automatic Git-hook* writes during Git operations.

## Choose the storage mode

Use the default `local` mode for personal work. It adds `--stealth`, so Beads
is excluded from the repository and `bd init` cannot make an initialization
commit. The tracker does not travel with clones; configure a Dolt remote later
if it needs cross-machine synchronisation.

Use `shared` only when the user explicitly wants `.beads/` managed by the
repository. Current Beads may make a dedicated initialization commit in this
mode. The script therefore refuses a dirty Git worktree before initializing.

## Run

From any directory, preview the change first:

```bash
python3 ~/.agents/skills/setup-beads/scripts/setup_beads.py \
  --target <project-root> --dry-run
```

When the user authorises the initialization, run the same command without
`--dry-run`:

```bash
python3 ~/.agents/skills/setup-beads/scripts/setup_beads.py \
  --target <project-root>
```

For repository-managed tracker state, the user must explicitly select it:

```bash
python3 ~/.agents/skills/setup-beads/scripts/setup_beads.py \
  --target <project-root> --mode shared
```

The script is idempotent. In the default local mode it invokes:

```bash
bd init --skip-agents --skip-hooks --non-interactive --init-if-missing --stealth
```

and adds the repository's concise durable-work policy only when no equivalent
Beads policy is already present. It refuses to edit a generated Beads section,
so a human can resolve competing guidance deliberately.

## Verify

After a real run, verify all of the following:

1. `.beads/` exists and `bd prime` succeeds from the repository root.
2. `AGENTS.md` contains either the new `## Durable work` section or an
   equivalent pre-existing Beads policy.
3. `bd hooks list` reports no Beads hooks newly installed by this setup.

An equivalent existing Beads policy is recognised; the skill then only
initializes Beads and does not add duplicate instructions.
