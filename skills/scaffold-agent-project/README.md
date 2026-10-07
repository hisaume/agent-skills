# Quick Start: Agent Project Scaffold

## What it does

Creates 3 broad separation of concerns, divided into 5 files:

**1. PROJECT PROMPT**

- `AGENTS.md` — repository-wide agent guidance, including sources of truth and delivery policy.
- `CONTEXT.md` — shared domain vocabulary, assumptions, and invariants.

**2. WORKFLOW PROMPT**

- `.agents/skills/application-delivery/SKILL.md` — instructions for planning and delivering durable application changes.
- `.agents/skills/application-delivery/references/workflow.md` — detailed workflow used by the application-delivery skill.

**3. APPLICATION DOCUMENTATION**

- `docs/specs/README.md` — index for the software behavioral specifications (e.g design, architecture, and API).

See also: [layout reference](references/layout.md).

## What it uses

Preview:

`python3 ~/.agents/skills/scaffold-agent-project/scripts/scaffold.py --target /path/to/project --dry-run`

Create a Beads-managed layout:

`python3 ~/.agents/skills/scaffold-agent-project/scripts/scaffold.py --target /path/to/project --project-name "My Project"`

Create the complete personal baseline, including local-only Beads without generated `AGENTS.md` guidance or Git hooks:

`python3 ~/.agents/skills/scaffold-agent-project/scripts/scaffold.py --target /path/to/project --project-name "My Project" --with-beads`

`--with-beads` delegates to `setup-beads`; use `setup-beads` directly when adding Beads to an established repository. `--initialize-beads` remains a compatibility alias.

Create without Beads:

`python3 ~/.agents/skills/scaffold-agent-project/scripts/scaffold.py --target /path/to/project --tracker none`

## Customize after scaffolding

1. `AGENTS.md`
   - Set install, check, and test commands.
   - Add project-wide invariants.
   - State commit, PR, and tracker-sync authority.

2. `CONTEXT.md`
   - Add stable domain vocabulary and invariants.

3. `docs/specs/README.md`
   - Link the authoritative specification.
   - Record superseded specifications and amendments.

4. `.agents/skills/application-delivery/references/workflow.md`
   - Change only if the project’s tracker lifecycle differs.

5. `.agents/skills/application-delivery/SKILL.md`
   - Change only for a genuinely different delivery workflow.
