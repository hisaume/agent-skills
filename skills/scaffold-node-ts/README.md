# scaffold-node-ts

Scaffolds a minimal, runnable Node.js TypeScript application in an existing directory, with consistent configuration and verified development commands.

## Usage

`$scaffold-node-ts Scaffold this directory as a Node.js TypeScript application.`

Inspects the directory, selects the newest locally installed Node LTS through nvm, resolves compatible development dependencies, and generates the application using canonical assets. Preserves existing files and stops if the directory is already a Node project or a destination file conflicts.

Requires installed nvm, a locally installed Node LTS from major 20, 22, or 24, and pnpm 10 or newer. Does not download Node or upgrade pnpm. Reuses an existing Git repository or initializes one when Git is available.

## Output

Creates a plain application with strict TypeScript, ESM, ESLint, Prettier, Vitest, source maps, and VS Code debugging.

- `pnpm dev` runs the starter application.
- `pnpm check` runs lint, formatting checks, type checks, and tests.
- `pnpm build` produces `dist/`; `pnpm start` runs the compiled application.
- Retains a lockfile and project-local pnpm configuration approving esbuild's installation script, without defining workspace packages.

Verifies the generated baseline, dependency compatibility, and application commands before reporting completion. Reports blockers and incomplete checks explicitly.

## Skill files

- [SKILL.md](SKILL.md) — environment preparation, dependency selection, verification, and reporting workflow.
- [scripts/scaffold.mjs](scripts/scaffold.mjs) — creates and verifies baseline files using explicit Node, pnpm, and dependency-version inputs; refuses existing files and unsafe destination paths.
- `assets/` — canonical starter code and configuration templates used by the script.

Generator regression checks: select a supported LTS through nvm, then run `node --test tests/scaffold.test.mjs` from this skill directory.
