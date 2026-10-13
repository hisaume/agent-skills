# Reusable Agent Skills

Intended to live in `~/.agents/skills/` and can be invoked from compatible coding agents using `$skill-name`. Individual projects generally do not need copies of these skills.

## Project setup

**New project with Beads**

`$scaffold-agent-project Scaffold this project with Beads.`

Creates project guidance, domain context, specification indexing, and a local application-delivery workflow.

**Add Beads to an existing project**

`$setup-beads Set up Beads for this project.`

Beads initializes Git if necessary. Use `--mode shared` only when `.beads/` should be repository-managed.

## Application scaffolding

**Node.js / TypeScript**

`$scaffold-node-ts Scaffold this directory as a Node.js TypeScript application.`

Node LTS, pnpm, ESM, TypeScript, linting, formatting, Vitest, and VS Code debugging. Run `pnpm check` for validation.

**Python**

`$scaffold-python Scaffold this directory as a Python application.`

CPython via uv, packaged `src/` layout, Ruff, mypy, pytest, and VS Code debugging. Run `./check.sh` for validation.

Both scaffolds target plain applications rather than framework-specific projects.

## Quality analysis

**Edge-case discovery and reconciliation**

- Defines two distinct modes of operation: discovery and reconciliation.

Discovery mode: `$edge-case-analysis Discover edge cases in this feature before specification.`

Reconciliation mode: `$edge-case-analysis Reconcile edge cases in this feature with the project-local register.`

Identifies meaningful failure scenarios during planning or maintenance. Maintains a project-local `docs/quality/edge-cases.md` register linked to specifications and executable tests.

## Conventions

- `~/.agents/AGENTS.md` holds shared cross-project guidance. Agent-specific configuration is required to load it.
- Each skill's `SKILL.md` defines its behaviour; its `README.md` provides usage guidance.
- Global skills stay in this library. Project-specific documentation and intentionally generated workflows remain in their respective repositories.
