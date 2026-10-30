---
name: pass-values-not-context-objects
description: A function takes the values it reads, not a context or settings object it mostly ignores; a function the change adds, or whose parameters it changes, that takes a context, settings, configuration, request or application-state object only to read half of its fields or fewer is a violation.
---

# Pass Values, Not Context Objects

A function takes the values it reads, not a context or settings object it mostly ignores.

A context or settings object is an object whose job is to carry many unrelated values to
many parts of the program: a context, settings or configuration, a web request, an
environment or application-state object. Its fields are inputs for different consumers,
not facts about one thing. A domain value is not one: an order, an invoice, a date
range, an amount or a record, whose fields all describe one thing.

Count the object's fields where its type is declared: in the file under review, or in a
file of the program that file imports. A framework's request and settings types are
context or settings objects with many fields.

## Violation

A function or method the change adds, or whose parameters the change edits, that takes
a context or settings object as a parameter when:

- every use of the parameter reads one of its fields; and
- it reads half of the object's fields or fewer, exactly half included.

Report it on the parameter.

## Not a violation

- A domain value parameter, however few of its fields the function reads.
- A context or settings object the function uses as a whole: it passes the object on to
  another call, calls one of its methods, returns it or stores it.
- Several plain values taken as separate parameters, however many.
- A parameter the framework passes and whose signature it sets: a view's or route
  handler's request, a middleware's request, a component's props.
- A function that reads more than half of the object's fields.
- An edit to a function's body that leaves its parameters as they were.
- Reaching through a value the function does use to another object's fields. That is
  `law-of-demeter`'s.

## Why

A function that takes the whole object claims to need all of it. Its tests must build
the whole object to call it, its callers must have one to hand, and a reader can't tell
from the signature which of its values decide the result. Taking the values it reads
says exactly what it depends on.

Source: Larry Constantine and Edward Yourdon, *Structured Design* (1979), stamp
coupling; Robert C. Martin, the Interface Segregation Principle, applied to a function's
parameters.
