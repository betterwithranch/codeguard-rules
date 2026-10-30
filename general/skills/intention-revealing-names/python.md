# In Python

Framework-chosen names include Django's `handle` on a management command, `get`,
`post` and `dispatch` on a view, Celery's `run`, and `unittest`'s `setUp`.

## Violation

- `def process_data(shipments)` whose body marks each shipment delivered.

## Not a violation

- `def mark_delivered(shipments)`.
