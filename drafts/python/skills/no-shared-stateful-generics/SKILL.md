---
name: no-shared-stateful-generics
description: One instance shared by every use (module-level, class-level, a default argument, or a cached factory's result) of a class whose methods store the results of a use on the instance is a violation.
---

# No shared instances of stateful classes

An object that collects the results of one piece of work is created for that work, never
shared between uses.

A class is stateful when a method called while doing the work, not while setting the
object up, writes that work's results to the instance: it appends to or adds to an
attribute (`self.issues.append(...)`, `self.rows.extend(...)`), reassigns one
(`self.total += amount`, `self.current = order`), or calls a method that does. An
instance is shared when one instance serves every use: it is assigned at module level,
as a class attribute (including a dataclass or pydantic field default), as a parameter
default, or returned by a cached function (`@cache`, `@lru_cache`).

## The test

For each shared instance in the file, find its class, in the file or in the module it is
imported from, and ask: does a method called while doing the work write that work's
results to the instance?

Yes is a violation, whatever builds the instance: the class itself
(`validator = OrderValidator(region="eu")`) or a factory function that returns one
(`validator = create_order_validator()`).

Not a violation:

- a shared instance whose methods write nothing to the instance during the work: a
  stateless calculator or formatter, a frozen dataclass or pydantic settings object, a
  compiled regex, a logger, an HTTP client;
- state written once while setting the object up, at import or start-up, and only read
  afterwards: routes added to a FastAPI `APIRouter` or Flask `Blueprint`, handlers added
  to a registry by decorators, a Celery app's configuration;
- state that exists to be shared across uses rather than to hold one use's results: a
  cache keyed by its inputs, a connection pool, a lock, a metrics counter;
- an instance created inside a function, per call, which is not shared.

## Violation

An instance in the file under review, created where every use shares it, of a class
whose methods write the results of one use to the instance.
