# implementation-seeding

Guides the internal shape of an agent's implementation through a few deliberate
source-code anchors, without writing a complete low-level design or implementing
the feature.

## Usage

**Seed — before implementation**

`$implementation-seeding Seed the folder-scanning feature with a few cohesive function boundaries.`

**Adopt — use a hand-written scaffold**

`$implementation-seeding Adopt my partial skeleton in src/scanner.py as implementation guidance.`

**Reconcile — during implementation**

`$implementation-seeding Reconcile the scanner scaffold with the code now implemented.`

**Review — without edits**

`$implementation-seeding Review where a minimal scaffold would help the cache refactor. Do not edit.`

## Output

- Minimal source declarations, signatures, or call outlines where useful; no
  arbitrary full implementation or boilerplate.
- A small, scoped project agent-guidance entry identifying the affected files
  and any explicit fixed anchors, when the project supports one.
- A handoff identifying provisional decisions and unfinished stubs.

The source skeleton guides later agents; it does not require every later agent
session to re-invoke this skill. Those agents must still read the applicable
project guidance and source. Reconcile and retire guidance as the code evolves.

## Boundaries

This is an **optional implementation-design aid**, not a replacement for
specifications, tests, or delivery workflows. Existing contracts outrank the
scaffold. User-confirmed anchors are binding; suggested private structure can
change. It does not automatically invoke or modify a project-local
`application-delivery` workflow.

## Files

- `SKILL.md` — seeding, adoption, reconciliation, and handoff procedure.
