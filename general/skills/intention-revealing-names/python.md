# In Python

Creation methods include `@classmethod`s that return `cls(...)`, methods of a
`...Factory`, `...Creator` or `...Maker` class, and methods named `create_...`,
`make_...`, `build_...`, `new_...`, `for_...` or `from_...`.

Framework-chosen names include Django's `handle` on a management command, `get`,
`post` and `dispatch` on a view, Celery's `run`, and `unittest`'s `setUp`.

## Violation

- `def process_data(shipments)` whose body marks each shipment delivered.
- `@classmethod def for_admin_dashboard(cls, ...)` on `Report`.

## Not a violation

- `def mark_delivered(shipments)`.
- `@classmethod def from_csv_row(cls, row)`.
