---
name: no-anonymous-tuples
description: A function does not return a tuple or a fixed-key dict whose elements answer different questions
---

# No anonymous tuples for separate answers

A function that returns several answers about its input returns them under names, not
by position or by string key.

## Definitions

- An **answer** is one fact the function works out: a rejection reason, whether the
  order is on hold, a shipping fee, the next run time.
- An **anonymous result** is a tuple (`return reason, held`, `-> tuple[str | None,
  bool]`) or a dict with a fixed set of string keys written in the function
  (`return {"reason": reason, "held": held}`, `-> dict[str, object]`), read by callers by
  position or by key.
- A **named result** is a class whose fields name the parts: a dataclass, `NamedTuple`,
  `TypedDict`, attrs class, pydantic model or enum.

## The test

For each return of an anonymous result in the file under review, ask: do its elements
answer different questions about the input, so each needs its own name to be read?

Yes: violation. No: not a violation.

The test reads these forms the same way:

- elements that answer different questions: a reason and a flag, a fee and a delivery
  date, a parsed value and a list of warnings, a record and whether it was created
  (`return user, created`). Violation.
- elements that are one kind of thing in a collection: `tuple[Order, ...]`, a dict keyed
  by data (`{order.id: order for ...}`, `dict[str, Carrier]`). Not a violation: they
  answer one question each, the same one.
- a pair whose positions are fixed by the language or a library protocol it implements:
  `divmod`-style `(quotient, remainder)` from `__divmod__`, `(key, value)` items yielded
  for `dict(...)`, a `__reduce__` tuple, `(status, headers, body)` for a WSGI or ASGI
  callable. Not a violation.
- a dict built as data for something outside the program, in the shape that thing
  defines: an HTTP request body or headers, a JSON payload a third-party API documents,
  a Django template context, `**kwargs` for a library call. Not a violation.
- a `NamedTuple`, `TypedDict`, dataclass or model returned instead: named. Not a
  violation.

## Violation

A function in the file under review that returns a tuple or fixed-key dict whose
elements answer different questions: `evaluate_order` returning
`(rejection_reason, is_on_hold)`; `quote` returning `{"fee_cents": fee,
"delivers_on": date}`.
