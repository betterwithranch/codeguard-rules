---
name: composition-over-inheritance
description: A class inherits only from a type it is a kind of, one whose job it does as a variety of it; a class that inherits from another to reuse its code for a different job is a violation.
---

# Composition Over Inheritance

A class inherits only from a type it is a kind of.

A class is a kind of its base when it does the base's job, as one variety of it: a
savings account holds money as every account does, and earns interest its own way; a
declined payment is an error, as every error is. A class whose own job is a different
one is not a kind of its base, even when it calls the base's methods on itself to get
its storage, retries, logging or sending: an invoice notifier's job is telling customers
about invoices, not sending email, so it is not a kind of email client, and a checkout
controller is not a kind of retry helper.

## Violation

A class the change adds, or whose bases the change edits, that inherits from a class it
is not a kind of, whether the program or a library defines that class: the class has a
different job from its base, and uses what it inherits as tools for that job.

Report it on the class's declaration line.

## Not a violation

- A class that is a kind of its base: it does the base's job its own way, or adds to it.
- A class that implements an interface, protocol or abstract base whose job it does.
- A framework or standard base class the framework requires: a database model, a view,
  a schema or settings model, a test case, an exception or error.
- A mixin: a small class written to be combined into others, named as one or documented
  as one.
- A class that holds the other type in a field and calls it: that is composition.
- A class with no base, or whose bases the change leaves as they were.

## Why

A subclass gets every method of its base, and every change to the base. When it inherits
only to reuse code, callers can call the base's methods on it that make no sense for its
job, and a change to the base made for the base's own callers breaks it. Holding the
other object in a field gives it only the calls it makes, behind a type it chose.

Source: favour object composition over class inheritance (Gamma, Helm, Johnson and
Vlissides, *Design Patterns*, 1994); Replace Superclass with Delegate (Martin Fowler,
*Refactoring*, 2nd ed., 2018).
