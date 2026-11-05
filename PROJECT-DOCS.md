# Four-Layer Project Documentation

## Purpose

This documentation system provides a lightweight, adaptable structure for planning software and system projects and communicating design decisions to implementation and execution agents.

It organises specifications into four levels of abstraction, from product intent to code-level implementation. Each level addresses a different subject, **not a mandatory degree of detail or prescription**.

The four levels are conceptual boundaries, not requirements to maintain four separate files.

## Document Structure

| Level                          | Document               | Central question                                                                       |
| ------------------------------ | ---------------------- | -------------------------------------------------------------------------------------- |
| **L1 - Product Brief**         | `L1-PROJECT.md`        | What are we building, for whom, why, and what should users accomplish?                 |
| **L2 - System Architecture**   | `L2-DESIGN.md`         | What are the major components, technologies, boundaries and relationships?             |
| **L3 - Component Design**      | `L3-COMPONENTS.md`     | How is each component logically organised, and how do its internal parts collaborate?  |
| **L4 - Implementation Design** | `L4-IMPLEMENTATION.md` | How should the design translate into files, functions, data structures and algorithms? |

### L1 - Product Brief

Defines the application's purpose, intended users, primary usage scenarios, scope and success criteria.

Generally independent of technology and implementation choices. Intended to remain relatively stable as the technical design evolves.

### L2 - System Architecture

Describes the application's major building blocks, their responsibilities, deployment arrangements, technology choices and communication boundaries.

Examples include frontend/backend separation, runtime environment, hosting platform and principal storage technology.

### L3 - Component Design

Describes the internal logical organisation of individual components.

May define modules, responsibilities, interfaces, behavioural contracts, data flows, dependencies, constraints and verification requirements.

**Logical modules do not necessarily correspond to source files or classes.**

### L4 - Implementation Design

Provides selective code-level guidance, including source-file organisation, function signatures, library APIs, algorithms, control flow, error handling and concrete tests.

Can specify individual implementation details without prescribing the surrounding codebase.

## Operating Principles

1. **Abstraction and prescription are independent.** Any level may contain declarative requirements, precise constraints or imperative instructions.
2. **Detail is selective.** The document author may specify some areas exhaustively while leaving others minimally described.
3. **Flexibility belongs to the author.** The structure accommodates different planning styles. It does not automatically grant implementation agents discretion over documented requirements.
4. **Decisions belong near their relevant scope.** System-wide choices generally belong in L2, component-specific decisions in L3, and code-level decisions in L4.
5. **Boundaries are intentionally approximate.** A decision may reasonably fit several levels. Clarity, maintainability and ease of retrieval take precedence over strict classification.
6. **Uncertainty should remain identifiable.** Fixed requirements, preferences, deliberately delegated decisions and unresolved questions should be distinguishable where their status matters.

## Consolidation and Progressive Detail

All four levels need not be represented as separate files.

- Small projects may combine L1 and L2 in `PROJECT.md`.
- L2 and L3 may coexist in `DESIGN.md`, with component-specific sections.
- L4 may be omitted entirely or limited to individual modules, functions or concerns.
- Larger projects may extract sections into separate documents when their size or maintenance requirements justify it.

A useful default is to begin with a small number of documents and expand only where necessary.

The goal is sufficient specification for the project, not completion of a prescribed documentation hierarchy.
