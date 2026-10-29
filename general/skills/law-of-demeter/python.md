# In Python

Exempt fluent and pipeline APIs include pandas and polars chains, Django querysets
(`Order.objects.filter(...).select_related(...)`), SQLAlchemy queries and statements,
and builders that return `self`. A Django model's `ForeignKey` hop that reads a field
of plain data (`order.customer.email`) reads one collaborator's field through the
attribute Django gives it; `order.customer.account.charge(...)` reaches through.

## Violation

- `order.customer.account.charge(order.total_cents)`.
- `self._cart.owner.wallet.balance_cents -= total`.

## Not a violation

- `order.charge_customer()`, where `Order` asks its customer.
- `request.user.email` in a view.
- `df.groupby("region").sum().reset_index()`.
