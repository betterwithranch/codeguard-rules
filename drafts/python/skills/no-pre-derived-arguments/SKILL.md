---
name: no-pre-derived-arguments
description: A call to the program's own function or class does not pass both a value and the input that value was derived from.
---

# No pre-derived arguments

A call does not hand its callee both an input and a value derived from that input.

A value is derived from an input when the caller computes it from that input: a call
that takes it (`select_lines(cart, region)` from `region`), one of its fields
(`order.email` from `order`), or a key of it (`context["region"]`). The derivation is
inline in the argument list or assigned to a local earlier in the same function
(`rate = tax_rate(customer)` and then `invoice_total(subtotal, rate, customer)`).

## The test

For each call that receives both an input and a value derived from it, ask: is the
callee a function, method or class the program declares, so it could take the input
and derive the value itself?

Yes:

- a function or method declared in the file under review or a file of the program it
  imports: `quote(lines=select_lines(cart, region), region=region)`,
  `notify(order.email, order)`, `self._render(self._totals(invoice), invoice)`;
- a class the program declares that stores derived data next to its source: a
  dataclass, pydantic model or attrs class built with
  `Summary(total=total_of(lines), lines=lines)`.

No:

- a builtin or library callee, which can't be changed to derive it: `dict.get(key,
  default_for(key))`, `getattr`, `min`, `max`, `print`, `logging`, `os.path.join`,
  `re.sub`, a third-party client's method;
- the derived argument is a collaborator built to be injected, not a value: an object
  the callee calls methods on (`Service(repo=OrderRepository(session), session=session)`,
  `RetryingClient(HttpClient(config), config)`).

## Violation

A call to a function, method or class the program declares that receives both an input
and a value the caller derived from it, inline or through a local.
