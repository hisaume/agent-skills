# Cross-project Agent Conventions

---

## Project documentation

When a project contains PROJECT.md, DESIGN.md, COMPONENTS.md, or
IMPLEMENTATION.md (optionally prefixed with L1-, L2-, L3-, or L4-),
consult PROJECT-DOCS.md in this directory for their intended
roles and interpretation.

Read only existing project documents relevant to the
task. Do not create missing documents or require all four
levels unless explicitly requested.

Respect explicit project requirements and distinguish
them from preferences, open decisions, and examples.

---

## Human-readable documentation

Prefer describing responsibilities positively. State
exclusions explicitly when they clarify genuine
ambiguity or enforce meaningful constraints.

### Markdown style

By default, write in a **structured, concise, technical Markdown style**, choosing the format that best reflects the nature of the information.

- Use bullet lists for discrete items, attributes, requirements, constraints, rules, or independently meaningful statements.
- Use paragraphs for cohesive explanations, workflows, sequential behaviour, and related statements that naturally form continuous prose.
- Use tables for comparisons, mappings, or consistently structured information.
- Group related information under meaningful headings.
- Keep paragraphs focused and reasonably short, without artificially splitting cohesive explanations into bullets.
- Express distinct ideas separately when doing so improves clarity or makes the information easier to reference.
- Avoid repetitive phrasing, unnecessary transitions, and conversational filler.
- Preserve technical precision, logical relationships, qualifications, and exceptions.

**Guiding principle:** Structure information according to its logical form, not a fixed preference for bullets or prose. Use lists when readers benefit from scanning individual items; use paragraphs when readers benefit from following a connected explanation.

The result should resemble well-organized technical documentation or a concise specification, rather than an essay, transcript, or collection of disconnected bullet points.

---

## Code conventions

- Unless otherwise specified in a local style guide, follow these conventions:
  - Separate top-level declarations, functions, and tests with blank lines.
  - Within functions and tests, use blank lines to distinguish setup, operations, and assertions where it improves readability.
  - Run formatting and linting before finalizing.
  - Use the prompt-residue-sweep skill to clean up prompt residue, before finalizing the task.
