---
name: no-alternative-helper-inputs
description: A test helper takes each input through one parameter; it never accepts the same value through two parameters and picks whichever was passed
---

# One parameter per helper input

A test helper takes each value it needs through one parameter, in one form.

Two parameters are alternatives when the caller passes one or the other: each supplies
the same value in a different form, and the body uses whichever was passed. An object
and its id (`account` and `account_id`), an object and the key it is looked up by
(`author` and `author_username`), one quantity in two units (`amount` and
`amount_cents`), a path and the text it holds.

## The test

For each helper or fixture factory with optional parameters, ask: do two of its
parameters supply the same value, with the body using whichever one the caller passed?

Not a violation:

- each parameter supplies a different value: `make_invoice(account: Account, amount: Decimal)`;
- one optional parameter with a fallback that isn't another parameter:
  `account = account or make_account(db_session)`, `due = due or date(2026, 1, 31)`;
- two optional parameters for different values: `billing_account` and
  `shipping_account`.

A violation, in any form that chooses:

- `resolved_id = account.id if account is not None else account_id`;
- `account_id = account_id or account.id`;
- `if account is not None: ... elif account_id is not None: ...`;
- `amount = amount if amount is not None else Decimal(amount_cents) / 100`.

## Violation

A test helper that declares two parameters for the same value and chooses between them
in its body.
