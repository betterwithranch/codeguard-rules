# In Python

Comments are `#` lines and trailing `#` text. `# noqa`, `# type: ignore`,
`# pragma: no cover`, `# fmt: off`, `# pyright:`, `# mypy:`, `# pylint:`, `# ruff:`,
`# isort:` and `# ast-grep-ignore:` are directives. ruff's ERA001 and TD003 check
commented-out code and TODOs.

## Violation

- `total += line.amount  # add the line amount to the total`.
- `"""Return the total."""` on `def total(self) -> int`.

## Not a violation

- `BATCH = 50  # the carrier API rejects more than 50 parcels per request`.
- `"""Raises CarrierError when the carrier rejects the address."""`.
