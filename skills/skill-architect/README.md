# skill-architect

Designs, reviews, and refines reusable Agent Skills (`SKILL.md`) with an emphasis on clear responsibilities, reliable guardrails, and low maintenance overhead.

## Usage

**Create — design and implement a new skill**

`$skill-architect Create a reusable skill for database migration reviews.`

**Review — assess an existing skill without editing files**

`$skill-architect Review edge-case-analysis for maintainability and guardrails. Do not modify it.`

**Refine — implement justified improvements**

`$skill-architect Refine edge-case-analysis based on the review findings.`

## Approach

- Establish scope, target agent, existing conventions, and permitted changes.
- Review triggering, workflow structure, responsibilities, side effects, documentation hygiene, and stopping rules.
- Prefer focused edits to unnecessary restructuring; **no change needed** is a valid outcome.
- Keep the main workflow portable and add references, assets, or scripts only where they provide a concrete benefit.
- Validate metadata, links, realistic invocations, and compatibility with existing behaviour.

## Files

- `SKILL.md` — complete workflow and assessment criteria.
