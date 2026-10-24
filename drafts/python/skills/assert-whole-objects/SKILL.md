---
name: assert-whole-objects
description: Assert whole result objects
---

# Assert whole result objects

A test that checks several parts of a value it produced compares the whole value once
instead.

The test for each produced value: do the test's assertions check several of its parts,
check all of it with some fields left out, or check only how many items it has, when
one comparison of the whole value could replace them? If yes, it is a violation. The
produced value is what the call under test returned or changed, read from the test's
code. Which side of a comparison it is on doesn't matter.

- Parts are its fields, items and keys, members of a set it is or holds, and values
  computed from it, such as a filtered subset of its items or an outcome derived from
  it.
- One comparison of the whole value could replace them when its type has `__eq__`: a
  dict, list, set or tuple, a dataclass or attrs class (unless declared with
  `eq=False`), a NamedTuple, a pydantic model. A field that changes each run (a
  generated id, a timestamp, a duration) doesn't prevent it: the test controls its
  source.
- Fields that together are one property the test is about, such as a node's start and
  end line as its span, are one part.

Checks parts instead of the whole value (violations):

- Several fields, each in its own assertion: `assert invoice.number == "42"` followed by
  `assert invoice.total == 120`, even when they cover every field today.
- Several fields at once: `assert (invoice.number, invoice.total) == expected_pair`,
  `assert [(p.sku, p.qty) for p in parcels] == [("A1", 1), ("B2", 2)]`.
- Several members or computed values: `assert Kind.BODY in kinds` with `assert
  Kind.HEADER not in kinds`; `assert [d for d in review.diagnostics if d.is_error] ==
  []` with `assert outcome(review) is Outcome.VALID`; a response's keys and then a
  prefix of one of its values.
- Several fields of a value whose other fields change each run: `assert
  (attrs["cache_hit"], attrs["changed_files"]) == (False, ["a.py"])` on span
  attributes that also hold durations.
- All of it but some fields, dropped or replaced before the comparison, on a copy or in
  place: `dataclasses.replace(order, id=None)`, `order.model_copy(update={"id": None})`,
  `order.model_dump(exclude={"id"})`, `del` or `pop` of a key, a dict comprehension that
  filters keys out, `order.id = None`, or `Order(id=ANY, ...)` as the expected value.
- How many items it, or each of its items, has instead of what they are: `assert
  len(parcels) == expected_count`, `assert expected_count == len(parcels)`, `assert
  parcels`.

Not violations:

- One part, when that is what the test checks: `assert invoice.number == "42"`, `assert
  parcels[0].sku == "A1"`, `assert [p.sku for p in parcels] == ["A1", "B2"]`.
- One property that spans fields: `assert [(n.start_line, n.end_line) for n in scopes]
  == [(1, 3), (2, 3)]` in a test of the nodes' spans.
- The produced value compared once with an expected value, however the expected value
  is built: a constructor, a literal, `baseline.model_copy(update={"total": 2})`,
  `replace(baseline, total=2)`, `len(lines)` as the expected value of a produced count,
  or a tuple of another object's fields (`(expected.share, expected.remainder)`) as the
  expected value of a produced tuple.
- A produced scalar or bool asserted directly.
- The fields the test is about, when the value's type has no `__eq__`: a
  `subprocess.CompletedProcess`'s `returncode` and `stdout`, a plain class's fields. One
  `==` on such a value compares identity and checks nothing.
- Identity checks: `assert cached.store is judges.store`. An `==` on the whole value
  can't state that two references are the same object.
