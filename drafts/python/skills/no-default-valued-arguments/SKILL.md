---
name: no-default-valued-arguments
description: Test code never passes an argument equal to the default of the parameter it fills
---

# No arguments that repeat a default

A call in test code passes only the arguments that change what the callee would do.

A default-valued argument is an argument whose value equals the default of the
parameter it fills: `make_invoice(db_session, account, status="draft")` when
`make_invoice` declares `status: str = "draft"`. The callee's signature decides it: a
function or class defined in the file under review, or in a project module the file
imports from. For a dataclass, attrs or pydantic class the defaults are its field
defaults; for a Django or SQLAlchemy model, the `default=` of its fields.

## The test

For each argument in a call to a callee whose definition is in the project, find the
parameter it fills. Does that parameter have a default, and does the argument equal
it?

Not a violation:

- an argument that differs from the default: `status="paid"` when the default is
  `"draft"`;
- an argument to a parameter with no default, whatever its value;
- a call to a third-party or standard-library callee;
- `**overrides` passed through untouched.

A violation, by keyword or by position:

- `status="draft"` to `status: str = "draft"`;
- `notes=None` to `notes: str | None = None`;
- `currency=Currency.EUR` to a dataclass field `currency: Currency = Currency.EUR`;
- `make_order(customer, 1)` when the second parameter is `quantity: int = 1`.

## Violation

An argument in test code equal to the default of the parameter it fills.
