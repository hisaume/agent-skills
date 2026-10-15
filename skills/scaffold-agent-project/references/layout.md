# Standard project layout intention

```text
project/
├── AGENTS.md
├── CONTEXT.md
├── .agents/skills/application-delivery/
│   ├── SKILL.md
│   └── references/workflow.md
└── docs/
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

Read relevant existing ADRs under `docs/adr/` when present; the scaffold does not
create that optional directory.

Tracker-free guidance has no issue-claiming or closure requirements. Beads and
repository tracker modes describe the selected workflow without asserting that
initialization has occurred. Small changes with clear scope and bounded impact
can proceed from existing contracts; consequential changes still require
appropriate specification and slicing.

Project commands remain explicitly unconfigured. Generated delivery authority
requires user authorization for commits, pushes, pull requests, and external
tracker synchronization. Existing repository policy is preserved through
collision refusal rather than silently replaced.
