---
name: no-dangling-parent-ids
description: A reference to another record in test data carries the id of a record the test or its fixtures created
---

# No dangling parent ids

Test data that points at another record points at one that exists in the test.

A reference is a field or argument that names another record: `order_id`,
`customer_id`, `account_pk`, `parent`, a foreign key. A dangling reference carries a
value that no record in the test has: a fresh `uuid4()`, a `UUID("...")` literal, a
made-up string or number, a random value.

## The test

For each reference in test data (a constructor, a creator call, a request payload, an
attribute assignment), ask: does its value come from, or equal the id of, a record the
test or the fixtures it requests created?

Not a violation:

- the id of a created record: `order_id=order.id`, `parent=category`;
- a literal equal to the id of a record the test or its fixtures created:
  `customer_id="cus-1"` next to `Customer(id="cus-1", ...)`;
- a record's own id: `Order(id=uuid4(), ...)`;
- a missing record as the case under test: the test asserts what happens when the
  referenced record doesn't exist (`pytest.raises(OrderNotFound)`, a 404, `is None`).

A dangling reference:

- `ShipmentService(db).ship(order_id=uuid4(), carrier="UPS")` with no order created;
- `InvoiceService(db).create(account_id=UUID("8f14e45f-..."), ...)` in a fixture with no
  such account;
- `client.post("/shipments/", {"order_id": 999})` when no order 999 exists;
- `line.invoice_id = "inv-404"` on a line whose invoice the test never makes.

## Violation

A reference in test data that carries an id no record created by the test or its
fixtures has, in a test that doesn't assert on the missing record.
