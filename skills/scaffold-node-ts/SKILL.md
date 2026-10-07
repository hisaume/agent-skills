---
name: scaffold-node-ts
description: Scaffold a new plain runnable Node.js TypeScript application in an already-created directory. Use for new non-framework Node/TypeScript applications; do not use for libraries/packages, React or Vite apps, monorepos/workspaces, or existing configured Node projects.
---

# Scaffold Node TypeScript

Create a minimal, runnable, testable, and debuggable Node.js TypeScript application.

Keep the scaffold generic. Do not add project-specific architecture or tooling beyond the baseline defined here.

## Inspect first

- Work in the directory requested by the user.
- If no directory is specified, use the current working directory.
- Inspect the directory before modifying anything.
- Preserve existing unrelated files.
- Never overwrite an existing file without explicit approval.
- If `package.json` already exists, stop and report that the directory is already a Node project.
- If substantial existing TypeScript or Node configuration is present, stop rather than attempting to merge or replace it.

## Required tools

- Use `nvm` to manage Node.js.
- Use `pnpm` exclusively for package management.
- Use Git when available.
- Do not install or replace system-wide package managers.
- Do not run `pnpm self-update`.
- If `nvm` or `pnpm` is unavailable in the current shell, stop and report the missing requirement.

## Node.js

- Use the latest available Node.js LTS release.
- Resolve it through nvm rather than hardcoding a Node version into this skill.
- Select or install it with nvm as needed.
- Write the exact selected Node version to `.nvmrc`.
- Set `engines.node` in `package.json` to the selected LTS major version range.
- Do not select the Node "Current" release when it is newer than LTS.

## pnpm

- Use the installed pnpm version.
- Record its exact version in `package.json` using the `packageManager` field.
- Do not silently upgrade pnpm.
- Generate and retain `pnpm-lock.yaml`; it is intended to be committed.

## Git

- Determine whether the target directory is already inside a Git repository.
- If it is already inside a repository:
  - Do not run `git init`.
  - Do not modify parent-repository configuration.
- If it is not inside a repository:
  - Run `git init`.
- Never create a nested Git repository.
- Never commit, push, merge, rebase, or create remotes automatically.

## package.json

Use the working directory name as the default package name.

Normalize the name when necessary:

- Convert to lowercase.
- Convert spaces and underscores to hyphens.
- Remove characters invalid in an npm package name.
- Collapse repeated hyphens.
- If no valid name remains, use `node-ts-app`.

Set these baseline fields:

- `version`: `0.0.1`
- `private`: `true`
- `type`: `module`
- `packageManager`: exact installed pnpm version
- `engines.node`: selected Node LTS major range

Do not configure package publishing.

## Development dependencies

Install the latest stable mutually compatible releases of:

- `typescript`
- `tsx`
- `@types/node`
- `eslint`
- `@eslint/js`
- `typescript-eslint`
- `globals`
- `prettier`
- `eslint-config-prettier`
- `vitest`

Do not add runtime dependencies unless requested by the user.

## Package scripts

Create these scripts:

```json
{
  "dev": "tsx src/index.ts",
  "build": "tsc -p tsconfig.build.json",
  "start": "node dist/index.js",
  "typecheck": "tsc --noEmit",
  "lint": "eslint .",
  "format": "prettier --write .",
  "format:check": "prettier --check .",
  "test": "vitest run",
  "test:watch": "vitest",
  "check": "pnpm lint && pnpm format:check && pnpm typecheck && pnpm test"
}
```

`pnpm check` is the canonical project quality check.

Do not create a `check.sh` wrapper.

## TypeScript

Create `tsconfig.json` for development and type checking.

Configure it to:

- Use strict TypeScript.
- Use modern Node.js ESM semantics.
- Target an ECMAScript version appropriate for the selected Node LTS.
- Include both application source and tests.
- Perform type checking without emitting files.
- Use Node.js type definitions.
- Support JSON module imports.
- Enforce consistent filename casing.
- Skip checking declaration files from dependencies.
- Avoid unnecessary legacy interoperability options unless required.

Create `tsconfig.build.json` extending the main configuration.

Configure the build configuration to:

- Compile only application files under `src/`.
- Use `src/` as `rootDir`.
- Emit JavaScript to `dist/`.
- Generate source maps.
- Produce runnable ESM JavaScript.
- Exclude tests from build output.

