---
name: interface-in-consumer-package
description: A Protocol or abstract base class defined in a package where none of the code that depends on it lives is a violation.
---

# Interfaces live with their consumers

An interface is defined in the package of code that depends on it.

An interface is a class whose bases include `Protocol` (`typing.Protocol`,
`Protocol[T]`) or `ABC` (`abc.ABC`, `metaclass=ABCMeta`), with members left for others to
supply. A consumer is code outside test files that annotates a parameter, attribute or
return value with the interface and uses its members; a class that only subclasses or
implements it is an implementer, not a consumer. A module's package is the directory it
is in (`payments/gateway.py` is in `payments/`); a subpackage is a different package.

## The test

For each interface defined in the file, find its consumers: in the file, and in the rest
of the repository by searching for the interface's name. Then ask: is any consumer in
the interface's own package?

Yes is not a violation. No, every consumer is in another package, is a violation,
whether the interface sits beside its implementers, in a shared `interfaces` or `base`
module, or alone. An interface with no consumer in the repository is not a violation
of this rule.

Placing it:

- `notifications/base.py` defines `Notifier(ABC)`, `notifications/sms.py` implements it,
  and only `orders/checkout.py` takes a `Notifier`: a violation;
- `orders/ports.py` defines `PaymentGateway(Protocol)`, `orders/checkout.py` takes one,
  and `payments/stripe.py` implements it: not a violation;
- a `Protocol` defined in the same module as the function that takes it: not a
  violation.

## Violation

An interface defined in the file under review whose consumers are all in packages other
than its own.
