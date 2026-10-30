---
name: no-redundant-checks
description: A check doesn't re-test a condition earlier code already guarantees; a check whose condition an earlier check, an enclosing branch, a dispatch, the value's type or the function that produced it already makes true is a violation.
---

# No Redundant Checks

A check doesn't re-test a condition earlier code already guarantees.

A check is code that tests a condition and stops the path when it fails: an assertion,
or a branch or match case that raises, returns, or leaves or skips the rest of a loop.
Its condition can be any test, a comparison or a test of the value's type. Code that
tests a condition and carries on either way, such as a conditional expression that
picks one of two values, is not a check.

A condition is guaranteed where the check runs when visible code makes it true every
time the check runs:

- an earlier check on the same path already stopped on the failing value;
- an enclosing branch only runs when the condition holds;
- a dispatch routes only values that meet the condition to this code, such as a table
  of handlers keyed by the value's kind;
- the value's type rejects failing values when it is built: a validator, a field
  constraint, a schema refinement, a non-null column;
- the function that produced the value always returns it in the guaranteed form.

The guarantee is in the file under review or in a file of the program it imports; read
that file when it comes from there.

## Violation

A check the change adds or edits whose condition is guaranteed where it runs.

Report it on the first line of the check.

## Not a violation

- A check on what nothing guarantees yet: outside data before it is parsed, an
  optional value, a lookup that may miss, a parameter of a function whose callers may
  pass either.
- A check whose condition only a type annotation guarantees. That is the type
  checker's to report.
- A check that tests a stronger condition than the guarantee: the type guarantees a
  positive amount and the check tests it against a limit.

## Why

A re-check says the guarantee can't be trusted, and hides which code owns it. The
reader can't tell whether the earlier code is the real check or the later one is, and
when the rule changes, one of them is missed. Establishing the guarantee once and
trusting it after keeps one place to read and change.

Source: Alexis King, "Parse, don't validate" (2019).
