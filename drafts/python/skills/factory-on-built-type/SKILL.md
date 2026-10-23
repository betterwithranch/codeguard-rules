---
name: factory-on-built-type
description: Code that decides a new instance's field values lives with the type it builds (on the class, or in the class's module) or in a mapper dedicated to one source; never on the source type, and never inline in code whose job is something else.
---

# Construction lives with the type it builds

Building an instance of one of the program's types happens in a place that changes with
that type: on the type, beside it, or in one mapper for the source it is built from.

The built type is a class the program declares: a plain class, a dataclass, a pydantic
model, an attrs class, a `NamedTuple`, a Django or SQLAlchemy model. Building it is
deciding its field values: computing them from a source, reading them off another
object, or picking them. `Shipment(order_id=order.id, address=order.address)` builds a
`Shipment` from an `Order`. Passing values straight through to code that builds is not
building: calling an alternative constructor (`Shipment.from_order(order)`,
`Quote.model_validate(raw)`), or calling the class with the function's own parameters
unchanged (`Handler(name)`).

The source is what the field values come from: another program type (`Order`), or
outside data: a payload, file contents, a command's output, a raw row (data whose shape
something outside the program decides).

## The test

For each construction of a program type that decides its field values, find where it
is and ask: is this one of the places where that type may be built?

The places where a type `C` may be built:

- on `C`: a `@classmethod` alternative constructor (`from_order`, `from_row`,
  `from_acme`), `__init__`, `__post_init__`, or another method of `C`;
- in `C`'s module: a function beside the class (`def default_settings() -> Settings`
  defined below `Settings`);
- in a mapper: a module or class whose job is translating one source into the
  program's types, and nothing else. `carriers/acme.py` turning Acme's API payloads
  into `TrackingEvent`s, `class OrderRowMapper` turning database rows into `Order`s,
  `orders/shipping_mapping.py` turning `Order`s into `Shipment`s. A mapper may also make
  the calls that fetch its source, such as a carrier client that requests the payload
  and translates it.

Anything else is not one of those places:

- the source type: `Order.to_shipment()` builds a `Shipment` from inside `Order`;
- code whose job is something else: a service method, a use case, a view, a command or
  a task handler that builds `C` inline among its other work;
- a module that is neither `C`'s module nor a mapper for this source:
  `shipping/planning.py` with a `make_shipment(order)` among planning functions.

Code that only delegates may live anywhere: a cache, registry or service that gets its
instance from an alternative constructor or a mapper (`_handlers[name] =
Handler.for_name(name)`, `events = acme.events_from(payload)`).

Read the built type's module when it is imported, to see whether the code under review
is that module, and what the type provides.

## Violation

A construction that decides a program type's field values, in a place that is not on
that type, in its module, or in a mapper for its source. The violation is the
construction call.

Not a violation:

- any construction on the built type or in its module;
- any construction in a mapper for one source, whether the source is outside data or
  another program type; a mapper is never required, and never a violation;
- delegation to an alternative constructor or a mapper, from anywhere;
- instances of classes the program doesn't declare (`Path`, `datetime`, `Decimal`, a
  third-party SDK's request object);
- copies of an existing instance with changed fields (`dataclasses.replace(order, ...)`,
  `order.model_copy(update=...)`, `attrs.evolve(order, ...)`).
