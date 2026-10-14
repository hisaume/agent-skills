# Cross-project Agent Conventions

## Artifact handoff

When producing human-readable prose in finished artifacts (code comments, documentation, essays, skills, etc.), write for its intended future reader, not for the conversation that produced it. Incorporate planning decisions without narrating the planning process. Remove conversational residue, self-referential commentary, and explanations of why content was included or structured a certain way, unless that rationale is genuinely useful to the artifact's reader. Before finalizing, review the artifact for such residue and remove or rewrite it.

## Edge-case documentation

- Use `docs/quality/edge-cases.md` as the canonical register of material edge cases within each project.
- When meaningful edge cases emerge during planning, implementation, review, testing, or maintenance, reconcile them with this register.
- Create the register on first use if absent, using the template supplied by the `edge-case-analysis` skill.
- Keep stable case IDs and record triggering conditions, expected behavior, risk, status, and verification references.
- Avoid duplicate edge-case inventories. Other documents may discuss cases but should reference the canonical register where practical.
- Keep executable validations in the project's normal test suite, not in skills or the edge-case register.
- Use the `edge-case-analysis` skill for dedicated discovery or reconciliation work.
- Do not perform full-project edge-case audits automatically during unrelated or trivial tasks.
- Keep documentation proportionate to the project's size and actual risks.
