---
name: result-parts-named
description: A function's result names what each of its parts means; a function that returns parts answering different questions in a tuple, or in a map whose keys nothing checks, is a violation.
---

# Result Parts Named

A function's result names what each of its parts means.

A result has parts when the function returns more than one value together. The parts
answer different questions when each means something different about the input: a fee
and a delivery date, a parsed value and its warnings, a record and whether it was
created, a flag and a reason.

A part is named when the result's type gives it a name that the type checker or the
language checks: a field of a record, a named tuple, a typed dictionary or an object
type. A part is anonymous when a caller finds it by position, as in a tuple or array, or
by a key nothing checks, as in a plain dictionary built from string keys.

## Violation

A return the change adds or edits whose result holds parts that answer different
questions, anonymously: by position, or by unchecked keys written in the function.

Report it on the return.

## Not a violation

- Parts that are one kind of thing in a collection: a list of orders, a map from id to
  order.
- A pair whose meaning is its type's own, such as a point's coordinates.
- A pair whose positions a language or library protocol fixes, such as a key and value
  for building a map, or the pair a framework's hook must return.
- A result in a shape something outside the program defines: an HTTP body, a template
  context, a documented payload.
- A result of a record, named tuple, typed dictionary or object type that names its
  parts.

## Why

Nothing checks what a position or an unchecked key means. A caller that reads the parts
in the wrong order, or misspells a key, still runs, and passes the wrong value on; a
reader has to open the function to learn which part is which. A named part is checked
everywhere it is read.

Source: prefer named tuples and records to bare tuples for results with several parts
(Brett Slatkin, *Effective Python*, 2nd ed., 2019, items 19 and 37).
