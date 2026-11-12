---
name: setup-beads
description: Initialize or verify Beads as a project's work tracker and install its tracker contract. Use for optional Beads activation in a repository with project delivery guidance; not for implementation workflow design or ticket planning.
---

# Set up Beads

The project's `application-delivery` skill governs implementation and validation. This skill installs tracker state and guidance only.

## Inspect and preview

1. Identify the project root. Require `AGENTS.md` and the project-local `application-delivery` skill. Read any existing `docs/agents/issue-tracker.md` and `.beads/` state. Confirm `bd` is available.
2. Refuse competing tracker policy, conflicting delivery rules, symlinked destinations, or divergent existing tracker guidance. Do not overwrite unrelated instructions.
3. Show the proposed file changes before applying them. Default to **local-only** Beads. Shared mode requires explicit authorization and a clean Git working tree; `bd init` may create a commit. Do not convert an existing installation between modes.

## Activate

1. If `.beads/` is absent, initialize from the project root:

   ```bash
   bd init --skip-agents --skip-hooks --non-interactive --init-if-missing --stealth
   ```

   Omit `--stealth` only for authorized shared mode. Do not install Beads-managed instructions or hooks. If `.beads/` exists, preserve it and skip initialization.
2. Run `bd prime`. If it fails, stop without editing guidance; report any partially initialized state.
3. Copy [assets/issue-tracker.md](assets/issue-tracker.md) to `docs/agents/issue-tracker.md` if absent. Keep compatible existing guidance; stop on conflicts.
4. Under `## Delivery authority` in `AGENTS.md`, add exactly one declaration, replacing any existing unconfigured-tracker statement or equivalent Beads declaration:

   ```markdown
   - Tracker: Beads. See `docs/agents/issue-tracker.md`.
   ```

   Verify destinations and planned edits before writing. Do not modify `application-delivery` or other project files.

## Verify

Confirm `bd prime`, a single Beads declaration, and a compatible tracker guide. Repeated setup must not duplicate guidance. Report edits and partial state; do not commit, push, or synchronize beyond authorized initialization.
