---
name: context-types-live-with-consumer
description: A dependency or context class is defined in the package of the stage or service that consumes it, and never in a module of output schemas.
---

# Dependency and context classes live with their consumer

The inputs a stage or service needs to run are part of that stage, not of the data it
produces.

A dependency or context class is a class whose fields hold what a stage, service,
handler or agent needs in order to run: collaborators (an HTTP client, a repository, a
database session, a cache), settings, or the run's context (the current user, a tenant,
a request id, a deadline). Examples: a pydantic-ai `deps_type` dataclass, a
`ServiceContext` a handler receives, a `PipelineDeps` a stage takes.

Its consumer is the stage or service whose code takes it as a parameter or field and
reads it. A module of output schemas is one whose other classes are the results,
responses or records the program produces (`schemas.py`, `results.py`, a module of
pydantic response models).

## The test

For each dependency or context class the file defines, ask: which stage or service
reads it? Grep the program for its name. Then ask: is it defined in that consumer's
package, in a module that is not a module of output schemas?

This holds for dataclasses, pydantic models, attrs classes, `TypedDict`s and
`NamedTuple`s alike.

Not a violation:

- a context class in its consumer's module, or in its own module in the consumer's
  package;
- an output schema in a module of output schemas;
- a class that stages in several packages read (program-wide settings loaded once at
  start-up): it has no one consumer package, so the test doesn't place it.

## Violation

A dependency or context class defined in a module of output schemas
(`ReviewDeps` beside `ReviewResult` and `Finding` in `review/schemas.py`), or in a
package other than its consumer's (`ImportContext` read only by `imports/stages.py`,
defined in `shared/context.py`).
