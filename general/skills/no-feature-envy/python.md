# In Python

A type is a class, dataclass, pydantic model, attrs class, `TypedDict`, `NamedTuple` or
Django or SQLAlchemy model the program defines. Its module is the `.py` file that
defines it. A field is an attribute read through the value (`loan.due_on`), a key of a
`TypedDict` (`event["kind"]`), or a `@property`.

## Violation

- A module function in another module whose body reads two or more fields of one
  parameter of a program type and returns an answer from them.
- A method of a service, view or another model that works out an answer from the
  fields of an instance it takes or holds in `self`, reading none of `self`'s own
  fields.
- An inline condition or calculation in a view or task over two or more fields of one
  model instance.

## Not a violation

- A method or `@property` of the type, or a function in the type's `.py` file.
- A call to `loan.is_overdue(today)` or `loans.models.is_overdue(loan, today)`.
- A DRF serializer, a pydantic response model built with `model_validate`, a
  `dataclasses.asdict`, or a dict literal mapping the value's fields to keys.
- A Django template or admin `list_display` reading fields to show them.
