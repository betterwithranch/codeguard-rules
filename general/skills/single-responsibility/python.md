# In Python

A function is a module function, a method, a `@staticmethod`, `@classmethod` or
`@property`, a nested function, or an `async def`, including a Django view, a DRF action,
a FastAPI route, a Celery task and a CLI command. A class includes a dataclass, a
pydantic model, a Django or SQLAlchemy model, a manager or repository, a service and a
class-based view.

## Violation

- A function that builds an HTML email body with f-strings and, in the same body, works
  out the loyalty points the email reports.
- A Django view or FastAPI route that reads its parameters and then applies a rate table
  or discount rules inline before returning the result.
- A function that unpacks a vendor's nested `dict` payload (its key names, its date
  strings) and applies the business's rules to the values it unpacked.
- A service class for one domain that gains a method writing another system's file
  layout, or calling an outside API that none of its other methods use.

## Not a violation

- A view, route, task or command that parses its input, calls a function that does the
  work, and returns or renders the result.
- A parser that reads every field of one format, converts units and builds the records.
- A frozen dataclass, `NamedTuple` or pydantic value object with arithmetic,
  comparison and `__str__` over its own fields.
- A Django or SQLAlchemy model's methods and properties over its own columns, and a
  manager or repository whose queries all read one model.
- A DRF `ViewSet` whose actions all serve one resource.
