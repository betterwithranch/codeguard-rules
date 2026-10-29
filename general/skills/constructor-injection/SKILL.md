---
name: constructor-injection
description: A method's collaborators come through its object's constructor; a method of a class that takes a collaborator as a parameter on each call is a violation.
---

# Constructor Injection

A method's collaborators come through its object's constructor.

A collaborator is an object a method calls to get its work done: a client, a repository,
a rate or price provider, a strategy, a formatter or renderer, a registry, a clock, a
mailer, a cache. Its kind decides it, from its type or, when it has none, from its name
and what the method does with it.

Data is what one call is about: the records, ids, amounts and dates it works on, a
request or event, a query, a callback the caller supplies for this one call. Data stays
a parameter even when the method calls its methods.

## Violation

A method of a class, which the change adds or whose parameters it edits, that takes a
collaborator as a parameter: a public or private method, a static or async method, in a
plain class, a record, a model or a view.

Report it on the parameter.

## Not a violation

- The constructor, a field the class declares, or a factory method that builds the
  instance and stores the collaborator on it.
- A function outside any class, which has no constructor to take it.
- A parameter that is data, even when the method calls its methods, such as an order
  whose total the method reads.
- A method whose signature an interface, base class or framework declares with that
  parameter, such as a handler the framework calls with its event and a bus.

## Why

A collaborator passed on each call has to be found by every caller, and each caller can
pass a different one, so the object's behaviour depends on who called it. Taken once in
the constructor, it is wired in one place, the signature of each method shows only what
the call is about, and a test swaps it by building the object differently.

Source: dependency injection (Martin Fowler, "Inversion of Control Containers and the
Dependency Injection pattern", 2004; Mark Seemann, *Dependency Injection in .NET*,
2011), which prefers constructor injection.
