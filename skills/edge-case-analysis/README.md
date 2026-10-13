# edge-case-analysis

Discovers, prioritises, and reconciles meaningful edge cases in software projects, during both initial planning and ongoing maintenance.

## Usage

**Discovery — before specification**

`$edge-case-analysis Discover edge cases in the authentication flow before to-spec.`

Examines requirements, domain rules, system boundaries, and potential failure scenarios. Filters out trivial or speculative findings.

**Reconciliation — during maintenance**

`$edge-case-analysis Reconcile edge cases in the caching subsystem against existing code and tests.`

Audits existing findings, checks verification coverage, identifies omissions, and updates documentation without duplicating cases.

## Output

Creates or updates the project-local register:

`docs/quality/edge-cases.md`

- Records triggers, consequences, expected behaviour, risks, and evidence.
- Preserves stable case identifiers across revisions.
- Tracks resolution and links to executable tests, specifications, or issues.
- Distinguishes confirmed behaviour from unresolved design decisions.

The skill performs analysis and documentation, not implementation or test generation. Executable validations remain in the project's normal test suite.

## Skill files

- `SKILL.md` — discovery and reconciliation workflow.
- `references/discovery-methods.md` — techniques, risk assessment, and filtering rules.
- `assets/edge-cases.template.md` — template for the project-local register.

No additional dependencies or scripts are required.
