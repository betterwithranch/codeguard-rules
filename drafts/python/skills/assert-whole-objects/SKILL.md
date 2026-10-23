---
name: assert-whole-objects
description: Assert whole result objects
---

# Assert whole result objects

A test that checks more than one part of a value it produced compares the whole value
once, rather than checking its parts separately.

The test for each produced value: do the test's assertions check several of its fields,
or all of it with some fields left out, instead of comparing it whole? If yes, it is a
violation. The produced value is what the call under test returned or changed, read
from the test's code. Which side of a comparison it is on doesn't matter.

Checks parts instead of the whole value (violations):

- Several of its fields, each in its own assertion: `assert invoice.number == "42"`
  followed by `assert invoice.total == 120`, even when they cover every field today.
- Several fields at once: `assert (invoice.number, invoice.total) == expected_pair`,
  `assert [(p.sku, p.qty) for p in parcels] == [("A1", 1), ("B2", 2)]`.
- All of it but some fields, dropped or replaced before the comparison, on a copy or in
  place: `dataclasses.replace(order, id=None)`, `order.model_copy(update={"id": None})`,
  `order.model_dump(exclude={"id"})`, `del` or `pop` of a key, a dict comprehension that
  filters keys out, `order.id = None`, or `Order(id=ANY, ...)` as the expected value. A
  field that changes each run (a generated id, a timestamp) is still part of the value.
- A collection's size instead of its contents: `assert len(parcels) ==
  expected_count`, `assert expected_count == len(parcels)`, `assert parcels`.

Not violations:

- One field or item, when that is what the test checks: `assert invoice.number ==
  "42"`, `assert parcels[0].sku == "A1"`, `assert [p.sku for p in parcels] == ["A1",
  "B2"]`.
- The produced value compared once with an expected value, however the expected value
  is built: a constructor, a literal, `baseline.model_copy(update={"total": 2})`,
  `replace(baseline, total=2)`, `len(lines)` as the expected value of a produced count,
  or a tuple of another object's fields (`(expected.share, expected.remainder)`) as the
  expected value of a produced tuple.
- A produced scalar or bool asserted directly.
- Every field asserted, one per line, when the produced value's type has no `__eq__`:
  a plain class compares by identity, so one `==` would check nothing. A dataclass or
  attrs class (unless declared with `eq=False`), a NamedTuple and a pydantic model have
  `__eq__`.
