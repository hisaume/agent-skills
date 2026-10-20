---
name: prompt-residue-sweep
description: Lightly review finished human-readable prose such as READMEs, SKILL.md files, documentation, essays, code comments, and docstrings for prompt residue from drafting discussions. Report small exact excerpts and minimal replacements or deletions without rewriting the artifact or changing executable code.
---

# Prompt Residue Sweep

Inspect a finished text artifact for drafting or conversation context that does
not belong in the artifact itself. Report only clear, localised findings. Do not
perform a general prose review or rewrite.

## 1. Establish scope

1. Read the requested artifact and enough surrounding text to understand its
   purpose, audience, and voice. For repository work, inspect only the named
   file(s) or explicitly requested scope.
2. Examine human-readable prose, including comments and docstrings in source
   files. Leave executable code, identifiers, syntax, configuration values,
   machine-readable data, and quoted source material untouched.
3. Treat the artifact as a standalone deliverable for its intended reader,
   who has not participated in the conversation that produced it.

## 2. Identify residue

Look for traces of the drafting process that do not help the intended reader:

- References to the user's request, a previous answer, model behaviour, or
  earlier iterations (for example, "as discussed" or "I added this because").
- Explanations of why a section, format, or approach was chosen during drafting,
  instead of instructions or information relevant to the finished artifact.
- Conversational transitions, self-references, or reassuring commentary carried
  over from the authoring exchange.
- Comparisons with abandoned alternatives that have no enduring explanatory or
  operational value.
- Instructions about editing, expanding, or organizing the artifact embedded in
  instructions for using it. Flag these when artifact maintenance is outside the
  section’s purpose; preserve them in explicit maintenance guidance.
- References to specific people, products, tools, or workflows carried over from
  the drafting discussion when the underlying guidance is general. Preserve
  names where genuine dependencies or compatibility requirements exist.

Normally keep it if it passes the reader test:

- Would this passage make sense and provide value to someone who never saw the
  drafting conversation?
- Is this passage addressed to the reader performing the artifact’s stated task
  (as opposed to the person drafting or maintaining the artifact?)

Do **not** flag material merely for being explanatory, verbose, or stylistically
imperfect. Preserve useful design rationale, meaningful operational constraints,
explicit decision records, legitimate authorial voice, quotations, examples, and
texts about prompting where such language is the subject. When uncertain, omit
the finding rather than inventing a stylistic problem.

## 3. Propose minimal corrections

1. Admit only high-confidence residue with a clear, local fix.
2. Select the shortest exact source span that identifies the issue; include a
   full sentence only when a shorter excerpt would be ambiguous.
3. Prefer deletion when the surrounding text already states the useful content.
   Otherwise suggest the smallest replacement that preserves intended meaning,
   grammar, technical accuracy, and the author's voice.
4. Do not propose section rearrangements, broad paraphrasing, added content,
   terminology changes, or rewrites of unrelated passages.
5. Combine overlapping findings. Stop when further findings become speculative,
   repetitive, or ordinary copy-editing. Do not pad the result.

## 4. Report

Return a concise numbered list, in document order. For each finding, show:

- **Location:** file and line (when known), or a brief section reference.
- **Found:** the exact, minimal quoted span.
- **Suggested:** a minimal replacement, or **Delete**.

Use a short explanation only when the reason is not obvious. If no convincing
residue appears, say: **No clear prompt residue found.**

Do not modify files by default. Only apply the listed, localised corrections
when the user explicitly requests edits; leave all other text and formatting
unchanged. Do not create reports, backups, scripts, or auxiliary files unless
requested.
