# In Python

A program type is a class, dataclass, pydantic model, attrs class, `NamedTuple` or
Django or SQLAlchemy model the program declares. It declares a default with a field
default, `field(default_factory=...)`, pydantic `Field(default=...)`,
`attrs.field(default=...)`, a column's `default=`, or a parameter default on its own
`__init__`.

## Violation

- `Account(currency=data.get("currency", "USD"), ...)`, `tier=tier or "free"`, or
  `if tier is None: tier = "free"` before `Account(tier=tier)`.
- `def register(email, tier="free"): return Account(email=email, tier=tier)`.
- `Account(account_id=str(uuid4()), ...)` or `opened_at=datetime.now(UTC)` where the
  class leaves the field required, in a service or in a `@classmethod` on it.

## Not a violation

- `Account(email=email)` where the class declares `tier: str = "free"`.
- `tier=requested_tier or user.signup_tier`, a fallback to other data.
- `AccountFactory(clock, ids)` passing `opened_at=self.clock.now()`.
- `Account(email=email, tier=Tier.TRIAL)` in a function that opens trial accounts.
- `def recent_accounts(limit: int = 20)`, or `httpx.get(url, timeout=10)`.
