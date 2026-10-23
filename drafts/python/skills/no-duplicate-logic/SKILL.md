---
name: no-duplicate-logic
description: A function body does not repeat the steps of another function in the same file or in a module the file imports
---

# No duplicate logic

One computation is written once, so a fix or a change to it lands everywhere it runs.

## Definitions

- A **function** is a module function, method, `@staticmethod`, `@classmethod`,
  `@property`, nested function or `async def`.
- Two functions are **copies** when their bodies do the same steps in the same order on
  corresponding inputs, and differ only in names (of the function, its parameters and
  its locals), in the order of their parameters, or in formatting. A body that contains
  another's steps plus steps of its own is a copy of that part when the shared part is
  at least two statements, or one expression with at least two operations
  (`max(round((subtotal - discount) * (1 + rate)), 0)`).
- The **other side** of a copy is a function in the file under review, or in a module it
  imports (`from shipments.fees import domestic_fee`, `import invoices.totals`). Read
  each imported module of the project to compare its functions.

## The test

For each function the change adds or edits, ask: is there another function, in this file
or in a module this file imports, whose body it copies?

No: not a violation. Yes: violation.

Not copies, whatever their size:

- a function that calls the other one (`return domestic_fee(total, weight) + SURCHARGE`);
- bodies that differ in a step: a different operator, condition, constant or call
  (`>= FREE_SHIPPING_THRESHOLD` against `> 0`, `round` against `int`);
- bodies that share only one statement or one simple expression (`return self.total`,
  `if not items: return []`, `return Order(**fields)`);
- structure a framework or library asks every implementation to repeat: two DRF
  serializers' `Meta` classes, two Django models' `__str__` returning a field, two
  pydantic validators that each strip their own field, two classes' `__eq__`
  methods comparing their own fields;
- overloads and `Protocol`/ABC method stubs (`...`, `pass`, `raise NotImplementedError`).

## Violation

A function added or edited in the file under review whose body is a copy of another
function's body in that file or in a module it imports, whether the copy keeps the
parameter order (`credit_note_total(subtotal, tax_rate, discount)` with
`invoice_total`'s body) or reorders it (`return_fee(weight_grams, order_total)` with
`domestic_fee(order_total, weight_grams)`'s body).
