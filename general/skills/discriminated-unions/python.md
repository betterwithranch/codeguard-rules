# In Python

Parsed unions are unions of pydantic models, `TypedDict`s read by pydantic and msgspec
`Struct`s: `CardPayment | BankPayment`, `Union[...]`, a `type` alias, or a
`TypeAdapter` of one. The discriminator is named with `Field(discriminator="kind")`,
`Annotated[..., Discriminator(...)]`, or msgspec's `tag=` and `tag_field=`. A tag is
declared `kind: Literal["card"] = "card"`.

## Violation

- `payment: CardPayment | BankPayment` with no `Field(discriminator=...)`.
- `kind: str = "bank"` on a variant of a discriminated union.
- Two variants both declaring `kind: Literal["card"]`.

## Not a violation

- `payment: CardPayment | BankPayment = Field(discriminator="kind")`, each variant
  with its own `Literal` tag.
- `amount: Decimal | int`, and `note: str | None`.
- Dataclasses the program builds and handles with `match payment: case CardPayment():`.
