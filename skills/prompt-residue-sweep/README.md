# prompt-residue-sweep

Reviews finished human-readable prose for conversational or drafting residue without turning the review into general copy-editing.

## Usage

**Review documentation**

`$prompt-residue-sweep Review this README.md for prompt residue. Report findings only.`

**Review code comments**

`$prompt-residue-sweep Check the docstrings in src/library.py for prompt residue.`

## Output

Reports high-confidence findings with the location, shortest exact source excerpt, and a minimal replacement or deletion. If no clear residue is found, says so.

The skill preserves legitimate explanations, quoted material, and authorial voice. It does not edit files unless explicitly requested, and never modifies executable code.

## Files

- `SKILL.md` — review criteria, minimal-correction rules, and reporting format.
