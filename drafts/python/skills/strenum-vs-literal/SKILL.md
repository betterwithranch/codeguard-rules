---
name: strenum-vs-literal
description: Code never branches on, or keys a table by, the values of a `Literal` type that lists two or more values.
---

# No branching on `Literal` value sets

A closed set of names that code branches on or looks things up by is an enumeration
type, not a set of string literals.

A literal value set is a single `Literal[...]` that lists two or more values, in an
annotation or an alias: `Literal["pending", "shipped", "cancelled"]`, or
`type OrderStatus = Literal[...]`. A one-value `Literal["card"]` is a tag, not a value
set, and stays one when read through a union of variants that each declare their own
(`payment.kind` where `payment: CardPayment | BankTransfer`).

Branching on a value means choosing what to do by which value it is: `==` or `!=`
against one of the literals, `in` a tuple, list or set of them, a `match` with `case`
on them, or a dict or registry keyed by them and indexed with the value.

## The test

For each comparison, `in` test, `case` pattern or keyed lookup in the file, ask: is the
value being branched on typed as a literal value set? Find its type from its annotation,
the field or parameter it is read from, or the alias it names, following an import to
the file that defines it.

Typed as a literal value set: a violation. This holds for a dataclass, pydantic, attrs
or `TypedDict` field, a function parameter, and a SQLAlchemy `Mapped[...]` or Django
field annotated with the Literal.

Not a violation:

- branching on members of a `StrEnum`, `IntEnum` or Django `TextChoices`
  (`case OrderStatus.SHIPPED:`, `if order.status is OrderStatus.PENDING`);
- a literal value set that is only stored, validated, passed on or serialized, never
  branched on (a `Literal["json", "yaml"]` option handed to a library);
- branching on a tag, or on the variant's class (`case CardPayment():`);
- comparing a value whose type is `str`, or that the code doesn't show, to a string.

## Violation

A branch on a literal value set: `if order.status == "pending"` or
`match order.status: case "shipped":` where
`status: Literal["pending", "shipped", "cancelled"]`, or `if mode in ("fast", "safe")`
where `mode: Mode` and `type Mode = Literal["fast", "safe", "off"]`.

A dict or registry keyed by a literal value set's values and looked up by a value of
that set: the violation is the dict literal that spells the keys
(`{"created": on_created, "deleted": on_deleted}` looked up by `event.kind` where
`kind: Literal["created", "updated", "deleted"]`).
