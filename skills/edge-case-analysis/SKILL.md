---
name: edge-case-analysis
description: Discover, prioritise and reconcile meaningful edge cases in software projects. Use during requirements planning before specification, when reviewing failure scenarios, or when auditing existing code, tests and documentation for missing edge cases.
---

# Edge-Case Analysis

Discover meaningful edge cases and maintain a durable,
project-specific record of them.

This skill performs analysis and documentation. It does not
automatically implement fixes or write tests.

## 1. Shared preparation

1. Select the operating mode:
   - **Discovery:** Explore requirements, proposed designs or
     features before formal specification.
   - **Reconciliation:** Review existing cases against current
     specifications, implementation, tests and evidence.

   Use Discovery during initial planning and Reconciliation
   during maintenance or coverage audits. Both modes use
   the shared assessment, documentation and completion rules.

2. Establish scope:
   - Work within the current project's repository root.
   - Prefer a named feature or subsystem over a full-project
     audit unless broader coverage is requested.
   - During maintenance, focus on changed or affected behaviour.
   - Do not expand scope merely to generate more findings.

3. Inspect relevant project instructions, requirements,
   architecture, domain rules and existing documentation.
   Locate any existing edge-case register before making changes.

4. Identify intended behaviour, inputs, outputs, invariants,
   states, dependencies and significant failure boundaries.

5. Establish sources of authority:
   - Explicit requirements and accepted design decisions
     define intended behaviour.
   - Implementation, tests and incidents provide evidence
     of actual behaviour and existing safeguards.
   - Tests are authoritative for their assertions, not for
     requirements they were never intended to establish.
   - Do not silently turn observed implementation behaviour
     or undocumented assumptions into product requirements.

6. Respect existing project conventions and documentation.
   Do not introduce competing registers or independently
   redefine established contracts.

Do not modify implementation or test code unless separately
requested. Honour explicitly read-only requests.

## 2A. Discovery

Use when exploring requirements, planning a feature or
challenging a proposed design.

Prefer running after requirements exploration and before
formal specification.

1. Examine the feature's normal behaviour and its significant
   boundaries, assumptions and failure conditions.
2. Apply `references/discovery-methods.md` selectively to
   discover non-obvious scenarios.
3. Identify plausible triggers, consequences, supporting
   evidence and potential verification approaches.
4. Distinguish established expected behaviour from unresolved
   design questions.

Pass candidate findings to shared assessment.

Do not mechanically enumerate every possible boundary or
assume missing requirements are established facts.

## 2B. Reconciliation

Use during maintenance, after feature changes or when
auditing existing coverage.

1. Read the existing edge-case register, if present.
2. Inspect relevant specifications, implementation, tests,
   issues and available incident evidence.
3. Compare registered cases with current intended behaviour,
   actual implementation and verification coverage.
4. Identify missing, duplicated, obsolete, conflicting or
   partially addressed cases.
5. Identify affected cases requiring updated expectations,
   risk assessments, status or verification references.
6. Apply `references/discovery-methods.md` where additional
   scenario discovery is warranted.

Pass candidate additions and revisions to shared assessment.

Do not infer coverage merely from the existence or naming
of related tests.

## 3. Shared assessment

Apply the same admission, prioritisation and stopping rules
to both modes.

### Admission

Only admit a finding when it has:

- A plausible triggering condition.
- A meaningful consequence if mishandled.
- A distinct risk or behaviour not already documented.
- An actionable decision, mitigation or verification path.

Reject or consolidate arbitrary, implausible, redundant or
purely hypothetical cases without meaningful consequences.

Uncertain but potentially severe cases may be retained when
there is a credible mechanism worth investigating.

### Risk and confidence

Assign risk and confidence separately.

Risk:
- **High:** Security, privacy, material cost, data integrity,
  major availability or critical correctness failures.
- **Medium:** Meaningful functional errors or recoverability
  problems.
- **Low:** Minor or cosmetic consequences.

Confidence expresses the strength of evidence supporting the
proposed triggering scenario.

Use High, Medium or Low for each. Do not invent numerical
failure probabilities.

Prefer high- and medium-value findings. Low-value cases
should normally be omitted or consolidated.

### Prioritisation and stopping

- Prioritise distinct, consequential and actionable findings.
- Default to at most ten new findings per pass; do not pad
  the count.
- If important findings exceed the limit, prioritise them
  and disclose the remaining scope.
- Stop expanding a category when further scenarios no longer
  produce meaningful new insight.
- Do not run exhaustive audits during routine tasks.

### Escalation

- Make routine evidence-supported documentation decisions
  without requiring approval for every entry.
- Escalate consequential ambiguity or a decision that cannot
  responsibly be inferred.
- Offer a proposed resolution when expected behaviour is
  unresolved, clearly labelled as a proposal.
- Never silently invent product requirements or accept risks
  on the developer's behalf.

## 4. Canonical documentation

Maintain the project-local register:

`docs/quality/edge-cases.md`

- If absent, create it using `assets/edge-cases.template.md`,
  but only when there are admitted findings.
- If present, reconcile rather than replace it.
- If an equivalent register already exists elsewhere, respect
  explicit project instructions and avoid creating a competing
  register. Resolve material location conflicts before writing.
- Keep existing case IDs stable and assign new sequential
  `EC-NNN` identifiers.
- Never reuse retired identifiers.
- Merge duplicate cases without losing references or history.
  Retain a primary case and preserve redundant identifiers
  through linked retired entries or existing aliases.
- Do not delete unresolved risks to make coverage appear
  more complete.
- Record trigger, impact, expected behaviour, evidence,
  risk, confidence, status and verification reference.
- Distinguish established expectations from proposals and
  unresolved decisions.
- Link to specifications, issues and tests rather than
  reproducing their contents.

### Status definitions

- **Proposed:** Plausible finding awaiting confirmation of
  assumptions, applicability or expected behaviour.
- **Open:** Applicable finding requiring action or verification.
- **Covered:** Expected behaviour supported by relevant
  verification evidence, not merely a related test reference.
- **Accepted:** Risk explicitly accepted by the developer;
  preserve the decision and its reference.
- **Retired:** Case no longer applicable or consolidated into
  another case; preserve its ID and relevant history.

### Evidence and verification

- Inspect actual test assertions before claiming coverage.
- Do not assume a test passes unless execution evidence
  confirms that result.
- Record known verification results or limitations.
- Do not represent historical verification as a current run.
- Report partial coverage precisely.
- Keep executable validations in the project's normal test
  suite, not in the register.
- Not every admitted case requires a new test; some require
  a design decision, correction or conscious risk acceptance.

The register is the catalogue of scenarios and decisions.
It does not supersede authoritative requirements or
executable verification.

## 5. Completion and reporting

Summarise:

1. Scope and mode used.
2. New or updated findings, highlighting the most important.
3. Unresolved decisions requiring user input.
4. Missing verification or recommended follow-up actions.
5. The register path and whether it was created, updated
   or left unchanged.

Before completion:

- Ensure findings meet admission criteria and are deduplicated.
- Confirm identifiers, statuses and references remain consistent.
- Preserve existing decisions and historical information.
- Distinguish verified facts from hypotheses and proposals.
- Stop when meaningful risks within the requested scope have
  been addressed.

Keep reporting concise. Do not reproduce the entire register
in the response.
