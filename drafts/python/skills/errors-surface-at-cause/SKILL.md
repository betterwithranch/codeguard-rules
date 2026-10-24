---
name: errors-surface-at-cause
description: An error surfaces where it is caused; code doesn't swallow an error it can't handle, fall back silently to a default for data that should exist, or clamp a state that should never exist.
---

# Errors surface at their cause

When something goes wrong, the code where it goes wrong fails, so the error is seen
where it was caused instead of as a wrong value somewhere later.

An error is anything that tells the code it can't do what it was asked: a raised
exception, data that should exist and doesn't, a value in a state the program's rules
say can never happen. Code handles an error when it does something that answers it:
retries the operation, raises an error that names the failure in the program's own terms
(`raise PaymentDeclined(order.id) from err`), takes a documented other path that still
does the job, or, at the program's top level (a CLI's `main`, a request handler's error
response, a worker's loop over independent jobs), reports it to the user or the log and
stops that one unit of work. Code hides an error when it carries on as if nothing went
wrong.

Whether data should exist is read from the code: a field the model declares required,
a setting the program can't work without (a secret, a service URL, a database URL), a
key the code itself put in the mapping, an id the program created. Optional data has a
real default: a query parameter, a user preference, a display name, a page size, a log
level.

## The test

For each `except` clause, `contextlib.suppress`, defaulted lookup, `or` fallback and
`min`/`max` clamp the change touches, ask: does the code after it carry on with a value
that hides an error it can't handle, or does the error surface where it was caused?

### Swallowed exceptions

Violation: an `except` clause, or `contextlib.suppress`, that catches an error the code
doesn't handle and carries on: its body is `pass`, `continue` or `break`, returns a
default (`None`, `0`, `[]`, `False`, an empty object), or only logs and then carries on
as if the work were done. A bare `except:`, `except Exception` or `except
BaseException` around work whose failure the caller needs to know about is one, however
it logs. It is reported on the `except` clause or the `suppress` call.

Not a violation:

- catching a specific error the code expects and handling it: a retry, a raise of the
  program's own error (with `from err` or `from None`), an `else` path that still does
  the job;
- a top-level boundary that turns the error into a user-facing message, an error
  response or an exit code, and stops that unit of work;
- `contextlib.suppress` or `except` of a specific error whose case is expected and
  harmless where it runs: `suppress(FileNotFoundError)` around deleting a temporary
  file, `except KeyError` on a lookup of optional data;
- an `except` that cleans up and re-raises (`raise` with no argument).

### Silent fallback defaults

A fallback default is a value the code puts in place of missing data: the second
argument of `dict.get`, `os.environ.get`, `os.getenv` or `.pop`, the third of
`getattr`, a literal after `or` (`value or 0`, `name or ""`), or a literal chosen when
a value `is None`.

Violation: a fallback default for data that should exist, so its absence turns into a
wrong value later instead of an error now: `config.get("payments_url", "")`,
`os.environ.get("STRIPE_SECRET_KEY", "")`, `RATES.get(currency) or 1.0` on a currency
the order was priced in, `line.quantity or 0` on a field the model declares required.
It is reported on the default.

Not a violation: a default for optional data that is a real value for it
(`params.get("page_size", 20)`, `os.environ.get("LOG_LEVEL", "INFO")`,
`user.nickname or "Guest"`), and a lookup without a default that raises when the data
is missing (`config["payments_url"]`).

### Clamped impossible states

A clamp is `max`, `min` or a comparison that forces a computed value into a range
(`max(0, balance)`, `min(percent, 100)`).

Violation: a clamp on a value the program's own rules say can never leave that range,
so a broken rule turns into a plausible number instead of an error: `max(0,
account.balance_cents - amount_cents)` hiding an overdraft, `max(0, product.stock -
quantity)` hiding an oversold item. It is reported on the clamp.

Not a violation: a clamp on outside input, which may be anything
(`max(1, requested_page)` on a query parameter); a clamp that states a business rule
where both sides of it are valid states (`min(coupon_cents, subtotal_cents)` when a
coupon may exceed the cart).

## Violation

Code in the file under review that hides an error from where it was caused: an
`except` or `suppress` that swallows an error it doesn't handle, a fallback default for
data that should exist, or a clamp on a state that should never exist.
