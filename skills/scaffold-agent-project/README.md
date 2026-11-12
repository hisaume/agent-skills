# scaffold-agent-project

Creates a tracker-neutral agent-guidance baseline without overwriting existing files.

```bash
python3 ~/.agents/skills/scaffold-agent-project/scripts/scaffold.py --target /path/to/project --dry-run
python3 ~/.agents/skills/scaffold-agent-project/scripts/scaffold.py --target /path/to/project
```

Output: `AGENTS.md`, `GLOSSARY.md`, `docs/specs/README.md`, and `.agents/skills/application-delivery/SKILL.md`. Project commands and domain details remain unconfigured. A tracker can be added separately.

The deterministic generator previews destinations, refuses collisions and unsafe paths, and reports partial failures. Test with `python3 -m unittest discover -s tests` from the skill directory.

## File structure scaffolded

```
project/
├── AGENTS.md
├── GLOSSARY.md
├── docs/
│   └── specs/
│       └── README.md
└── .agents/
    └── skills/
        └── application-delivery/
            └── SKILL.md
```
