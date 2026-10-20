# implementation-brief

**Experimental.** Presents a provisional, implementation-level approach to an
already-planned feature, fix, refactor, or maintenance change. Useful for
exploring how much function-level design should be specified before coding.

## Usage

`$implementation-brief Present the likely function and module boundaries for the planned import feature.`

`$implementation-brief Focus on state ownership, helper delegation, and where defaults should live in the cache refactor.`

## Output

A proportionate, read-only presentation of likely code organisation, data flow,
and relevant implementation choices. Distinguishes established constraints,
agent proposals, and choices deferred until coding. **Unknown details are
acceptable**; the skill is not a demand for a complete implementation blueprint.

## Boundaries

Assumes the intended feature is already understood. Does not grill the user,
request approval, modify files, scaffold functions, or implement the change.
Independent of `feature-brief` and `implementation-seeding`.

## Files

- `SKILL.md` — context review, provisional design, uncertainty policy, and stopping rules.
