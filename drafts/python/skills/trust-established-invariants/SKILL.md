---
name: trust-established-invariants
description: No guard re-checks a condition that other visible code already guarantees, such as the dispatch that routed the value here, an earlier check in the same flow, or a validator of the value's type.
---

# Trust established invariants

Code does not re-check a condition that other code already guarantees at that point.

A guard is code that checks a condition and stops or diverts when it fails: an `assert`,
an `if` that raises or returns early, an `isinstance` check, a `cast`, a `match` case or
`else` branch that raises. A guarantee is code that makes the condition true before the
guard runs, so the guard can never fail. The guarantee is in the file under review or a
file of the program it imports; read that file when the guarantee comes from there.

## The test

For each guard, ask: does code the reader can see make this condition true every time
the guard runs?

Guarantees that make the answer yes:

- an earlier check in the same function or flow that already stopped on the failing
  value (`if not lines: return` above `if len(lines) == 0: raise`), or an enclosing
  branch that already narrowed it;
- a dispatch that routes only matching values to this code: a registry keyed by the
  value's tag (`HANDLERS[request.kind].handle(request)`), a `match` or `if` chain that
  calls this function only in the branch for that variant;
- the value's type rejecting the failing value when it is built: a pydantic
  `field_validator` or `Field(gt=0)`, a dataclass `__post_init__` that raises, an attrs
  validator, a Django model field with `null=False`, a SQLAlchemy column with
  `nullable=False`;
- a collaborator whose code always returns the guaranteed form (a function that never
  returns an empty list, a lookup that raises instead of returning `None`).

The answer is no when nothing visible guarantees the condition: data from outside the
program, a parameter the callers can pass in either form, an optional field, the result
of `dict.get`, a lookup that may miss. Checking that is validation, not a re-check. A
condition that only the parameter's declared type guarantees is the type checker's
job (basedpyright's `reportUnnecessaryIsInstance` and `reportUnnecessaryComparison`),
so this rule is about guarantees made by code, not by annotations.

## Violation

A guard whose condition visible code already guarantees where the guard runs: an
`isinstance` check of a payload in a handler only a registry keyed by that payload's
kind calls, an `assert x is not None` below an `if x is None: raise`, an
`if amount <= 0: raise` on a model field whose validator already rejects non-positive
amounts.
