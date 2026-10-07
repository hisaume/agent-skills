# scaffold-node-ts

Scaffolds a plain runnable TypeScript application in an existing project folder.

## Tools

- Requires existing `nvm` and `pnpm`.
- Selects or installs the latest Node.js LTS through nvm.
- Installs TypeScript, tsx, and Node.js types.
- Installs ESLint and its TypeScript/Prettier configuration dependencies.
- Installs Prettier and Vitest.
- Configures strict TypeScript, ESM, source maps, and VS Code debugging.

## Project structure

```text
my-app/
├── .gitignore
├── .nvmrc
├── .prettierignore
├── .prettierrc.json
├── .vscode/launch.json
├── eslint.config.js
├── package.json
├── pnpm-lock.yaml
├── tsconfig.json
├── tsconfig.build.json
├── src/index.ts
└── tests/index.test.ts
```

- Reuses an existing Git repository or initializes one when needed.
- `pnpm dev` runs the starter app.
- `pnpm check` runs lint, formatting checks, type checks, and tests.
- `pnpm build` produces `dist/`; `pnpm start` runs the compiled app.
