# In Python

Anonymous results are a returned tuple (`return fee, delivers_on`) and a returned `dict`
with string keys written in the function (`return {"valid": ok, "errors": errors}`).
Named results are a dataclass, attrs class, pydantic model, `NamedTuple` or `TypedDict`.

## Violation

- `def quote(...) -> tuple[Decimal, date]: ... return fee, delivers_on`.
- `return {"valid": not errors, "errors": errors}` from a validation function.
- `return user, created` from a function of the program.

## Not a violation

- `return ShippingQuote(fee=fee, delivers_on=delivers_on)`.
- `return x, y` from a function returning a point's coordinates.
- `__divmod__`, `__reduce__`, `(key, value)` pairs for `dict(...)`.
- A Django view's `get_context_data`, and a dict a DRF or FastAPI view returns as its
  response body.
