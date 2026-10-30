# In Python

A program type is a class, dataclass, pydantic model, attrs class or `NamedTuple` the
program declares. Its homes are `__init__`, `__post_init__` or a `@classmethod`
constructor on it, a function in its `.py` file, a factory class, or a mapper module or
class named for its source (`stripe_mapping.py`, `class CsvRowMapper`). A Django or
SQLAlchemy model is the persistence library's to build.

## Violation

- `account = Account(owner_id=user.id, plan=user.signup_plan, region=user.country)` in a
  service method that then saves and emails.
- `Account.model_validate(response.json())` in a handler that then charges the account.
- An `Invoice` method that returns `Account(owner_id=self.customer_id, ...)`.

## Not a violation

- `Account.for_user(user)` or `AccountFactory(clock, ids).open(user)` called from a
  service.
- `Account(owner_id=owner_id, plan=plan)` from the function's own parameters, or with
  `status=AccountStatus.PENDING`.
- `User.objects.create(...)`, or `session.add(User(...))`, in a view or handler.
- `raise AccountLocked(account_id=account.id)`.
- `dataclasses.replace(account, tier="pro")`, `account.model_copy(update=...)`.
- `Path(...)`, `Decimal(...)`, `datetime(...)`, `httpx.Client(timeout=10)`.
