---
name: enum-usage
description: Code never reads `.value` from a member of an enum whose members already are their string or int value (`StrEnum`, `IntEnum`, `IntFlag`, Django's `TextChoices` and `IntegerChoices`).
---

# No `.value` on a value enum member

A member of an enum whose members already are their value is used as that value, never
unwrapped to it.

A value enum is an enum whose members are instances of their value's type and format,
compare and hash as that value: `StrEnum`, `IntEnum`, `IntFlag`, Django's `TextChoices`
and `IntegerChoices`, and any subclass of these. A plain `Enum`, and an enum that only
mixes in `str` or `int` (`class Color(str, Enum)`), is not a value enum: its members
format as `Color.RED`, so `.value` is how code gets the value.

## The test

For each read of `.value` (`x.value`, `attrgetter("value")`), ask what the receiver is.
Find its type from the code: its annotation, the class it is read from
(`ShipmentStatus.SHIPPED.value`), the field it is read from (`shipment.status.value`
where `Shipment.status: ShipmentStatus`), or the loop over an enum class
(`for status in ShipmentStatus`). Follow an imported enum, model or dataclass to the
file that defines it.

A member of a value enum: a violation, wherever the value goes (an f-string, a dict key,
a comparison, `json.dumps`, a Django query filter, a pydantic field, a SQLAlchemy
column).

Not a violation:

- a member of a plain `Enum`, a `Flag`, or a `(str, Enum)` mix-in;
- `.value` read from anything that is not an enum member: a dataclass, pydantic model,
  attrs class or ORM row with a field named `value`, a `ContextVar` token, a
  `multiprocessing.Value`, a form or widget attribute;
- a receiver whose type the code doesn't show (an unannotated parameter).

Defining a value enum, reading `.name`, or passing the member itself is outside the
rule.

## Violation

`.value` read from a member of a value enum: `status.value` where
`status: ShipmentStatus` and `ShipmentStatus(StrEnum)`, `Priority.HIGH.value` where
`Priority(IntEnum)`, `[kind.value for kind in DocumentKind]` where
`DocumentKind(models.TextChoices)`.
