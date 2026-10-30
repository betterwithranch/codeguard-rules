# In Python

## Violation

- `send_receipt(order.customer.email, order)` where `send_receipt` is declared in the
  program and reads `order` too.
- `apply_discount(cart, discount_for(cart))` where both functions are the program's.

## Not a violation

- `settings.get("timeout", default_timeout("timeout"))`: `dict.get` is a builtin.
- `logger.info("sent %s", order.id, extra={"order": order})`: a library call.
