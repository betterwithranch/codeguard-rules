# In Python

A function is a module function, a method, a `@staticmethod`, `@classmethod` or
`@property`, a nested function, or an `async def`. A module of the program is one the
file imports by `import loans.fees` or `from loans.fees import late_fee`; the standard
library and third-party packages are not the program.

## Violation

- A function whose body repeats another's steps: `renewal_penalty(rate, days)` doing what
  `late_fee(days, rate)` does, line for line.
- Private siblings that repeat each other's steps with a different constant each, where
  one function taking the value as an argument would state the steps once.
- A module function or another class's method that repeats the steps of a method the
  type already has: `def due_back(loan)` computing what `Loan.due_date()` returns.
- Calls that chain a process's stages outside it, through locals, nested calls or
  `await`: `store(clean(read_rows(path)))` beside an `ingest(path)` that runs those
  three stages in that order.
- A module-level tuple, list, set or dict that lists exactly another set's members: its
  items, a dict's keys, or an `Enum`'s members or values.
  `SUPPORTED_FORMATS = ("csv", "json")` beside `FORMATS = {"csv": write_csv, "json":
  write_json}`.
- A second dataclass, pydantic model, `TypedDict` or `NamedTuple` with the fields of
  one already modelling the same message, file or response.

## Not a violation

- A call to the representation, with or without steps around it:
  `return late_fee(days, rate) + LOST_ITEM_CHARGE`.
- A collection derived from another: `tuple(FORMATS)`, `frozenset(Format)`,
  `[member.value for member in Format]`, `typing.get_args(FormatName)`.
- `@overload` signatures, and `Protocol` or abstract method stubs (`...`, `pass`,
  `raise NotImplementedError`).
- What a framework asks each class to declare: a Django model's `Meta` and `__str__`,
  a DRF serializer's `Meta`, a pydantic validator for each class's own field, an
  `__eq__` comparing the class's own fields.
- A Django or SQLAlchemy model and a pydantic model with the same fields, one for the
  stored row and one for the API, mapped where they meet.
