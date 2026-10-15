# scaffold-agent-project

Creates project guidance, domain and specification entry points, and a project-local application-delivery workflow without overwriting existing files.

## Usage

`$scaffold-agent-project Scaffold agent guidance in this project.`

Inspects existing guidance and tracker state, previews the planned files, and runs the deterministic generator. An existing established layout requires review rather than automatic replacement.

Direct invocation from any directory:

```bash
python3 ~/.agents/skills/scaffold-agent-project/scripts/scaffold.py --target /path/to/project --dry-run
python3 ~/.agents/skills/scaffold-agent-project/scripts/scaffold.py --target /path/to/project
```

The default is no tracker. Select `--tracker beads` for Beads guidance or `--tracker repository` to reuse another declared tracker. Guidance selection alone does not initialize a tracker. When local Beads setup is explicitly requested, add `--with-beads`; it implies Beads unless an incompatible tracker is supplied. `--initialize-beads` remains a compatibility alias. Initialization delegates to `setup-beads` without taking ownership of its safety or hook policy.

## Output

Separates repository-wide guidance and domain context from an on-demand delivery workflow and a specification index. See [the layout reference](references/layout.md).

- Preserves existing files and refuses unsafe destinations before creation.
- Generates genuine tracker-free guidance when no tracker is configured.
- Marks project commands unconfigured and leaves domain placeholders intact.
- Requires authorization for commits, pushes, pull requests, and external tracker synchronization.
- Allows small, well-understood changes without creating specifications or vertical-slice plans solely because those artifacts are absent.

The result is a scaffold, not a fully configured project. Customize commands, domain invariants, specifications, and delivery authority only in a separately requested step. Unexpected partial failures report created and missing files; inspect that output before retrying.

## Skill files

- [SKILL.md](SKILL.md) — inspection, tracker selection, generation, verification, and handoff rules.
- [scripts/scaffold.py](scripts/scaffold.py) — deterministic template rendering, destination preflight, exclusive creation, and optional delegation to Beads setup.
- `assets/` — canonical guidance and delivery-workflow templates.

Regression checks: `python3 -m unittest discover -s tests` from this skill directory.
