---
name: law-of-demeter
description: A function doesn't reach through one object into another's parts; code that follows a chain from an object it has, through an object that object holds, to call a method on, read a part of or assign a part of a third, is a violation.
---

# Law of Demeter

A function doesn't reach through one object into another's parts.

A function's direct collaborators are its own object and its fields, its parameters,
objects it creates, and objects a call it makes returns. Reaching through is following
a chain past a direct collaborator into the objects it holds: `order.customer.account`
reads the customer that the order holds, and then the account the customer holds,
and calls a method on or reads a part of that third object.

Count only objects of types with behavior and parts of their own: the program's
classes, models and services. Plain data does not count as a step.

## Violation

Code the change adds or edits that reaches from a direct collaborator through at least
one object it holds, to call a method on, read a field of, or assign a field of a
further object of the program's types.

Report it on the line with the chain.

## Not a violation

- A call on a direct collaborator, or reading one of its fields: `order.total()`,
  `order.customer`.
- Reading into a value object's own data: `invoice.total.amount`, `period.start.year`,
  `address.postcode`, where the value is plain data that describes one thing.
- A fluent or pipeline API, whose each call returns a new value of the same family: a
  query builder, a dataframe, a collection pipeline, a string builder, a promise chain.
- A framework's request, settings, or application object: `request.user.email`,
  `settings.DATABASES["default"]`.
- Module paths and enums: `os.path.join`, `datetime.date.today()`, `Status.PAID.value`.

## Why

The function depends on how every object along the chain is built, so changing any one
of them breaks it. Asking the direct collaborator for what is needed keeps each object's
structure its own, and lets a reader see what the function depends on from its
collaborators alone.

Source: Karl Lieberherr and Ian Holland, "Assuring Good Style for Object-Oriented
Programs" (1989), the Law of Demeter; Martin Fowler, *Refactoring* (1999), Message
Chains.
