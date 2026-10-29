---
name: no-value-with-its-source
description: A call doesn't pass a value together with the input it was derived from; a call to a function, method or class the program declares that receives both an input and a value computed from it is a violation.
---

# No Value With Its Source

A call doesn't pass a value together with the input it was derived from.

A value is derived from an input when the caller computes it from that input: a call
that takes the input (`select_lines(cart, region)` from `region`), one of its fields
(`order.email` from `order`), or one of its keys (`context["region"]`). The derivation
is in the argument list itself, or in a local the same function assigned earlier
(`rate = tax_rate(customer)`, then `invoice_total(subtotal, rate, customer)`).

The callee is declared by the program when its definition is in the file under review
or a file of the program it imports. Read that definition to see what it does with each
argument.

## Violation

A call the change adds or changes that passes both an input and a value derived from it
to a function, method or class the program declares:

- `quote(lines=select_lines(cart, region), region=region)`;
- `notify(order.email, order)`;
- `self._render(self._totals(invoice), invoice)`;
- `Summary(total=total_of(lines), lines=lines)`, building a dataclass, pydantic model
  or attrs class that stores derived data next to its source.

Report it on the call.

## Not a violation

- A builtin or library callee, which can't be changed to derive the value: `dict.get(key,
  default_for(key))`, `getattr`, `min`, `max`, `print`, a logger, `os.path.join`,
  `re.sub`, a third-party client's method.
- A derived argument that is a collaborator the callee calls methods on, not a value:
  `Service(repo=OrderRepository(session), session=session)`,
  `RetryingClient(HttpClient(config), config)`.
- A value derived from a different input than the one passed alongside it:
  `quote(select_lines(cart), region)`.
- A derived value passed without its input: `quote(select_lines(cart, region))`.

## Why

The callee could derive the value from the input itself. Passing both lets the two
disagree: a caller that passes one order and another order's email gets an email sent to
the wrong customer, and nothing in the callee can tell. Every caller also repeats the
derivation, so changing how the value is computed means finding each of them.

Source: house convention, from Kent Beck's "once and only once" and the Single Source of
Truth principle, applied to a call's arguments.
