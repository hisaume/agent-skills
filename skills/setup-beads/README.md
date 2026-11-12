# setup-beads

Initializes Beads and adds its tracker contract to a scaffolded project. Use `$setup-beads` after `scaffold-agent-project` or in an established compatible layout.

- `SKILL.md` — preflight, initialization, verification, and safety rules.
- `assets/issue-tracker.md` — copied to `docs/agents/issue-tracker.md`.
- `tests/` — development-only checks of SKILL.md's frontmatter and contract; not used at runtime.

Local-only mode is the default. Shared initialization requires authorization and a clean Git working tree. The skill uses `bd` directly; it does not invoke a setup script or modify `application-delivery`.

Optional `setup-planning` may follow once the tracker is available.

Validation: `python3 -m unittest discover -s tests` from this skill directory.

## File structure scaffolded

```
project/
├── AGENTS.md                     # Updated: tracker declaration
├── docs/
│   └── agents/
│       └── issue-tracker.md
└── .beads/
    └── (tracker state)
```
