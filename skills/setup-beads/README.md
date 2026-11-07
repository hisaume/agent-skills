# setup-beads

Initialize Beads in a project created with `scaffold-agent-project`, including projects initially scaffolded without a tracker.

```bash
python3 ~/.agents/skills/setup-beads/scripts/setup_beads.py --target /path/to/project --dry-run
python3 ~/.agents/skills/setup-beads/scripts/setup_beads.py --target /path/to/project
```

The default initializes local-only Beads without generated agent instructions, Git hooks, or commits. `--mode shared` explicitly selects repository-managed storage and may cause an initialization commit.

The setup updates the scaffold's existing tracker guidance in `AGENTS.md` and the project-local `application-delivery` skill, and adds `docs/agents/issue-tracker.md`. It preserves custom project content and refuses unfamiliar tracker instructions rather than overwriting them. It does not migrate an existing Beads database between storage modes.

Requires a working `bd` executable and the installed sibling `scaffold-agent-project` skill.
