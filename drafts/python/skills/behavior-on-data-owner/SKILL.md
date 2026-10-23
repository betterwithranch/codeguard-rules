---
name: behavior-on-data-owner
description: A function that reads nothing but one value's own data is a method of that value's type, not a free function, a static method, or a method that ignores its own object.
---

# Behavior lives on the type whose data it reads

Behavior computed only from one value's own data is defined on that value's type.

The value's type is a class the program declares with its own fields: a plain class, a
dataclass, a pydantic model, an attrs class, a `NamedTuple`, a Django or SQLAlchemy
model. It is declared in the file under review or in a file of the program that file
imports; read that file when the type is imported. A function reads a value's own data
when it reads the value's attributes or calls the value's own methods.

## The test

For each function defined with `def` outside the class it reads — a module-level
function, a nested function, a `@staticmethod`, a `@classmethod`, or a method whose body
never uses `self` — ask: does its body read anything besides one parameter's own data?

Inputs that don't count, so the function still reads only that parameter's data:
literals, module constants, builtins (`len`, `sorted`, `round`), and methods of the
field values themselves (`line.sku.casefold()`, `event.at.date()`).

Inputs that count, so the answer is yes:

- a second parameter, even one of the same type (`a.total < b.total`);
- a variable of an enclosing function, read by a nested function;
- `self` or `cls` state, or any collaborator: a client, a repository, a clock, a
  registry;
- module state that changes at run time, a file, the environment, the network.

## Violation

The answer is no: the function reads only one parameter's own data, and that
parameter's type is a class the program declares. This holds whatever the function
returns — a sort key, a predicate (`weight_kg > 30`), a derived amount, a formatted line,
a dict of its fields — and whether it is public or private.

Not a violation:

- the parameter's type is not the program's: `str`, `int`, `datetime`, `dict`, a
  `Path`, a third-party class (`requests.Response`), a `Protocol` or abstract interface;
- the function is a method the class's base class or `Protocol` declares, so the
  interface sets its signature (`def render(self, invoice)` on a `Renderer` subclass);
- the function builds and returns a new instance of a different class the program
  declares (`Shipment(...)` from an `Order`): that is construction, not behavior of
  the parameter;
- a lambda (`key=lambda line: line.position`);
- a method defined on the parameter's own type (`def is_heavy(self)` on `Shipment`).
