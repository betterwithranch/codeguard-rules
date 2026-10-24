---
name: assert-whole-objects
description: A test compares a value that compares by value as a whole with ==, never one of its parts (a field, an item, a key, a slice, or one member's presence) on its own.
---

# Assert whole values

A test compares a value whose type compares by value as one whole, so every field and
item is checked, including ones added later.

A part of a value is a field (`invoice.number`), an item by index or key (`parcels[0]`,
`payload["total"]`), a slice (`parcels[:2]`), or one item's presence in a collection
(`line in invoice.lines`). A part read through other parts is still a part of each value
it passes through: `invoice.lines[0].sku` is a part of `invoice`, of `invoice.lines` and
of `invoice.lines[0]`.

## The test

For each assert, including `self.assert...` methods, that compares, tests the truth of,
or checks membership of a part, ask: does a value the part is read from compare by value
with `==`? If yes, it is a violation. If no value it passes through compares by value,
it is not.

Compares by value:

- a dataclass (unless `eq=False`), an attrs class (`@define`, `@attr.s`), a pydantic
  model, a `NamedTuple`, a `TypedDict`;
- a class that defines `__eq__` over its fields;
- a list, tuple, dict or set, whatever it holds, and a string.

Doesn't compare by value:

- a plain class without `__eq__`, or a dataclass with `eq=False`;
- a Django model instance or SQLAlchemy ORM row (`==` compares the primary key or
  identity), a mock or a test double without `__eq__`;
- an exception, a `pytest.raises` result, a framework response (`response.status_code`),
  a file handle.

Fields the code generates, such as an id or a timestamp, don't change the answer: the
expected value can take them from the result (`Order(id=order.id, ...)`) or from a
frozen clock.

The answer is the same however many fields the test checks: separate asserts that
cover every field of a value that compares by value are each a violation.

Not a violation:

- `assert result == Invoice(number="42", total=120)`, `assert parcels == [Parcel(sku="A1")]`;
- an attribute read inside the expected value (`Invoice(number=order.number)`);
- a part of a value that doesn't compare by value (`assert response.status_code == 200`,
  `assert fake_mailer.sent == [expected_email]` where the fake has no `__eq__`);
- a scalar result compared whole (`assert total_cents(order) == 120`).

## Violation

An assert in the file under review on a part of a value that compares by value:
`assert invoice.number == "42"`, `assert parcels[0].sku == "A1"`,
`assert payload["total"] == 120`, `assert order.paid`, `assert line in invoice.lines`,
`self.assertEqual(invoice.total, 120)`.
