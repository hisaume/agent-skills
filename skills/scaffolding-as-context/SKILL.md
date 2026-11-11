---
name: scaffolding-as-context
description: Prepare, interpret, or reconcile intentional partial source files that guide implementation. Use for code-level contracts, file boundaries, or advisory hints; not for generic project boilerplate.
---

# Scaffolding as Context

Use deliberate source scaffolds to communicate implementation intent. Express precise decisions in code where practical. It may complement other implementation documentation.

## 1. Establish scope and authority

1. Choose the operation: **Review** (propose only), **Seed** (create), **Adopt** (recognise existing scaffolds), **Consume** (implement using them), or **Reconcile** (update or retire them).
2. Read the affected source, tests, and applicable project contracts. Limit attention and edits to the relevant area.
3. Distinguish authority:
   - **Contractual:** Deliberate, user-confirmed code, schemas, signatures, or established constraints. Preserve unless a change is authorised.
   - **Unspecified:** Default to the above, until proven otherwise.
   - **Advisory:** Suggestions explicitly labelled `Advisory:` in comments. Apply best effort; revise when justified.
4. Flag material conflicts or unclear authority rather than silently overriding a contract.

## 2. Work with scaffolds

1. **Review:** Suggest the smallest useful scaffold without editing.
2. **Seed:** Create only high-leverage files, declarations, signatures, fixed code, or short comments. Leave incidental helpers and algorithms open. Make incomplete code recognisable as unfinished and syntactically valid where practical.
3. **Adopt / Consume:** Respect contractual anchors and treat advisory notes as guidance. Consume mode continues the requested implementation; it does not stop at scaffolding. Remove temporary placeholders or advisory notes once superseded.
4. **Reconcile:** Compare scaffolds with implemented code, retire stale guidance, and preserve working behaviour and unrelated files.

## 3. Handoff and completion

When delegating, identify relevant source paths and any consequential contracts through the existing handoff; do not assume another agent inherited invocation context. Report files affected, contractual versus advisory decisions, incomplete work, conflicts, and checks actually run. Do not commit, push, or expand into full implementation unless separately requested.
