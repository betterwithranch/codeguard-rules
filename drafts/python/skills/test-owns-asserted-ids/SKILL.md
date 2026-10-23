---
name: test-owns-asserted-ids
description: An identity value a test asserts on is written in that test or read from a record it built, never from a shared constant
---

# A test owns the ids it asserts on

The identity values a test checks are visible in that test.

An identity value is a value that names one record or object: an id, a key, a number
such as an order or invoice number, a slug, a code, an email used to find a user. A
shared constant is a name the test reads but doesn't own: a module-level `UPPER_CASE`
name, a class-level constant read through `self` or the class, or a name imported from
another module (`tests.constants`, `conftest`).

## The test

For each identity value an assertion compares, ask: where does the test get it?

Owned by the test, so not a violation:

- a literal in the test: `assert shipment.order_id == "ord-42"`;
- read from a record or object the test, or a fixture it requests, built:
  `assert shipment.order_id == order.id`;
- a local the test assigns: `order_id = "ord-42"` in the test body.

From a shared constant:

- `ORDER_ID = "ord-42"` at module level, then `assert shipment.order_id == ORDER_ID`;
- `ACCOUNT_ID = UUID("8f14e45f-ceea-4672-9c3d-1b2a5f7e6d10")` used inside an expected
  object: `assert invoice == Invoice(account_id=ACCOUNT_ID, ...)`;
- `self.ORDER_ID` from a test class, or `from tests.constants import ORDER_ID`, in an
  assertion or a unittest `assert*` call.

A constant that isn't an identity value (`MAX_RETRIES`, `TIMEOUT_SECONDS`) is outside
this rule.

## Violation

An assertion that compares an identity value read from a shared constant.
