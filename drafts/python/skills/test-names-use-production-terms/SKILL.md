---
name: test-names-use-production-terms
description: A test's name calls each concept of the code under test by the term that code uses
---

# Test names use the production code's terms

A test's name calls each concept of the code under test by the name that code gives it.

The code under test's terms are the names it gives its concepts: its classes,
functions, methods, fields, enum members, exceptions and constants, and the words they
are made of (`resolve_dependencies` names "resolve", `EmptyResult` names "empty
result", `OrderStatus.CANCELLED` names "cancelled"). The judge reads the modules the
test imports to find them.

## The test

For each word or phrase in a test name that refers to an action, state, condition or
thing of the code under test, ask: does the code under test have its own name for that
concept, and does the test name use a different word for it?

Not a violation:

- the code's own term: `test_resolve_dependencies_orders_by_rank` for
  `resolve_dependencies`, `test_empty_result_when_no_rows` for `EmptyResult`;
- words for things the code under test doesn't name: scenario wording such as
  `_with_two_items` or `_for_a_weekend_order`;
- testing words: `returns`, `raises`, `rejects`, `when`, `without`.

A violation:

- `test_inject_dependencies_orders_by_rank` where the function is
  `resolve_dependencies`;
- `test_assemble_report_...` where the function is `build_report`;
- `test_no_reaction_when_no_rows` where the code returns `EmptyResult`;
- `test_voided_order_...` where the status is `OrderStatus.CANCELLED`.

## Violation

A test name in the file under review that calls a concept of the code under test by a
word other than the one that code uses for it.
