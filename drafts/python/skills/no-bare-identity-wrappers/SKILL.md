---
name: no-bare-identity-wrappers
description: A class whose instances hold nothing but one identifier, with no behavior and no check on the value, is a violation.
---

# No bare identity wrappers

A type models a concept with behavior or rules, not a single key that already
identifies something.

An identifier is a value whose job is to name one record or thing: an id, key, code,
slug, reference number or UUID (`order_id: str`, `sku: str`, `customer_key: UUID`).
Behavior is a method or property beyond construction, `__repr__`, `__str__`, equality
and hashing. A check is code the class runs on the value: a pydantic validator or
constrained field (`Field(pattern=...)`, `constr`), an attrs validator, a check in
`__init__` or `__post_init__` that raises, or an enum's closed set of members.

## The test

For each class defined in the file, ask: does each instance hold exactly one value, is
that value an identifier, and does the class define no behavior and no check?

Yes is a violation, in any form:

- a dataclass, attrs class or `NamedTuple` with one identifier field;
- a pydantic `BaseModel` with one identifier field and no validator or constraint;
- a plain class whose `__init__` stores one identifier;
- a subclass of `str`, `int` or `UUID` with an empty body.

Not a violation:

- `NewType("OrderId", str)` and type aliases, which define no class;
- a class that checks its value (an `Iban` that verifies its checksum, a `Sku` whose
  pydantic field has a `pattern`), or an enum;
- a class with behavior (`TrackingNumber.carrier()`);
- a class with two or more values (`OrderRef(region, number)`), or one value that is not
  an identifier (`Money(cents)`, `Percentage(value)`);
- a Django or SQLAlchemy model, which stores a record, not a key.

## Violation

A class in the file under review whose instances hold only one identifier, and which
defines no behavior and no check on it.
