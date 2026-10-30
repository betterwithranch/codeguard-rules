# In Python

A type is a class, including a Django model, a DRF view or serializer, a manager, or a
service class. Its public methods are those whose names don't start with `_`.

## Violation

- A `CheckoutPricer.order_total(order)` that adds up line prices and tax, where
  `OrderPricing.total(order)` in `orders/pricing.py` already does.
- A DRF view's `get_queryset` that selects the open tickets with its own filter, where
  `TicketQuerySet.open()` already selects them.
- A `SignupForm.check_password(password)` with its own length and character rules,
  where `PasswordPolicy.validate(password)` already applies them.

## Not a violation

- `CheckoutPricer.order_total(order)` returning `OrderPricing().total(order)` plus a
  checkout fee.
- A Django model method and a serializer field that reads it.
- Classes that implement one `Protocol` or `ABC`, each its own way.
- A method whose name starts with `_`, called by its own class's public methods.
