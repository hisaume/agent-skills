---
name: scaffold-python
description: Scaffold a new plain runnable Python application in an already-created directory. Use for new non-framework Python applications; do not use for publish-first libraries, existing configured Python projects, web frameworks, monorepos/workspaces, or projects with substantial Python configuration.
---

# Scaffold Python Application

Create a small, packaged Python application that is runnable, typed, tested, and easy to verify.

## Inspect first

- Inspect the target directory before changing it.
- Preserve unrelated existing files.
- Never overwrite an existing file or configuration without explicit approval.
- For an existing `.gitignore`, preserve its contents and append missing baseline entries as specified below.
- If `pyproject.toml` already exists, stop and report that the directory is already a Python project.
- Do not use this skill for libraries intended primarily for publishing, existing configured Python projects, web frameworks, monorepos/workspaces, or projects with substantial Python configuration.

## Naming

- Derive the default project name from the already-created folder name.
- Normalize the folder-derived distribution name to a hyphenated name, such as `my-app`; do not rename the existing project directory.
- Normalize the import package to an underscore-safe Python identifier, such as `my_app`.
- Use the distribution name as the CLI name where practical, such as `my-app`.
- Never use hyphens in a Python import package name.
- Report the derived distribution, import package, and CLI names before completion if normalization is non-obvious.

## Git

- Detect whether the target directory is already inside a Git repository; do not rely only on a local `.git` entry.
- Reuse the existing repository when the target is inside one.
- If it is not inside a repository, initialize Git in the target directory.
- Never create a nested repository.
- Never commit, push, merge, rebase, create remotes, or alter shared history automatically.

## Python and uv

- Use `uv` for Python runtime, project, and dependency management.
- Select the latest stable **final** CPython release available. Never select alpha, beta, or release-candidate versions.
- Do not call Python releases LTS.
- Pin the selected Python minor line in `.python-version`, for example `3.14`; use a patch-level pin only when necessary.
- Set `requires-python` consistently in `pyproject.toml`.
- Initialize outside any parent uv workspace by using `--no-workspace` or the current equivalent.
- Do not let uv initialize Git; manage Git separately.
- Use uv's current recommended pure-Python build backend, `uv_build`, where appropriate.
- Set the initial project version to `0.0.1`.
- Remove generated metadata references to excluded files, such as a README or license, rather than creating those files.
- Generate and retain `uv.lock`; it is intended to be committed.
- Do not publish the project or invent a Python equivalent of npm `private: true`.

## Project layout

Create this conceptual layout, without replacing unrelated existing files:

```text
.gitignore
.python-version
.vscode/launch.json
check.sh
pyproject.toml
uv.lock
src/<import_package>/__init__.py
src/<import_package>/__main__.py
tests/test_smoke.py
```

- Create `.git/` only when the target was not already contained in a Git repository.
- Use the packaged `src/` layout.
- Ensure uv installs the application editably in its environment so tests exercise the installed package rather than accidental repo-root imports.

## Runtime entry point

- Create `src/<import_package>/__main__.py` with `main() -> None`.
- Include `if __name__ == "__main__": main()`.
- Add a `[project.scripts]` entry mapping `<cli-name>` to `<import_package>.__main__:main` so `uv run <cli-name>` works.
- Ensure `uv run python -m <import_package>` also works.
- Make starter behavior print only a simple confirmation.
- Do not invent application architecture or business logic.

## Development tools

- Add the latest stable mutually compatible development releases of `ruff`, `mypy`, and `pytest`.
- Use `pytest`, not `unittest`, as the test baseline.
- Do not add Black, isort, Flake8, pytest plugins, coverage tooling, tox, nox, just, Make, or other task runners by default.
- Keep mypy as the type-checking baseline; do not substitute Pyright or ty.

## Ruff

- Configure Ruff in `pyproject.toml`.
- Use Ruff for both linting and formatting.
- Use a sensible modern baseline rule set without over-customizing style.
- Let metadata such as `requires-python` supply the target Python version; do not duplicate unnecessary version configuration.

## mypy

- Configure mypy in `pyproject.toml`.
- Start strict for a fresh project.
- Add an exception only for a current tooling limitation, and document it narrowly.

## pytest

- Configure pytest in `pyproject.toml`.
- Keep tests in `tests/`.
- Prefer pytest's importlib import mode for a new `src/` layout project, for example `--import-mode=importlib`.
- Add one minimal smoke test that proves the package import and test setup work.
- Do not invent fake business behavior.

## check.sh

- Create an executable root-level `check.sh`.
- Treat the root location as a deliberate house convention for discoverability, not universal Python practice.
- Use a Bash shebang (`#!/usr/bin/env bash`), followed by `set -euo pipefail`.
- Keep the quality gate visible in the script; do not hide it in another task runner.
- Run the following checks with the lock enforced:

```bash
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy .
uv run --locked pytest
```

- Larger projects may later move this file to `scripts/` and update references.
- Do not add PowerShell parity by default; Git Bash or WSL can run this script on Windows.

## .gitignore

- Preserve existing entries; append only missing baseline entries.
- Include these sensible Python/application entries:

```gitignore
.venv/
__pycache__/
*.py[cod]
.mypy_cache/
.ruff_cache/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.env
.env.*
!.env.example
*.log
.DS_Store
```

- Do not ignore `.vscode/`; the scaffold deliberately provides a debug configuration.

## VS Code-compatible debugging

- Create only `.vscode/launch.json` as the editor-specific convenience layer.
- Configure it to launch and debug the module or application with the project `.venv` interpreter and ordinary Python source breakpoints.
- Do not add source maps; Python does not need them.
- Do not add `debugpy` as a project dependency by default. VS Code-family Python debugging already supplies the needed machinery.
- Add `debugpy` only when the project explicitly needs remote, container, or attach debugging.
- Do not create `.vscode/settings.json`, extension recommendations, or other editor configuration.

## Verification

- Run the formatter to normalize generated files when appropriate.
- Run `./check.sh`.
- Verify `uv run <cli-name>` succeeds.
- Verify `uv run python -m <import_package>` succeeds.
- Verify `uv build` succeeds and generates artifacts.
- Inspect `git status --short` when Git is available.
- Fix failures caused by the scaffold before reporting success.
- Report the selected Python version, derived distribution/import package/CLI names, whether Git was initialized or reused, and verification results.

## Boundaries

Do not create any of the following unless the user explicitly requests them:

- `AGENTS.md` or `CONTEXT.md`
- ADRs, specifications, README files, or licenses
- CI/CD, Docker, environment files, Git hooks, or release/version/tagging workflows beyond `0.0.1`
- Publishing configuration or publishing processes
- Web or application frameworks, databases, workspace/monorepo configuration, coverage tooling, or extra task runners
- A project `debugpy` dependency
