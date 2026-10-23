---
name: no-repeated-type-switches
description: Two or more functions or methods in one file that each choose their behavior by a value's type, over the same set of types, are a violation.
---

# No repeated type switches

The choice of behavior by a value's type is made in one place, not repeated in several
functions.

A type switch is code that picks a branch by which of several types a value has: an
`if`/`elif` chain of `isinstance` or `issubclass` checks, `type(x) is` or `type(x) ==`
comparisons, a `match` statement with class patterns (`case CardPayment():`), or a
lookup keyed by `type(x)` (`handlers[type(event)]`). Its type set is the types it
chooses among. A switch on values, such as a `match` on strings or an `if` on
`payment.kind == "card"`, is not a type switch.

## The test

For each type switch in the file, ask: does another function or method in the same file
also switch on a value of the same kind, with at least two of the same types among its
choices?

Yes is a violation. No, because the file has one such switch, or the switches choose
among different types, is not.

Not type switches, so not counted:

- a single `isinstance` guard that rejects or narrows one type (`if not isinstance(raw,
  str): raise TypeError`), as in a pydantic `field_validator` or a `__eq__`;
- `functools.singledispatch` or `singledispatchmethod` registrations, and methods each
  type defines for itself;
- `except` clauses, which choose by exception type as part of error handling.

The switches can be in module functions, in methods of one class, in methods of
different classes, in Django or DRF views, or in a serializer's `to_representation`;
what counts is that the same file chooses among the same types more than once.

## Violation

Two or more functions or methods in the file under review that each switch on a value of
the same kind over at least two of the same types: `shipping_fee(payment)` and
`receipt_line(payment)` each branching on `isinstance(payment, CardPayment)` and
`isinstance(payment, BankTransfer)`.
