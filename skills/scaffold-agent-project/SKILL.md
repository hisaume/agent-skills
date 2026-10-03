---
name: scaffold-agent-project
description: Scaffold a project-root agent-guidance layout with AGENTS.md, domain and specification indexes, and an application-delivery skill. Use when starting a repository or standardizing its agent documentation; do not use to modify an established layout without review.
---

# Scaffold agent project

Create the personal project-standard layout without overwriting existing
guidance. The scaffold supplies structure, not project decisions.

## Before scaffolding

1. Confirm the target directory is the intended project root.
2. Inspect existing `AGENTS.md`, `.agents/`, `docs/`, and tracker state.
3. For an established repository, show the planned files first and preserve
   existing guidance unless the user explicitly asks to replace it.

## Run the scaffold

Run a dry run first:

```bash
python3 .agents/skills/scaffold-agent-project/scripts/scaffold.py \
  --target <project-root> --dry-run
```

For a new Beads-managed project, omit `--tracker`; it defaults to `beads`.
Use `--tracker none` when the repository has no durable tracker yet. Add
`--initialize-beads` only when the user explicitly wants Beads initialized.
It uses the same safe default as `setup-beads`: no generated Beads guidance
and no Git hooks.

The script refuses to overwrite files. After it succeeds, replace the command
placeholders in `AGENTS.md`, add domain terms only when they settle, and add a
specification when real scope exists.

## Resulting layout

The scaffold creates `AGENTS.md`, `CONTEXT.md`, `docs/specs/README.md`, and
the project-local `application-delivery` skill. Read
[the layout reference](references/layout.md) when deciding which generated
files remain useful for a particular repository.
