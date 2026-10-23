---
name: narrow-collaborator-params
description: A function does not take a bundle object (a context, request, settings, config or state object) when all it does with it is read a few of its fields.
---

# Take the values, not the bundle

A function takes the values it uses, not a bundle object it only reads a few fields
from.

A bundle is an object whose job is to carry many unrelated values to many consumers:
a context (`CheckoutContext`, `RequestContext`), settings or config (`Settings`,
`AppConfig`, a pydantic `BaseSettings`), a web request (`HttpRequest`, a FastAPI
`Request`), an environment or app-state object. Its fields are inputs for different
parts of the program, not facts about one thing. A domain value is not a bundle: an
`Order`, `Invoice` or `Shipment`, a `DateRange`, a `Money`, a `TypedDict` of one
record's fields, whose fields all describe one thing.

The bundle's class is declared in the file under review or a file it imports; read it
there to see its fields. A framework's request and settings types are bundles.

## The test

For each parameter that is a bundle, ask two questions:

1. Is every use of the parameter a read of one of its fields (`context.shipping_region`,
   `settings.page_size`, `request.headers`)? It is not when the function passes the
   object on to another call (`self._printer.archive(context)`), calls one of its methods
   (`context.receipt_lines()`, `request.is_secure()`), or returns it, stores it on
   `self`, or yields it.
2. Count the distinct fields the function reads and the fields the bundle's class
   declares. Does it read half of them or fewer?

A violation needs yes to both. Reading 2 of 6 fields is a violation; reading 3 of 4 is
not, since the function uses most of the bundle.

## Violation

A function or method that takes a bundle parameter and only reads a few of its fields:
a method `tax_cents(self, context: CheckoutContext)` that reads `context.subtotal_cents`
and `context.shipping_region`, a helper taking `settings: Settings` for one timeout.

Not a violation:

- a domain value parameter, however few of its fields the function reads;
- a bundle the function uses as a whole, as listed above;
- a framework method whose signature the framework sets: a Django or DRF view's
  `get(self, request)`, a FastAPI route that declares `request: Request`, a middleware's
  `__call__(self, request)`.
