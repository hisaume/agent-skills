
---
name: edge-case-analysis
description: Discover, prioritise and reconcile meaningful edge cases in software projects. Use during requirements planning before specification, when reviewing failure scenarios, or when auditing existing code, tests and documentation for missing edge cases.
---

# Edge-Case Analysis

Discover meaningful edge cases and maintain a durable,
project-specific record of them.

This skill performs analysis and documentation. It does not
automatically implement fixes or write tests.

## Modes

### Discovery

Use when exploring requirements, planning a feature, or
challenging a proposed design.

Prefer running after requirements exploration and before
formal specification.

1. Read available requirements, design documents, domain
   rules and relevant architecture.
2. Identify inputs, outputs, invariants, states, dependencies
   and significant failure boundaries.
3. Apply `references/discovery-methods.md` to discover
   non-obvious scenarios.
4. Filter, deduplicate and prioritise findings.
5. Separate confirmed expected behaviour from unresolved
   design questions.
6. Reconcile admitted findings with the project register.

Do not assume missing requirements are established facts.

### Reconciliation

Use during maintenance, after feature changes, or when
auditing existing coverage.

1. Read the existing edge-case register, if present.
2. Inspect relevant specifications, implementation, tests,
   issues and available incident evidence.
3. Compare documented cases with actual system behaviour
   and verification coverage.
4. Identify missing, duplicated, obsolete or partially
   addressed cases.
5. Update records while preserving stable identifiers.
6. Report outstanding risks and actionable coverage gaps.

Reconciliation may discover new cases. Apply the same
admission criteria as Discovery.

## Scope

- Work within the current project's repository root.
- Prefer a named feature or subsystem over a full-project
  audit unless broader coverage is requested.
- For maintenance, focus on changed or affected behaviour.
- Do not expand scope merely to generate more findings.
- Do not modify implementation or test code unless the
  user separately requests that work.

## Admission criteria

Only record a scenario when it has:

- A plausible triggering condition.
- A meaningful consequence if mishandled.
- A distinct risk or behaviour not already documented.
- An actionable decision, mitigation or verification path.

Do not record arbitrary, purely hypothetical or redundant
cases merely to increase the count.

Use the reference guide for detailed discovery techniques,
risk assessment and filtering.

## Prioritisation

Assign risk and confidence separately.

Risk:
- High: security, privacy, material cost, data integrity,
  major availability or critical correctness failures.
- Medium: meaningful functional errors or recoverability
  problems.
- Low: minor or cosmetic consequences.

Confidence expresses the strength of evidence supporting
the proposed triggering scenario.

Prefer high- and medium-value findings. Low-value cases
should normally be omitted or consolidated.

Default to at most ten new findings per pass. Do not pad
the count. If important findings exceed this limit,
prioritise them and disclose the remaining scope.

## Canonical documentation

Maintain the project-local file:

`docs/quality/edge-cases.md`

- If absent, create it using
  `assets/edge-cases.template.md`.
- Create it only when there are admitted findings.
- If present, reconcile rather than replace it.
- Keep existing case IDs stable and assign new sequential
  `EC-NNN` identifiers.
- Do not reuse retired identifiers.
- Record trigger, impact, expected behaviour, evidence,
  risk, confidence, status and verification reference.
- Mark unresolved expectations explicitly.
- Link to existing specifications, issues and tests instead
  of reproducing their contents.
- Never create competing edge-case registers.

Use these statuses:
- Proposed: plausible finding awaiting confirmation.
- Open: confirmed case requiring action or verification.
- Covered: expected behaviour has relevant verification.
- Accepted: risk consciously accepted by the developer.
- Retired: case no longer applicable.

Never mark a case Covered merely because a test has a
similar filename or name. Inspect what it actually asserts.

Do not assume a test passes unless its execution confirms
that fact.

An executable test is authoritative for its assertions;
the register remains the catalogue of scenarios and
decisions.

## Interaction

- Make routine, evidence-supported documentation updates
  without requiring approval for every entry.
- Ask only when a consequential behaviour is ambiguous
  or a decision cannot responsibly be inferred.
- Offer a proposed resolution for unresolved decisions,
  clearly labelled as a proposal.
- Never silently invent product requirements.
- Do not run an exhaustive audit during routine tasks.

## Output

Summarise:
1. Scope and mode used.
2. New or updated findings, highlighting the most important.
3. Unresolved decisions requiring user input.
4. Missing verification or recommended follow-up actions.
5. The register path and whether it was created or updated.

Keep reporting concise. Do not reproduce the entire register
in the response.
