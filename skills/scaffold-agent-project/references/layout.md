# Standard project layout

```text
project/
├── AGENTS.md
├── CONTEXT.md
├── .agents/skills/application-delivery/
│   ├── SKILL.md
│   └── references/workflow.md
└── docs/
    ├── adr/
    └── specs/README.md
```

`AGENTS.md` is always-loaded project configuration: sources of truth, concrete
commands, non-obvious invariants, and delivery authority. It is not a workflow
manual.

`CONTEXT.md` holds domain vocabulary and invariants. Delete it only if the
project has no durable domain language worth preserving.

`application-delivery` is the reusable, on-demand project workflow. Its
`workflow.md` is a detailed tracker lifecycle and must name only the
repository's authoritative validation command concept, not an assumed command.

`docs/specs/README.md` is the stable entry point for a project with multiple
specifications, amendments, or superseded decisions. It may say that no active
specification exists yet.

`.beads/` remains Beads-managed state. Do not use it as a template asset.
