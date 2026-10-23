---
name: constructor-dependencies
description: A method does not take a collaborator (a client, repository, provider, strategy, formatter, registry or clock) as a parameter; its class receives collaborators when it is constructed.
---

# Collaborators arrive at construction

A class receives the collaborators it works with once, when it is built, and its methods
take only the data each call works on.

A collaborator is an object the method calls to get work done: a client, a repository
or DAO, a rate or price provider, a strategy, a formatter or renderer, a registry, a
clock, a mailer, a cache. A parameter's kind decides it, from its annotation or, when it
has none, from its name and from what the method does with it; the callers don't matter.

Data is what the call is about: the records, ids, amounts, dates, a request or event,
a model instance, a query, a callback a caller supplies for this one call.

## The test

For each parameter of a method of a class (other than `self` and `cls`), ask: is it a
collaborator the method calls to do its work, or the data this call works on?

- collaborator: `rate_provider: RateProvider` used as `rate_provider.rate_cents(...)`,
  `formatter: CurrencyFormatter`, `repo: OrderRepository`, `client: httpx.Client`,
  `clock: Clock`, an untyped `mailer` the method calls `.send()` on;
- data: `shipment: Shipment`, `order_id: int`, `lines: list[InvoiceLine]`,
  `request: HttpRequest` in a Django or DRF view method, `since: datetime`, a pydantic
  model, a SQLAlchemy row, `key=` passed to `sorted` for this call.

## Violation

A method of a class takes a collaborator as a parameter: in a plain class, a
dataclass, an attrs class, a pydantic model, a Django model or view, whether the method
is public, private, a `@staticmethod`, or an `async def`.

Not a violation:

- `__init__`, a dataclass, attrs or pydantic field, or a `@classmethod` that builds the
  instance and stores the collaborator on it (`from_settings(cls, client)`);
- a module-level function that takes a collaborator, since it has no constructor;
- a parameter whose type is data, even when the method calls its methods
  (`order.total_cents()`);
- a method whose signature a base class, `Protocol` or framework declares with that
  parameter (a handler interface `def handle(self, event, bus)` that the class
  implements).
