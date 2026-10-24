---
name: docstrings-add-information
description: A docstring tells the caller something the name, signature and body don't already say
---

# Docstrings add information

A docstring tells its reader something the code does not already say.

## Definitions

- A **docstring** is the string literal that opens a module, class, function or method
  body.
- **What the code says** is the name, the parameter names and types, the return type,
  the decorators, and what the body plainly does.
- **Information** is anything a caller needs that the code doesn't show: units or
  ranges the types don't carry, which exceptions are raised and when, side effects
  (writes a file, sends a request), behavior on edge inputs (empty list, `None`, a
  missing key), a reason or outside constraint (`The carrier API accepts at most 50
  parcels`), thread-safety, or the format of a string it takes or returns.

## The test

For each docstring the change adds or edits, ask: does it give the reader information,
beyond what the code says?

Yes: not a violation. No: violation.

The test reads these forms the same way:

- a docstring that rewords the name or signature (`"""Return the total."""` on
  `def total(self) -> int`, `"""Order model."""` on `class Order`, `Args: order: the
  order` sections that repeat parameter names): violation;
- a docstring that narrates the body step by step: violation;
- a docstring that describes what the code used to do or does not do: violation;
- a docstring that props up a vague name by saying what the body plainly does
  (`"""Sets the order to submitted and emails the customer."""` on `def handle`):
  violation;
- a docstring with at least one piece of information (a unit, a raised exception and
  when, an edge case, a side effect, an outside constraint) is not a violation, even
  when it also restates the name;
- module, class, `@property`, Django model, DRF view, pydantic model, Click or Typer
  command docstrings are read the same way; a CLI command's docstring that is its
  `--help` text gives the user information and is not a violation.

## Violation

A docstring added or edited in the file under review that gives no information beyond
what its code says: it rewords the name or signature, narrates the body, describes what
the code did before or doesn't do, or stands in for a name that doesn't say what the
code does.
