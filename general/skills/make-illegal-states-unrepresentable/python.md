# In Python

A type is a dataclass, pydantic model, attrs class, `TypedDict` or plain class. An
optional field is annotated `X | None` or `Optional[X]`, set to `None` in `__init__`, or
is a `TypedDict` key marked `NotRequired[X]` or declared in a `total=False` class. A
status or kind field is a `Literal`, an `Enum` or a string whose values name states.

## Violation

- A dataclass with `state: Literal["draft", "sent", "paid"]`, `sent_at: datetime | None`
  and `paid_amount: Decimal | None`, where only a sent invoice has `sent_at` and only a
  paid one has `paid_amount`.
- A pydantic model with `kind: Kind`, `card_number: str | None` and `iban: str | None`.
- A `TypedDict` with `status` and `NotRequired` keys that only some statuses have.
- A dataclass with `email: str | None` and `phone: str | None`, where exactly one of
  them is set.

## Not a violation

- `Draft | Sent | Paid`: three dataclasses or pydantic models, each with its own fields,
  optionally with a `Literal` tag and `Field(discriminator=...)`.
- A Django or SQLAlchemy model with a status column and nullable columns.
- A `TypedDict` or pydantic model that mirrors an outside API's payload as it arrives,
  before it's parsed into the program's own types.
- `middle_name: str | None` and `phone: str | None` on a contact.
