# Cross-project Agent Conventions

## Project documentation

When a project contains L1-PROJECT.md, L2-DESIGN.md,
L3-COMPONENTS.md, or L4-IMPLEMENTATION.md (or without `L[1-4]-`), consult
PROJECT-DOCS.md in this directory for their intended
roles and interpretation.

Read only existing project documents relevant to the
task. Do not create missing documents or require all four
levels unless explicitly requested.

Respect explicit project requirements and distinguish
them from preferences, open decisions, and examples.

## All human-readable documentation

Prefer describing responsibilities positively. State
exclusions explicitly when they clarify genuine
ambiguity or enforce meaningful constraints.

## Code conventions

- Unless otherwise specified in a local style guide, follow these conventions:
  - Separate top-level declarations, functions, and tests with blank lines.
  - Within functions and tests, use blank lines to distinguish setup, operations, and assertions where it improves readability.
  - Run formatting and linting before finalizing.
  - Use the prompt-residue-sweep skill to clean up prompt residue, before finalizing the task.
