# Reusable Agent Skills

Intended to live in `~/.agents/skills/` and can be invoked from compatible coding agents using `$skill-name`. Individual projects generally do not need copies of these skills.

## Skill development

- ### Agent Skill architecture and review
  - Supports three operations: Create, Review, and Refine.

    Create:

    `$skill-architect Create a reusable skill for database migration reviews.`

    Review:

    `$skill-architect Review edge-case-analysis for maintainability and guardrails. Do not modify it.`

    Refine:

    `$skill-architect Refine edge-case-analysis based on the review findings.`

  - Evaluates skill structure, responsibilities, guardrails, documentation hygiene, portability, and maintenance cost. Prefers minimal changes and accepts "no change needed" as a valid outcome.

## Debugging

- ### Isolated code probing and debugger handoff

  Auto-probe:

  `$code-probe Check whether compare() skips a target under certain conditions.`

  Handoff:

  `$code-probe handoff on compare()`

  Creates minimal, disposable harnesses with adjustable inputs and dependency isolation. Auto-probe investigates suspected behaviour; handoff prepares a VS Code debugging entry point without executing behavioural checks or setting breakpoints. Language-independent and adapted to existing project tooling.

## Quality analysis

- ### Edge-case discovery and reconciliation
  - Defines two distinct modes of operation: discovery and reconciliation.

  Discovery mode:

  `$edge-case-analysis Discover edge cases in this feature before specification.`

  Reconciliation mode:

  `$edge-case-analysis Reconcile edge cases in this feature with the project-local register.`

  Identifies meaningful failure scenarios during planning or maintenance. Maintains a project-local `docs/quality/edge-cases.md` register linked to specifications and executable tests.

- ### Prompt-residue sweep

  `$prompt-residue-sweep Review this README.md for conversational residue. Report findings only.`

  Identifies drafting or conversational residue in finished prose, documentation, and code comments. Reports exact excerpts and minimal corrections without modifying files.

## Project setup

- ### Project agent guidance

  `$scaffold-agent-project Scaffold agent guidance in this project.`

  Creates project guidance, domain context, specification indexing, and a local application-delivery workflow. Defaults to no tracker; reuses a declared tracker when selected. Explicitly requesting Beads initializes it with `setup-beads` skill. Small, well-understood changes do not require new specifications or vertical-slice plans.

- ### Add Beads to an existing project

  `$setup-beads Set up Beads for this project.`

  Beads initializes Git if necessary. Use `--mode shared` only when `.beads/` should be repository-managed.

## Application scaffolding

- ### Node.js / TypeScript

  `$scaffold-node-ts Scaffold this directory as a Node.js TypeScript application.`

  Locally installed Node LTS through nvm, pnpm, ESM, TypeScript, linting, formatting, Vitest, and VS Code debugging. An agent resolves compatible dependencies; bundled assets and a generator create and verify the baseline. Run `pnpm check` for validation.

- ### Python

  `$scaffold-python Scaffold this directory as a Python application.`

  Locally installed final CPython through uv, packaged `src/` layout, Ruff, mypy, pytest, and VS Code debugging. An agent resolves compatible tools; bundled assets and a generator create and verify the baseline. Run `./check.sh` for validation.

  Both scaffolds target plain applications rather than framework-specific projects.

## Conventions

- `~/.agents/AGENTS.md` holds shared cross-project guidance. Agent-specific configuration is required to load it.
- Each skill's `SKILL.md` defines its behaviour; its `README.md` provides usage guidance.
- Global skills stay in this library. Project-specific documentation and intentionally generated workflows remain in their respective repositories.
