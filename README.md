# Agent Skills

## New project with Beads

Standard agent-guidance layout + local-only Beads setup:

```
$scaffold-agent-project Scaffold this project with Beads.
```

## Add Beads to an existing project

Note: Beads initializes git if it is not already a git repository.

```
$setup-beads Set up Beads for this project.
```

Use `--mode shared` only when `.beads/` should be repository-managed.

## New Node.js TypeScript application

Plain application with Node LTS via nvm, pnpm, ESM, linting, formatting, tests, and VS Code debugging:

```
$scaffold-node-ts Scaffold this directory as a Node.js TypeScript application.
```

Use `pnpm check` for the canonical quality check. Excludes frameworks, libraries, and existing configured Node projects.
