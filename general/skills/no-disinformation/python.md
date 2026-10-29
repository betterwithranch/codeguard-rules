# In Python

Names are read from `def`, `async def` and `class` statements, split on underscores and
capitals. `@property`, `@staticmethod`, `@classmethod` and nested functions are read the
same way.

## Violation

- `def validate_order(order)` whose body sets `order.status = SUBMITTED` and saves it.
- `def get_cached_rates()` whose body calls the rates API on every call.
- `class PdfInvoiceRenderer` whose `render` returns an HTML string.

## Not a violation

- `def submit(order)` that sets the status to submitted and stamps `submitted_at`.
- `__init__`, `__eq__`, and framework hooks such as Django's `save`, `clean` or
  `get_queryset`, whatever their body does.
