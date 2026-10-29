---
name: composition-over-inheritance
description: A class inherits only from a type it is a kind of; a class that inherits from another to reuse its code, when it isn't a kind of that type, is a violation.
---

# Composition Over Inheritance

A class inherits only from a type it is a kind of.

A class is a kind of its base when every statement true of the base is true of it, and
a caller that wants the base would take it: a savings account is a kind of account, a
declined payment is a kind of error. A class that inherits only to call the base's
methods on itself, to get its storage, retries, logging or sending, is not a kind of it:
an invoice notifier is not a kind of email client, a checkout controller is not a kind
of retry helper.

## Violation

A class the change adds, or whose bases the change edits, that inherits from a class
the program defines when it is not a kind of that class: it uses the base's methods as
tools for its own different job, and no caller would pass it where the base is
expected.

Report it on the class's declaration line.

## Not a violation

- A class that is a kind of its base: it does the base's job its own way, or adds to it.
- A class that implements an interface, protocol or abstract base it is a kind of.
- A framework or standard base class the framework requires: a database model, a view,
  a schema or settings model, a test case, an exception or error.
- A mixin: a small class written to be combined into others, named as one or documented
  as one.
- A class that holds the other type in a field and calls it: that is composition.
- A class with no base, or whose bases the change leaves as they were.
- An override that stubs or refuses an inherited method: a separate rule judges it.

## Why

A subclass gets every method of its base, and every change to the base. When it inherits
only to reuse code, callers can call the base's methods on it that make no sense for its
job, and a change to the base made for the base's own callers breaks it. Holding the
other object in a field gives it only the calls it makes, behind a type it chose.

Source: favour object composition over class inheritance (Gamma, Helm, Johnson and
Vlissides, *Design Patterns*, 1994); Replace Superclass with Delegate (Martin Fowler,
*Refactoring*, 2nd ed., 2018).
