# In Python

A field is an annotated name in a class body (a dataclass, pydantic, attrs or ORM model
field) or an attribute set on `self`.

## Violation

- `shipped_at: datetime | None` and `is_shipped: bool = False` on one dataclass.
- `__init__` setting `self.items = []` and `self.item_count = 0`, and `add` appending to
  one and incrementing the other.
- `customer: Customer` and `customer_email: str` on one class, where `Customer` has
  `email` and nothing sets `customer_email` at a moment of its own.

## Not a violation

- `@property def is_shipped(self) -> bool: return self.shipped_at is not None`, or a
  `cached_property` on an immutable class.
- `is_gift: bool` beside `shipped_at`.
- `billed_address: Address`, set once by the method that issues the invoice, beside
  `customer`.
- A Django `ForeignKey` and its `_id` column, or a SQLAlchemy `customer_id` column beside
  its `customer` relationship.
