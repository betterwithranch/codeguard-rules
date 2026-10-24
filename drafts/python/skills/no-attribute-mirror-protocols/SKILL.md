---
name: no-attribute-mirror-protocols
description: A Protocol whose members are all data attributes copied, name for name and type for type, from one concrete class that has more fields is a violation.
---

# No protocols that mirror one class's attributes

A protocol states what its consumer needs from the things it accepts, not a slice of one
class's data copied as attributes.

A `Protocol` is a class whose bases include `typing.Protocol` or `Protocol[T]`. Its
members are data members (annotated attributes such as `timeout_seconds: int`, and
properties that only return a value) or methods that do work. A concrete class is a
class in the program that holds data: a dataclass, an attrs class, a pydantic model or
`BaseSettings`, a Django or SQLAlchemy model, a `NamedTuple` or a plain class. It
matches a member when it declares a field or attribute of the same name and type.

## The test

For each `Protocol` defined in the file, ask:

1. Are all of its members data members?
2. Does exactly one concrete class in the repository match every member (search the
   repository for the member names)?
3. Does that class declare fields the protocol leaves out?

Yes to all three is a violation. No to any is not.

Not a violation:

- a protocol with a method that does work (`def charge(self, token: str) -> str`),
  however many data members it also has;
- a protocol whose data members several concrete classes match (`HasId` with `id: int`
  matched by many models);
- a protocol whose members no single class matches, or that matches a class field for
  field with nothing left out.

## Violation

A `Protocol` in the file under review whose members are all data attributes, every one
matching a field of the same single concrete class in the repository, which declares
more fields than the protocol.
