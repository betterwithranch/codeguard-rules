---
name: union-variants-together
description: A named union's variant classes are defined in the module that declares the union, as one unbroken run of definitions directly before the alias.
---

# A union's variants are defined together, next to its alias

A named union and the types it is made of are read as one unit, so the variants sit in
one place, side by side, ending in the union's name.

A union alias is a module-level name for a union of two or more classes:
`type PaymentMethod = CardPayment | BankTransfer`,
`PaymentMethod = CardPayment | BankTransfer`, `PaymentMethod = Union[...]`, or
`PaymentMethod = Annotated[CardPayment | BankTransfer, Field(discriminator="kind")]`.
Its variants are the classes it names. A union with `None` (`Card | None`), or of plain
values (`int | str`), is not a union alias. An inner union alias that the outer alias
names is itself a variant: its own variants and alias form a run inside the outer run.

The run is the module-level code from the first variant's definition to the alias.

## The test

For each union alias in the file, ask:

1. Is every variant defined in this module? A variant imported from another module is
   defined elsewhere.
2. Does the run hold only the variants' definitions (with their decorators) and inner
   union aliases? Any other class, function, constant or statement in the run breaks
   it.
3. Does the alias come directly after the run?

Any "no" is a violation. This holds alike for pydantic models, dataclasses, attrs
classes, `TypedDict`s, `NamedTuple`s and msgspec `Struct`s.

Not a violation:

- code before the first variant or after the alias (imports, a base class the variants
  share, functions that use the union);
- a base class the variants inherit from, defined before the run;
- a union written inline in an annotation (`payment: CardPayment | BankTransfer`), which
  has no alias.

## Violation

A union alias whose variants are not one run directly before it in its module: a
variant imported from another module, an unrelated class or a function defined between
two variants, or the alias declared before its variants or with other code between the
last variant and the alias.