The resulting entry point after `pnpm build` must be:

```text
dist/index.js
```

## Application entry point

Create:

```text
src/index.ts
```

Provide minimal executable starter code that visibly confirms the application runs.

Keep it intentionally trivial. Do not invent application architecture.

For example, running either:

```text
pnpm dev
```

or:

```text
pnpm build
pnpm start
```

should complete successfully and print a simple confirmation message.

## Tests

Create:

```text
tests/index.test.ts
```

Add one small passing Vitest test.

The purpose of the starter test is to prove that:

- Vitest is installed correctly.
- TypeScript tests execute correctly.
- The test command works.

Do not invent meaningful application behavior solely to create a test.

Use explicit Vitest imports rather than global test functions.

## ESLint

Create:

```text
eslint.config.js
```

Use the current ESLint flat configuration format.

Configure:

- `@eslint/js` recommended rules.
- `typescript-eslint` recommended rules.
- Node.js globals.
- TypeScript source and test files.
- `dist/` and `coverage/` as ignored output.
- `eslint-config-prettier` last so formatting rules do not conflict with Prettier.

Do not enable type-aware linting by default.

Keep linting separate from TypeScript type checking.

## Prettier

Use Prettier's standard defaults.

Create:

```text
.prettierrc.json
.prettierignore
```

Use an empty JSON object in `.prettierrc.json` to make use of Prettier explicit without adding personal style overrides.

Ignore generated or dependency content such as:

- `node_modules/`
- `dist/`
- `coverage/`
- `pnpm-lock.yaml`

## .gitignore

Create `.gitignore`, or append missing baseline entries if one already exists.

Do not remove existing entries.

Include at least:

- `node_modules/`
- `dist/`
- `coverage/`
- `.env`
- `.env.*`
- `!.env.example`
- `*.log`
- `.DS_Store`

Do not ignore `.vscode/`, because this scaffold provides a project debug configuration.

## VS Code-compatible debugging

This is an editor-specific convenience layer. Keep it isolated from the core project configuration so it can be removed easily later.

Create:

```text
.vscode/launch.json
```

Configure a Node launch target that:

- Runs `src/index.ts`.
- Uses Node with `tsx` loaded through `--import tsx`.
- Uses the project working directory.
- Supports TypeScript breakpoints.
- Skips Node internal source while stepping.
- Uses source maps where applicable.

Do not create editor settings, extension recommendations, or other VS Code configuration.

If `.vscode/launch.json` already exists, do not overwrite it.

`tsx` officially supports running TypeScript through `node --import tsx`, which makes this suitable for Node-based debugger launch configurations. VS Code's Node debugger supports `runtimeArgs` and TypeScript source maps.

## Expected project shape

After scaffolding, expect approximately:

```text
.
├── .gitignore
├── .nvmrc
├── .prettierignore
├── .prettierrc.json
├── .vscode/
│   └── launch.json
├── eslint.config.js
├── package.json
├── pnpm-lock.yaml
├── tsconfig.json
├── tsconfig.build.json
├── src/
│   └── index.ts
└── tests/
    └── index.test.ts
```

A `.git/` directory will also exist when this directory was not already contained within a Git repository.

## Verification

Before reporting completion:

- Run `pnpm format`.
- Run `pnpm check`.
- Run `pnpm build`.
- Run `pnpm dev` and confirm the starter application executes successfully.
- Run `pnpm start` and confirm the compiled application executes successfully.
- Confirm `dist/index.js` exists after the build.
- Confirm source-map output exists.
- Inspect `git status --short` when Git is available.

Fix scaffold-generated failures before reporting success.

Report:

- Selected Node version.
- Selected pnpm version.
- Derived project name.
- Whether Git was initialized or an existing repository was reused.
- Whether all verification commands passed.

## Boundaries

Do not create or configure project-specific setup or separate skills, such as but not limited to:

- `AGENTS.md`
- `CONTEXT.md`
- project specifications or ADRs
- README documentation
- licenses
- CI/CD
- Docker
- environment files
- Git hooks
- commit conventions
- release tooling
- package publishing
- library exports
- monorepo/workspace configuration
- application frameworks
- databases
- `check.sh`
