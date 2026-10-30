# In Python

Creation methods include `@classmethod`s that return `cls(...)`, `@staticmethod`s that
return a new instance of their class, methods of a `...Factory`, `...Creator` or
`...Maker` class, and functions and methods named `create_...`, `make_...`,
`build_...`, `new_...`, `for_...` or `from_...`, whether at module level or in a class.

## Violation

- `@classmethod def for_admin_dashboard(cls, ...)` on `Report`.

## Not a violation

- `@classmethod def from_csv_row(cls, row)`.
