# scaffold-python

Scaffolds a small packaged Python application in an existing directory, with consistent configuration and verified development commands.

## Usage

`$scaffold-python Scaffold this directory as a Python application.`

Inspects the directory, selects the newest locally installed final CPython through uv, resolves compatible tools, and generates the application from canonical assets. Preserves existing files and stops on an existing Python project or conflicting destination. Existing `.gitignore` entries are retained.

Requires installed uv and final CPython 3.11 or newer. Does not download Python or upgrade uv. Reuses an existing Git repository or initializes one when Git is available. Targets standalone applications rather than parent uv workspaces.

## Output

Creates an editable packaged `src/` application with a CLI and module entry point, Ruff formatting and linting, strict mypy, pytest, and VS Code debugging.

- Derives distribution, import package, and CLI names from the directory.
- Pins the Python minor line and retains `uv.lock`.
- `uv run <cli-name>` and `uv run python -m <import_package>` run the starter application.
- `./check.sh` runs lint, formatting checks, type checks, and tests with the lock enforced.
- `uv build` creates a wheel and source archive in `dist/`.

Verifies canonical files, editable installation, and application commands before reporting completion. Reports blockers and incomplete checks explicitly.

## Skill files

- [SKILL.md](SKILL.md) — environment preparation, dependency selection, verification, and reporting workflow.
- [scripts/scaffold.py](scripts/scaffold.py) — creates and verifies baseline files from explicit runtime and tool-version inputs, preserving existing work and rejecting unsafe paths.
- `assets/` — canonical starter code and configuration templates used by the script.

Generator regression checks: run `uv run --no-project --python <installed-final-version> python -m unittest discover -s tests` from this skill directory. The generator tests use the standard library; generated applications use pytest.
