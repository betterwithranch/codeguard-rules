---
name: helpers-return-what-they-build
description: A test helper or fixture returns the objects it builds or receives, never a value it gets by using them
---

# Helpers return what they build

A test helper or fixture hands the test the objects it built, so the test makes every
call on them itself.

Building is making an object or record: a constructor, a factory, a builder chain that
returns the built object (`OrderBuilder().with_total(5).build()`), or a creator that
makes and returns a new record (`InvoiceService(db).create(...)`,
`CustomerService(db).register(...)`, `Order.objects.create(...)`). Using an object is
anything else done to it to get a value out: calling a method that maps, runs,
selects, classifies or computes; reading an attribute; indexing; filtering it in a
comprehension.

## The test

For what each helper or fixture returns or yields, ask: is it an object the helper
built or received, or a value it got by using one?

Built or received, so not a violation:

- `return InvoiceMapper(MappingRules(currency="EUR"))`;
- `return OrderBuilder().with_total(5).build()`;
- `return InvoiceService(db_session).create(account_id=account.id, amount=amount)`;
- a ledger the fixture built and issued invoices into, returned whole: `return ledger`;
- a collection of objects it built: `return [make_line(sku) for sku in skus]`.

Got by using one:

- `return InvoiceMapper(rules).map(raw)`, or `mapper = InvoiceMapper(rules)` then
  `return mapper.map(raw)`;
- `return build_runtime(config).context`;
- `return ledger.overdue_invoices(today=date(2026, 2, 1))`;
- `return [invoice for invoice in ledger.invoices if invoice.overdue]`;
- `return client.get("/orders/").json()`, `return created.id`, `yield service.run()`.

## Violation

A test helper or fixture that returns or yields a value it got by using an object it
built or received.
