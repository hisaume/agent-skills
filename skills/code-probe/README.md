# code-probe

A disposable code-inspection skill for isolating one function or execution path without starting the entire application. The skill chooses a lightweight harness from the tooling already available in the repository, with two operating modes.

## Usage

**Auto-probe** runs a focused investigation and reports its observations:

```text
$code-probe Check whether compare() skips a target when its folder contains a source file.
```

**Debugger handoff** prepares a reusable entry point and VS Code launch configuration, without running behavioral checks:

```text
$code-probe handoff on compare()
```

A narrower handoff request typically results in a more specific test harness:

```text
$code-probe handoff on compare(), using a folder source and two target files.
```

## What it produces

- A small, disposable harness calling the real target implementation.
- Adjustable inputs and fake dependency responses grouped near the top of the harness.
- In auto-probe mode, observations and hypothesis findings.
- In handoff mode, a named debugger launch configuration (where appropriate) and start instructions.

The skill selects among direct scripts, REPL evaluation, existing test runners, dependency injection, fakes, and temporary resources. It does not use a mandatory escalation sequence or require a particular programming language.

## Boundaries

- **No automatic breakpoints.** Set them yourself in VS Code.
- **No unnecessary production changes.** Existing dependency seams and runtime tools are preferred.
- **No unapproved dependency installation or tracked configuration changes.** Existing `launch.json` entries are preserved; permission is required before altering a tracked one.
- **No automatic regression-test promotion.** Harnesses are disposable, but retained long enough for manual debugging or reuse.
- **Preserve existing handoffs.** Manual scenario edits and unrelated launch entries are retained. Malformed launch files receive a separate configuration snippet instead of being overwritten.
- **No implied verification in handoff mode.** The generated scenario is prepared for execution; behavior has not been tested by the agent.
