---
name: no-scenario-fixtures
description: A fixture builds objects and readies the environment; it never runs the application operations that put a test's objects into the state its act starts from
---

# No scenario fixtures

A fixture builds what a test needs and readies the environment the tests run in; the
steps that bring the application's objects into a test's starting state happen in the
test.

An application operation is a call into the code under test that changes the state of
an object or record that already exists: starting a workflow or job, issuing, submitting,
approving, paying, cancelling, adding an item to a cart, moving a record to another
status. It may be a method call (`workflow.start(order)`), a service call that takes the
record's id (`OrderService(db).pay(order.id)`), or a request through a test client
(`client.post(f"/orders/{order.pk}/submit/")`).

## The test

For each call in a fixture, ask: is it an application operation on an object or record
that exists before the call, made so that a test's act starts from the state it leaves?

Not an application operation, so not a violation:

- building: a constructor, factory or builder (`InvoiceService(ledger)`,
  `OrderBuilder().with_total(5).build()`), or a creator whose result is the new record
  the fixture returns or builds with (`CustomerService(db).register(email=...)`,
  `Order.objects.create(...)`, `session.add(Order(...))`);
- readying the environment every test in the file runs in, whatever its scenario:
  starting and stopping a worker, server or broker, opening a transaction, creating
  tables, setting a feature flag or setting, registering a handler or plugin, freezing
  the clock, logging the test client in.

An application operation:

- `workflow.start(order)` or `job.run()` on a workflow or job the fixture built;
- `service.issue("inv-42", amount=120)` on the service the fixture returns;
- `OrderService(db).submit(order.id)` or `order.approve()` on a record created just before;
- `client.post(f"/carts/{cart.pk}/items/", {...})` that changes a record before the test.

## Violation

A fixture that runs an application operation on an existing object or record, so the
test that requests it starts from the state that operation leaves.
