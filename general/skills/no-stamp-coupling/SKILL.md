---
name: no-stamp-coupling
description: A function takes the values it reads, not a bundle it mostly ignores; a parameter that is a context, settings, config, request or app-state object, of which the function only reads half the fields or fewer, is a violation.
---

# No Stamp Coupling

A function takes the values it reads, not a bundle it mostly ignores.

A bundle is an object whose job is to carry many unrelated values to many parts of the
program: a context, settings or configuration, a web request, an environment or
application-state object. Its fields are inputs for different consumers, not facts
about one thing. A domain value is not a bundle: an order, an invoice, a date range, an
amount, a record's fields, which all describe one thing.

Read the bundle's type where it is declared, in the file under review or a file of the
program it imports, to count its fields. A framework's request and settings types are
bundles with many fields.

## Violation

A function or method the change adds, or whose parameters it changes, that takes a
bundle as a parameter when:

- every use of the parameter reads one of its fields; and
- it reads half of the bundle's fields or fewer.

Report it on the parameter.

## Not a violation

- A domain value parameter, however few of its fields the function reads.
- A bundle the function uses as a whole: it passes the bundle on to another call,
  calls one of its methods, returns it, stores it or yields it.
- Several plain values taken as separate parameters, however many.
- A parameter the framework passes and whose signature it sets: a view's or route
  handler's request, a middleware's request, a component's props.
- A function that reads more than half of the bundle's fields.
- Reaching through a value the function does use to another object's fields. That is
  `law-of-demeter`'s.

## Why

A function that takes the whole bundle claims to need all of it. Its tests must build
the whole bundle to call it, its callers must have one to hand, and a reader can't tell
from the signature which of its values decide the result. Taking the values it reads
says exactly what it depends on.

Source: Larry Constantine and Edward Yourdon, *Structured Design* (1979), stamp
coupling; Robert C. Martin, the Interface Segregation Principle, applied to a function's
parameters.
