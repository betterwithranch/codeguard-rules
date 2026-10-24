---
name: no-acting-fixtures
description: A test's act, the call whose result or effect it asserts, runs in the test body and never in a fixture
---

# No acting fixtures

The call a test checks runs in that test, so the test shows what it does as well as
what it expects.

The act is the call into the code under test whose result or effect a test's
assertions check: the function or method whose return value the test compares, or
whose change to state (a ledger entry, a sent message, a saved row, a status) the test
asserts.

## The test

For each test, find what its assertions check and the call that produced it. Ask: does
that call run in the test body (directly or through a helper the body calls), or in a
fixture the test requests?

In the test body, so not a violation:

- the test calls the code under test and asserts on the result:
  `receipt = checkout(cart)` then `assert receipt.total == 120`;
- fixtures provide the inputs, collaborators and environment the act uses, and the
  test asserts on what its own act did to them.

In a fixture:

- a fixture returns the result of calling the code under test, and the test only
  asserts on it: `@pytest.fixture def receipt(cart): return checkout(cart)`, a fixture
  that returns `client.post("/checkout/")`'s response, or one that returns
  `InvoiceMapper(rules).map(raw)`;
- a fixture calls the code under test for its effect (`service.pay("inv-42")`,
  `notifier.send_reminders()`, `call_command("close_month")`), and the test asserts on
  that effect without making the call itself.

## Violation

A fixture that makes the call a test's assertions check, so the test that requests it
has no act of its own.
