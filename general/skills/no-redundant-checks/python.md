# In Python

Checks are `assert`, and an `if`, `elif`, `else` or `match` case that raises, returns,
continues or breaks. Their condition may be a comparison or an `isinstance` or
`issubclass` test. A `cast` and a conditional expression (`a if cond else b`) stop
nothing, so they aren't checks. Guarantees from a type include pydantic `Field(gt=0)`
and validators, a dataclass `__post_init__` that raises, attrs validators, and Django
or SQLAlchemy non-null fields on a row loaded from the database.

## Violation

- `assert customer is not None` below `if customer is None: raise NotFound()`.
- `if order.amount <= 0: raise ValueError(...)`, where `order` was just built by
  `Order.model_validate(data)` and the pydantic model has
  `amount: Decimal = Field(gt=0)`.

## Not a violation

- `if user is None: raise NotFound()` after `user = users.get(user_id)`.
- `if not isinstance(count, int): raise TypeError`, where only the annotation says
  `count: int`. basedpyright's `reportUnnecessaryIsInstance` covers it.
