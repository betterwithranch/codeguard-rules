---
name: explicit-discriminated-unions
description: A union of parsed model variants (pydantic models, TypedDicts, msgspec Structs) tags every variant with a literal field and declares the union discriminated on it, so the parser never infers the variant from field shape.
---

# Parsed unions are discriminated by an explicit tag

When data is parsed into one of several variant types, each variant carries a literal
tag and the union names that tag, so the variant is chosen by the tag and never guessed
from which fields fit.

A parsed union is a union of two or more classes that a parser builds from data: a
union of pydantic models or of `TypedDict`s read by pydantic (a model field, a
`TypeAdapter`, a request body), or of msgspec `Struct`s. A union with `None`
(`Shipment | None`), and a union of `str`, `int` or other plain values, has one class
or no classes to choose between and is not a parsed union.

A tag is a field that every variant declares with a one-value literal type
(`kind: Literal["card"] = "card"`), with a different value in each variant; for msgspec
`Struct`s, the `tag=` class argument is the tag. The union
is declared discriminated when it names that field:
`Annotated[CardPayment | BankTransfer, Field(discriminator="kind")]`, a field with
`Field(discriminator="kind")`, a callable `Discriminator(...)` that reads the tag field,
or msgspec `Struct` variants with `tag=` and `tag_field=` set.

## The test

For each union in the file whose members are classes, ask: does a parser build it from
data? If so, does every variant declare the same tag field with its own one-value
literal, and does the union's declaration name that field as its discriminator? Follow
an imported variant to the file that defines it.

Not a violation:

- a union of plain classes or dataclasses that no parser builds (code constructs each
  variant and tells them apart by class, `case CardPayment():`);
- a union with `None`, or of plain values;
- a parsed union that is tagged and names its discriminator, whatever the tag field is
  called.

## Violation

A parsed union whose variant is inferred from field shape:

- the union names no discriminator (`payment: CardPayment | BankTransfer` on a
  pydantic model, `type Event = Created | Deleted` of `TypedDict`s passed to a
  `TypeAdapter`);
- a variant has no tag field, or its tag is a plain `str` rather than a one-value
  literal;
- two variants carry the same tag value.

The violation is on the code that writes the union (`CardPayment | BankTransfer`, the
`Union[...]` or the alias that holds it) and on a variant's missing or plain-`str` tag,
not on fields that only name an alias declared elsewhere.
