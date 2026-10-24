---
name: test-has-signal
description: Every test can fail for a plausible bug in the project's own code that no other test in its file would also catch
---

# Every test has signal

Every test can fail for a plausible bug in the project's own code that no other test in
its file would also catch.

The project's own code is what the project wrote: its functions, methods, validators,
custom serializers, computations and branches, and the constraints it declares because
the domain requires them. A plausible bug is a change a developer could make by
mistake in that code: a wrong branch, a wrong calculation, a missing check, a
constraint set to the wrong bound. Editing a literal the test copied (a label's text,
a config value) is not a bug the test can catch; it only makes the copy differ.
A bug in Python, the standard library, or a library (pydantic, Django, attrs, an
enum) is not the project's.

## The test

For each test, ask: can you name a plausible bug in the project's own code that makes
this test fail while every other test in the same file still passes?

No such bug, so the test has no signal:

- tautology: the expected value is a copy of a declaration in the code under test, so
  only editing that declaration breaks it: `assert Settings.model_config ==
  {"extra": "forbid", "frozen": True}`, `assert OrderStatus.SHIPPED.value ==
  "shipped"`, `assert FrequencyField.label == "Frequency"`;
- framework behavior: the test checks what Python or a library guarantees, with no
  decision of the project's in the path: a field without a validator accepts a value of
  its type, a field defaults to its declared default, a dataclass or a model without
  custom serializers round-trips through `asdict` or `model_dump`, `OrderStatus(value)`
  accepts each member's value;
- redundancy within the file: every bug that fails this test also fails another test
  in the file: `assert isinstance(build_order(...), Order)` beside a test that compares
  `build_order(...)` to a whole expected `Order`; `assert result is not None` beside a
  test asserting `result == expected`.

Has signal, so not a violation:

- a test that a domain constraint holds: a percentage field declared `Field(ge=0,
  le=100)` rejects 150; a quantity must be positive;
- a test of a validator, computed field, custom serializer or branch the project wrote;
- two tests of the same function with inputs that take different branches.

## Violation

A test in the file under review that no plausible bug in the project's own code would
fail, or that fails for no bug another test in the same file doesn't also fail for.
