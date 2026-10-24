---
name: tests-earn-their-place
description: Every test can fail for a plausible bug in the project's own code no other test in its file catches, an integration test crosses a seam between components, and a test's name claims only what its assertions check, in the code under test's own terms.
---

# Every test earns its place and says what it proves

Every test can catch a bug no sibling test catches, and its name states what it checks
in the words of the code it checks.

The project's own code is what the project wrote: its functions, methods, validators,
custom serializers, computations and branches, and the constraints it declares because
the domain requires them. A plausible bug is a change a developer could make by
mistake in that code: a wrong branch, a wrong calculation, a missing check, a
constraint set to the wrong bound, a key, route or registration two components don't
share. Editing a literal the test copied (a label's text, a config value) is not a bug
the test can catch; it only makes the copy differ. A bug in Python, the standard
library, or a library (pydantic, Django, attrs, an enum) is not the project's.

The code under test is what the test calls or reads; the judge reads the modules the
test imports to find it.

## The test

For each test, ask: would a plausible bug in the project's own code fail it while
every other test in its file passes, and does its name claim only what it checks, in
the code under test's terms? The forms below say what each part asks.

### Tests with no signal

Ask: can you name a plausible bug in the project's own code that makes this test fail
while every other test in the same file still passes?

Violation: a test with no such bug:

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

The violation is the test. For redundancy, it is the test whose bugs the other already
catches.

Not a violation:

- a test that a domain constraint holds: a percentage field declared `Field(ge=0,
  le=100)` rejects 150; a quantity must be positive;
- a test of a validator, computed field, custom serializer or branch the project wrote;
- two tests of the same function with inputs that take different branches.

### Integration tests that cross no seam

This form applies only to a test in an integration or end-to-end file: a file under an
`integration` or `e2e` directory, or whose name contains `integration` or `e2e`
(`test_payments_integration.py`, `test_orders_e2e.py`). Such a test exists to catch
bugs at a seam, which a unit test can't.

A component is a part of the program with its own job that a unit test could cover
alone: a view or route handler, a serializer, a service, a repository, a model and its
table, a queue producer or consumer, a pipeline step, a registry, the app's settings.

A seam is where one component hands data or control to another: a URL route to its
view, a view to its serializer, a service to the repository that stores what it built,
a producer to the consumer reading the same queue, a registration to the lookup that
finds it, one pipeline step to the next, a setting to the code that reads it. A
disagreement at a seam is a key, route, name, registration, setting or step order the
two sides don't share.

Ask: does the test observe a result that depends on one component receiving what
another passed, so a disagreement at that seam would fail it?

Violation: a test in an integration or end-to-end file whose result depends on one
component of the program alone:

- calling a pure function and asserting its return (`parse_amount("1,000.50")`);
- validating data with one serializer or pydantic model and asserting its errors;
- calling one model method or one class's method on objects the test built, with no
  other component of the program in the path.

The violation is the test.

Not a violation:

- `client.post("/orders/", data)` through the app's test client, then reading the
  stored `Order`;
- publishing an event to the app's queue and asserting the consumer's side effect;
- running a pipeline's steps end to end and comparing the final output;
- a service that saves through a real repository, then reading the row back from the
  database;
- a test of one component in a file that is not an integration or end-to-end file.

### Names that claim what isn't checked

A test name's claim is what the name says the code does: an outcome
(`test_refund_restores_stock` claims stock is restored), a value
(`test_total_includes_tax`), an error (`test_rejects_negative_quantity`), or a
mechanism (`test_reads_rates_from_cache` claims the cache is read). Words that only
set the scene (`_for_guest_checkout`, `_when_cart_is_empty`) describe the input, not a
claim.

An assertion checks a claim when the test asserts the claimed outcome: an `assert`, a
`pytest.raises`, a `self.assert...` call, or a helper the test calls that asserts it.

Ask: for each claim in the test's name, does an assertion in the test check it?

Violation: a test whose name claims an outcome, value, error or mechanism that none of
its assertions check:

- `test_refund_restores_stock` asserting only `refund.status == "refunded"`;
- `test_sends_confirmation_email` with no assertion on any email;
- `test_reads_rates_from_cache` asserting only the converted amount;
- `test_rejects_negative_quantity` asserting `line.quantity == 0`.

The violation is the test's name.

Not a violation:

- `test_cancel_sets_cancelled_status` asserting `order.status == OrderStatus.CANCELLED`;
- a name claiming one outcome, with assertions on that outcome and others;
- `test_rejects_negative_quantity` using `with pytest.raises(InvalidQuantity):`.

### Names in words the code under test doesn't use

The code under test's terms are the names it gives its concepts: its classes,
functions, methods, fields, enum members, exceptions and constants, and the words they
are made of (`resolve_dependencies` names "resolve", `EmptyResult` names "empty
result", `OrderStatus.CANCELLED` names "cancelled").

Ask: for each word or phrase in the test's name that refers to an action, state,
condition or thing of the code under test, does that code have its own name for the
concept, and does the test name use a different word for it?

Violation: a test name that calls a concept of the code under test by a word other
than the one that code uses for it:

- `test_inject_dependencies_orders_by_rank` where the function is
  `resolve_dependencies`;
- `test_assemble_report_...` where the function is `build_report`;
- `test_no_reaction_when_no_rows` where the code returns `EmptyResult`;
- `test_voided_order_...` where the status is `OrderStatus.CANCELLED`.

The violation is the test's name.

Not a violation:

- the code's own term: `test_resolve_dependencies_orders_by_rank` for
  `resolve_dependencies`, `test_empty_result_when_no_rows` for `EmptyResult`;
- words for things the code under test doesn't name: scenario wording such as
  `_with_two_items` or `_for_a_weekend_order`;
- testing words: `returns`, `raises`, `rejects`, `when`, `without`.

## Violation

A test in the file under review that doesn't earn its place or say what it proves: no
plausible bug in the project's own code would fail it, or only bugs another test in
the file also catches; in an integration or end-to-end file, its result depends on one
component alone; its name claims an outcome, value, error or mechanism no assertion
checks; or its name calls a concept of the code under test by a word that code doesn't
use for it.
