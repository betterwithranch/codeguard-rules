---
name: assert-whole-objects
description: Assert whole result objects
---

# Assert whole result objects

A test's assertions check the whole value the code under test produced, so they fail
whenever any part of it is wrong.

The test for each assertion: once it passes, could some part of the produced value
still be wrong? If yes, it is a violation. The produced value is what the call under
test returned or changed, read from the test's code. Which side of the comparison it
is on doesn't matter.

Leaves part of the produced value unchecked (violations):

- One field or item of it: `assert invoice.number == "42"`, `assert parcels[0].sku ==
  "A1"`. Separate `==` lines for each field of a type that has `__eq__` are a violation
  even when they cover every field today: they miss fields added later.
- Only its size: `assert len(parcels) == expected_count`, `assert expected_count ==
  len(parcels)`.
- A tuple of some of its fields: `assert (invoice.number, invoice.total) ==
  expected_pair`.
- A copy of it that drops or replaces fields, inline or in a variable compared later:
  `dataclasses.replace(order, id=None)`, `order.model_copy(update={"id": None})`,
  `order.model_dump(exclude={"id"})`, `del` or `pop` of a key, a comprehension that
  leaves fields out. A field that changes each run (a generated id, a timestamp) is
  still part of the value.

Checks the whole produced value (not violations):

- The produced value compared once with an expected value, however the expected value
  is built: a constructor, a literal, `baseline.model_copy(update={"total": 2})`,
  `replace(baseline, total=2)`, `len(lines)` as the expected value of a produced count,
  or a tuple of another object's fields (`(expected.share, expected.remainder)`) as the
  expected value of a produced tuple.
- A produced scalar compared directly.
- Every field asserted, one per line, when the produced value's type has no `__eq__`:
  a plain class compares by identity, so one `==` would check nothing. A dataclass, an
  attrs class, a NamedTuple and a pydantic model have `__eq__`.
