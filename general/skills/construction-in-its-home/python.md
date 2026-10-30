# In Python

A program type is a class, dataclass, pydantic model, attrs class or `NamedTuple` the
program declares. Its homes are `__init__`, `__post_init__` or a `@classmethod`
constructor on it, a function in its `.py` file, a factory class, or a mapper module or
class named for its source (`stripe_mapping.py`, `class CsvRowMapper`). It declares a
default with a field default, `field(default_factory=...)`, pydantic `Field(default=...)`
or `attrs.field(default=...)`.

## Violation

- `account = Account(owner_id=user.id, plan=user.signup_plan, region=user.country)` in a
  service method that then saves and emails.
- `Account(currency=data.get("currency", "USD"), ...)`, `tier=tier or "free"`, or
  `if tier is None: tier = "free"` before `Account(tier=tier)`.
- `def register(email, tier="free"): return Account(email=email, tier=tier)`.
- `Account(account_id=str(uuid4()), ...)` or `opened_at=datetime.now(UTC)` where the
  class leaves the field required.

## Not a violation

- `Account.for_user(user)` or `AccountFactory(clock, ids).open(user)` called from a
  service.
- A Django or SQLAlchemy model created in a view or handler with `objects.create(...)` or
  `Model(...)`.
- `raise AccountLocked(account_id=account.id)`.
- `dataclasses.replace(account, tier="pro")`, `account.model_copy(update=...)`.
- `Path(...)`, `Decimal(...)`, `datetime(...)`, `httpx.Client(timeout=10)`.
