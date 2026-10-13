
# Edge-Case Register

This document is the project's canonical catalogue of
material edge cases, decisions, risks and verification
references.

It is maintained by the `edge-case-analysis` skill and
may also be updated during other engineering workflows.

## Conventions

- IDs use `EC-NNN` and are never reused.
- Existing entries are updated rather than duplicated.
- Expected behaviour must distinguish established
  requirements from proposals or unresolved decisions.
- Executable validations live in the normal test suite.
- This register references tests; it does not replace them.
- Historical cases remain available when retired.

### Status definitions

| Status | Meaning |
|---|---|
| Proposed | Finding awaiting confirmation |
| Open | Confirmed, requiring action or verification |
| Covered | Relevant verification exists |
| Accepted | Risk consciously accepted |
| Retired | No longer applicable |

Risk and confidence are independently rated High,
Medium or Low.

## Cases

<!--
Copy this format for each real finding, beginning at EC-001.
Remove these instructions and placeholders when populating.

### EC-001 — Concise title

- **Area:** Feature or subsystem
- **Status:** Proposed
- **Risk:** High / Medium / Low
- **Confidence:** High / Medium / Low
- **Trigger:** Specific condition causing the scenario.
- **Impact:** Meaningful consequence if mishandled.
- **Expected behaviour:** Confirmed behaviour, or an
  explicitly unresolved decision.
- **Evidence:** Requirement, code path, incident, or
  reasoned architectural failure mode.
- **Verification:** Test path and test name, or Not covered.
- **Work item:** Issue/specification reference, if any.

-->
