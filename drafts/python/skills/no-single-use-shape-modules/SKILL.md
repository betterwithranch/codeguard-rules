---
name: no-single-use-shape-modules
description: A passive shape that only one type uses (its parameter, result or field shape) is defined in that type's module, not in a module of its own.
---

# A type's own shapes live in its module

A shape that exists only to serve one type is part of that type and is defined beside
it.

A passive shape is a class that only holds data: a dataclass, pydantic model, attrs
class, `TypedDict`, `NamedTuple` or msgspec `Struct` with no methods beyond the ones
its library generates, a `@property` over its own fields, or a validator.

A shape's users are the places outside its own module that name it: imports,
annotations, constructor calls, `isinstance` checks, tests excluded. Its owner is the
one type whose module holds all of those uses, when there is one: the shape appears
only as that type's method parameters, results or fields, or is built only inside its
methods.

## The test

For each passive shape the file defines or imports from another module of the program,
ask: does exactly one type, defined in another module, use it, with no other user
anywhere in the program (Grep for the shape's name)? If so, it is defined outside its
owner's module, which is a violation.

Two places show it:

- the file under review defines the shape, and its only user is one type in another
  module;
- the file under review defines the owner type and imports the shape from a module of
  the program where nothing else uses it.

Not a violation:

- a shape used by two or more types, modules or packages, including a function in
  another module or a second class;
- a shape that crosses a boundary in its own right: a request or response body a web
  framework route or a DRF view declares, a message a queue consumer reads, a row a
  repository returns to several callers;
- a shape defined in its owner's module;
- a class with behavior of its own (it is a type, not a shape).

## Violation

A passive shape whose only user is one type, defined in another module than that type:
`RetryAttemptParams` in `retry/retry_attempt_params.py` and `RetryAttempt` in
`retry/retry_attempt.py`, each used only by `RetryAttemptPolicy.next_attempt` in
`retry/retry_attempt_policy.py`, whether the change adds the shape module or the import
of it.
