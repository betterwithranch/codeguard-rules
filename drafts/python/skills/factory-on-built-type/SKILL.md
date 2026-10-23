---
name: factory-on-built-type
description: A function that builds and returns a new instance of one of the program's classes is defined on that class, not as a free function, a static method, or a method of another class that ignores its own object.
---

# Construction lives on the type it builds

Code that builds a new instance of a type is defined on that type.

The built type is a class the program declares: a plain class, a dataclass, a pydantic
model, an attrs class, a `NamedTuple`, a Django or SQLAlchemy model. It is declared in
the file under review or in a file of the program that file imports; read that file
when the class is imported. A function builds an instance when it calls the class
(`Shipment(...)`) or one of its alternative constructors (`Shipment.model_validate(...)`,
`Shipment.from_row(...)`) and returns the result.

## The test

For each function defined with `def` outside the class it builds — a module-level
function, a nested function, a `@staticmethod` or method of another class, a method
whose body never uses `self` — ask: is what it returns a new instance of one class the
program declares, built in this function?

The answer is yes whatever the function reads to build it: its parameters, a parsed
payload, a file, a module constant, or nothing (`def default_settings() -> Settings`).

The answer is no when the function returns:

- an instance of a class the program doesn't declare: `Path`, `datetime`, `Decimal`, a
  `FastAPI` app, a `logging.Logger`, a third-party SDK's request object;
- an instance it didn't build here: one it looked up (`Order.objects.get(...)`,
  `session.get(Order, order_id)`, `registry[name]`) or received;
- a copy of a parameter with changed fields (`dataclasses.replace(order, ...)`,
  `order.model_copy(update=...)`, `attrs.evolve(order, ...)`);
- a collection of instances, or a value other than the instance (it builds an object,
  saves or sends it, and returns an id).

## Violation

A function outside class `C` whose result is a new `C` it builds, where `C` is a class
the program declares: `def make_shipment(order: Order) -> Shipment` at module level,
`ShipmentPlanner.shipment_for` as a static method, or a nested `def to_event(row)` that
returns `ScanEvent(...)`.

Not a violation:

- a `@classmethod`, `@staticmethod` or method defined on `C` itself, or on a base class
  of `C`, that builds a `C`;
- a method of another class that uses `self` to build the instance (a builder that reads
  its own collected state, a repository that maps its rows);
- a lambda, and a class passed as a factory (`field(default_factory=list)`).
