# In Python

Parsed unions are unions of pydantic models and of `TypedDict`s read by pydantic:
`CardPayment | BankPayment`, `Union[...]`, a `type` alias, or a `TypeAdapter` of one or
of a `list` or `dict` of one. The discriminator is named with
`Field(discriminator="kind")` or `Annotated[..., Discriminator(...)]`. A tag is declared
`kind: Literal["card"] = "card"`, or `kind: Literal["card"]` on a `TypedDict`.

## Violation

- `TypeAdapter(CardPayment | BankPayment)`, or a `type` alias or `list[...]` of the
  union, with no discriminator named.
- A union with no discriminator named where one variant declares a `Literal` tag and
  another has no tag field.

## Not a violation

- `Annotated[CardPayment | BankPayment, Field(discriminator="kind")]`, each variant
  with its own `Literal` tag.
- `amount: Decimal | int`, and `note: str | None`.
- Dataclasses the program builds and handles with `match payment: case CardPayment():`.
- Forms pydantic and msgspec refuse when the model, adapter or decoder is built: a
  discriminated union's variant whose tag is `str` rather than a `Literal`, or that has
  no tag field; two variants with the same tag value; a msgspec union of `Struct`s that
  aren't all tagged with unique values.
- A field of a pydantic model annotated directly as a union of pydantic models the same
  file defines (`field: ModelA | ModelB`), with no discriminator named. The pattern rule
  `union-declares-discriminator` reports it.
