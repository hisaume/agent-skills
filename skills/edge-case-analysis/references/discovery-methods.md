# Edge-Case Discovery Methods

Use this guide during discovery and reconciliation.

Apply techniques selectively according to the project's
architecture, requirements and risks. Do not mechanically
generate scenarios for every category.

## 1. Establish the normal behaviour

First understand:
- The feature's intended outcome.
- Valid inputs and outputs.
- Important domain rules and invariants.
- State transitions and persistence.
- External systems and trust boundaries.
- Existing recovery and error-handling contracts.

Identify what must remain true even when operations fail.

## 2. Discovery techniques

### Boundaries and equivalence classes

Consider:
- Empty, missing, null and malformed values.
- Minimum, maximum and adjacent values.
- Size, length, quantity, precision and overflow limits.
- Unsupported formats or unexpected encodings.
- Valid inputs in unusual but permitted combinations.

Distinguish truly invalid input from uncommon valid input.

### Combinations and decision rules

Consider:
- Interactions between independently valid conditions.
- Contradictory configuration or permissions.
- Conflicting business rules.
- Order-sensitive behaviour.
- Multiple conditions becoming true simultaneously.

Use decision tables where combinations are important.
Avoid exhaustive combinations without a reason.

### State transitions and lifecycle

Consider:
- First use and initialization.
- Repeated operations and retries.
- Interrupted or incomplete operations.
- Expiration, deletion, migration and recovery.
- Invalid transitions and stale state.
- Idempotency and operations applied out of order.

### Concurrency and timing

Where relevant, consider:
- Simultaneous requests or modifications.
- Races between reading and writing.
- Timeouts and delayed responses.
- Duplicate delivery or execution.
- Ordering and eventual consistency.
- Cancellation during an in-flight operation.

### Dependency and environmental failures

Consider:
- Partial or complete dependency failure.
- Missing credentials, permissions or configuration.
- Network failure and transient unavailability.
- Version or schema incompatibilities.
- Filesystem, database or resource exhaustion.
- Deployment and rollback differences.

### Security and trust boundaries

Where relevant, consider:
- Authentication expiry or invalidation.
- Authorization at resource and operation boundaries.
- Untrusted or manipulated input.
- Cross-user or cross-tenant data exposure.
- Secret disclosure or unexpected information leakage.
- Abuse, rate limiting and cost amplification.

### Data and persistence integrity

Consider:
- Stale, corrupted or partially written data.
- Incompatible cache entries.
- Incomplete migrations.
- Duplicate or conflicting identifiers.
- Data loss and recovery behaviour.
- Mismatches between persisted and current state.

### Observability and operational consequences

Consider:
- Failures reported as success.
- Silent degradation.
- Repeated errors generating unexpected cost.
- Missing signals for important operational failures.
- Failure recovery that creates secondary damage.

## 3. Evidence and admission

For each candidate, establish:

1. Trigger: What specific situation produces it?
2. Consequence: What meaningful problem might result?
3. Evidence: Why is this plausible in this project?
4. Behaviour: What should happen instead?
5. Verification: How could that behaviour be checked?

Evidence may include:
- A requirement or specification.
- A relevant code path or system boundary.
- A reproducible observation or incident.
- A credible failure mode of a dependency.
- A clearly identified design assumption.

Do not present hypotheses as observed defects.

If expected behaviour is undefined, record an unresolved
decision rather than silently specifying a new contract.

## 4. Risk and confidence

Assess risk using:
- Potential severity.
- Plausibility of occurrence.
- Exposure and blast radius.
- Recoverability.
- Existing safeguards.

Assess confidence separately using the available evidence;
record it only when uncertainty affects a decision or investigation.

Do not invent numerical failure probabilities.

Reject or consolidate scenarios that are:
- Physically or architecturally implausible.
- Redundant with an existing case.
- Consequence-free or merely cosmetic.
- Based on unsupported chains of assumptions.
- Unactionable without a meaningful investigation path.
- Routine process rules or test arrangements without a
  consequential failure mechanism.

Low risk alone does not exclude a useful case: blocked user
actions, recurring regressions and important accepted tradeoffs
can warrant inclusion. Keep the expected behaviour focused on
the observable safeguard rather than implementation detail.

Retain uncertain but potentially severe scenarios only
when there is a credible mechanism worth investigating.

## 5. Choosing verification

Suggest the smallest suitable verification method:

- Example-based unit tests for isolated behaviour.
- Integration tests for component boundaries.
- Contract tests for external interfaces.
- Property-based tests for general invariants.
- Stateful tests for complex transitions.
- Concurrency or fault-injection tests where warranted.
- End-to-end tests for user-visible workflows.
- Configuration or operational checks where executable
  application tests are inappropriate.

Use the project's existing test framework and conventions.
Do not introduce new tooling solely for a speculative case.

Not every admitted case requires a new test. Some require
a specification decision, design correction, or conscious
acceptance of risk.

## 6. Reconciliation rules

Compare each in-scope finding with:
- Existing register entries.
- Specifications and accepted design decisions.
- Relevant implementation paths.
- Actual test assertions and available results.
- Current issues or recorded incidents.

Then:
- Add genuinely missing findings.
- Merge duplicates without losing important references.
- Consolidate only when safeguards, verification and status
  can be shared; separate cases needing different treatment.
- Update expectations when a decision is established.
- Mark Covered only when verification supports the full
  expected behaviour; otherwise keep confirmed, applicable
  cases Open unless the developer has accepted the risk.
- Mark Retired only when the condition no longer applies.
- Preserve historical IDs and meaningful decisions.
- Do not delete unresolved risks to make coverage appear
  more complete.

Distinguish test existence from a passing test run.

Report partial coverage precisely rather than treating a
related test as full coverage.

Tests of verification machinery establish that machinery's
behaviour, not the system it checks. Require deployment
evidence only for expectations that depend on deployment.

Link locatable evidence or describe the concrete observation;
avoid unexplained trial numbers and experiment shorthand.

## 7. Efficiency rule

Prefer a small number of high-value findings to a broad
inventory of speculative possibilities.

Stop expanding a category when additional scenarios no
longer produce distinct, consequential, actionable insight.
