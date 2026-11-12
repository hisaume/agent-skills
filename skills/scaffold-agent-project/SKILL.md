---
name: scaffold-agent-project
description: Create tracker-neutral agent guidance and an application-delivery skill for a new project. Use when preparing a project root for agentic work.
---

# Scaffold agent project

Create the baseline agent-guidance layout without configuring project-specific commands, domain rules, or work tracking.

## Inspect and preview

1. Identify the project root. Inspect existing `AGENTS.md`, `.agents/`, and `docs/`; refuse to overwrite established guidance or unsafe paths.
2. Resolve `scripts/scaffold.py` relative to this skill's directory. Preview the four intended files:

   ```bash
   python3 <skill-directory>/scripts/scaffold.py --target <project-root> --dry-run
   ```

3. If the preview is acceptable, run the same command without `--dry-run`. Use `--project-name` only when a different display name is needed. Never bypass a refusal; preserve and report partial output after failure.

## Verify and stop

- Confirm `AGENTS.md`, `GLOSSARY.md`, `docs/specs/README.md`, and `.agents/skills/application-delivery/SKILL.md` exist.
- Report the created files and any blocked output. Commands and domain content remain unconfigured.
- Do not fill placeholders, install a tracker, or modify existing project guidance without a separate request. The delivery skill works with an independently configured tracker or with none.
