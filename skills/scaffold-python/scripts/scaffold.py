"""Create or verify a Python application from canonical assets."""

import argparse
import json
import keyword
import platform
import re
import sys
import tomllib
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def render(target: Path, inputs: dict[str, object]) -> dict[str, str]:
    if set(inputs) != {"python", "uv_build", "dependencies"}:
        raise ValueError("Inputs must contain only python, uv_build, and dependencies")
    python = inputs["python"]
    if not isinstance(python, str) or not re.fullmatch(r"3\.\d+\.\d+", python):
        raise ValueError("Select an exact final CPython version")
    if (
        platform.python_implementation() != "CPython"
        or sys.version_info.releaselevel != "final"
        or platform.python_version() != python
    ):
        raise ValueError(
            "Run the generator through uv using the selected final CPython"
        )
    dependencies = inputs["dependencies"]
    if not isinstance(dependencies, dict) or set(dependencies) != {
        "mypy",
        "pytest",
        "ruff",
    }:
        raise ValueError("Provide exactly mypy, pytest, and ruff development versions")
    versions = {
        "BACKEND": inputs["uv_build"],
        **{k.upper(): v for k, v in dependencies.items()},
    }
    for value in versions.values():
        if not isinstance(value, str) or not re.fullmatch(
            r"\d+(?:\.\d+){1,3}(?:\.post\d+)?", value
        ):
            raise ValueError(
                "Dependency and backend versions must be exact stable releases"
            )
    distribution = (
        re.sub(r"[^a-z0-9]+", "-", target.name.lower()).strip("-") or "python-app"
    )
    package = distribution.replace("-", "_")
    if package[0].isdigit():
        package = "app_" + package
    if keyword.iskeyword(package):
        package += "_app"
    tokens = {
        "DISTRIBUTION": distribution,
        "PACKAGE": package,
        "MINOR": ".".join(python.split(".")[:2]),
        **versions,
    }
    output = {}
    for asset in sorted(ASSETS.rglob("*")):
        if not asset.is_file():
            continue
        relative = asset.relative_to(ASSETS).as_posix()
        if relative.startswith("package/"):
            relative = f"src/{package}/" + relative.removeprefix("package/")
        text = asset.read_text()
        for token, value in tokens.items():
            text = text.replace(f"@@{token}@@", str(value))
        if "@@" in text:
            raise ValueError(f"Unresolved asset token: {asset}")
        output[relative] = text
    output[".python-version"] = tokens["MINOR"] + "\n"
    return output


def execute(mode: str, target: Path, inputs: dict[str, object]) -> None:
    if target.is_symlink() or not target.is_dir():
        raise ValueError("Target must be an existing directory, not a symlink")
    output = render(target, inputs)
    for ancestor in target.parents:
        config = ancestor / "pyproject.toml"
        if config.is_file():
            metadata = tomllib.loads(config.read_text())
            if "workspace" in metadata.get("tool", {}).get("uv", {}):
                raise ValueError(
                    "Use a standalone directory outside the parent uv workspace"
                )
    if mode == "create":
        for relative in output:
            path = target / relative
            for part in [*path.parents, path]:
                if part == target.parent:
                    continue
                if part.is_symlink():
                    raise ValueError(f"Refusing symlink destination: {part}")
            if path.exists() and not (relative == ".gitignore" and path.is_file()):
                raise ValueError(f"Refusing existing destination: {path}")
            if any(p.exists() and not p.is_dir() for p in path.parents):
                raise ValueError(f"Destination parent is not a directory: {path}")
        for relative, text in output.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if relative == ".gitignore" and path.exists():
                original = path.read_text()
                missing = [
                    line
                    for line in text.splitlines()
                    if line not in original.splitlines()
                ]
                if missing:
                    with path.open("a") as stream:
                        if original and not original.endswith("\n"):
                            stream.write("\n")
                        stream.write("\n".join(missing) + "\n")
            else:
                with path.open("x") as stream:
                    stream.write(text)
            if relative == "check.sh":
                path.chmod(path.stat().st_mode | 0o111)
    else:
        for relative, expected in output.items():
            path = target / relative
            if path.is_symlink() or any(p.is_symlink() for p in path.parents):
                raise ValueError(f"Refusing symlink destination: {path}")
            actual = path.read_text()
            if relative == ".gitignore":
                valid = set(expected.splitlines()) <= set(actual.splitlines())
            elif relative.endswith(".toml"):
                valid = tomllib.loads(actual) == tomllib.loads(expected)
            elif relative.endswith(".json"):
                valid = json.loads(actual) == json.loads(expected)
            else:
                valid = actual == expected
            if not valid:
                raise ValueError(f"Baseline changed: {relative}")
        if not (target / "check.sh").stat().st_mode & 0o111:
            raise ValueError("check.sh must be executable")
    print(
        f"{mode}: baseline {'created' if mode == 'create' else 'verified'} for {target.name}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["create", "verify"])
    parser.add_argument("target", type=Path)
    parser.add_argument("inputs", type=Path)
    args = parser.parse_args()
    try:
        execute(args.mode, args.target.absolute(), json.loads(args.inputs.read_text()))
    except (OSError, ValueError, TypeError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
