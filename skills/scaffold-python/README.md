# scaffold-python

Scaffolds a plain runnable Python application in an existing project folder.

## Tools

- Uses uv to manage Python, dependencies, and the project environment.
- Selects the latest stable final CPython release and pins its minor version.
- Installs Ruff, mypy, and pytest as development dependencies.
- Uses `uv_build` for a packaged, editable `src/` application.
- Configures strict typing, linting, formatting, tests, and VS Code debugging.

## Project structure

```text
my-app/
├── .gitignore
├── .python-version
├── .vscode/launch.json
├── check.sh
├── pyproject.toml
├── uv.lock
├── src/my_app/
│   ├── __init__.py
│   └── __main__.py
└── tests/test_smoke.py
```

- Derives names from the folder: distribution/CLI `my-app`, import package `my_app`.
- Reuses an existing Git repository or initializes one when needed.
- `uv run my-app` or `uv run python -m my_app` runs the starter app.
- `./check.sh` runs lint, formatting checks, type checks, and tests.
- `uv build` produces distribution artifacts in `dist/`.
