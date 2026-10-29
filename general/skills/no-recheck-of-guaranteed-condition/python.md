# In Python

Checks are `assert`, an `if` that raises, returns, continues or breaks, `isinstance`,
`issubclass`, `cast`, and a `match` case that raises. Guarantees from a type include
pydantic `Field(gt=0)` and validators, a dataclass `__post_init__` that raises, attrs
validators, and Django or SQLAlchemy non-null fields.

## Violation

- `assert customer is not None` below `if customer is None: raise NotFound()`.
- `if order.amount <= 0: raise ValueError(...)`, where `order` is a pydantic model with
  `amount: Decimal = Field(gt=0)`.

## Not a violation

- `if user is None: raise NotFound()` after `user = users.get(user_id)`.
- `if not isinstance(count, int): raise TypeError`, where only the annotation says
  `count: int`. basedpyright's `reportUnnecessaryIsInstance` covers it.
