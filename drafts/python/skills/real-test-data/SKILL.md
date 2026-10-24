---
name: real-test-data
description: Test data is real and made the way production makes it; tests never build an object by hand that a production factory builds, save a record around its production creator, or fill a reference or a matched value with something no real record holds.
---

# Test data is real and made the way production makes it

A test drives the code with data its users' interface makes, so the data holds what
production data holds.

Test data is every object and record test code makes for a test: in a test body, a
helper, a fixture, a `setUp`, a factory or a request payload. Production code is the
application code the test can reach: the modules the file imports, the modules it
imports a type or record from, and any other application file given with the review.
Read those files to find what makes a kind of object or record; a factory or creator
counts wherever among them it is defined.

## The test

For each object or record test code makes, ask: is it made by a path production
doesn't use, or does it point at or hold a value no real record has? The forms below
say which paths and values.

### Built by hand around a production factory

A production factory is application code that builds an object: a function, a
classmethod or a builder that assembles a graph of collaborators
(`build_shipment_service(carrier=...)`, `ShipmentService.from_settings(settings)`), or
derives an object from an input (`invoice_from_order(order)`). Hand assembly is test
code that calls the factory's output type's constructor with the collaborators the
factory would create or the values it would derive.

Violation: test code builds an object by calling its type's constructor with
collaborators or derived values, for use as an input or subject, when a production
factory builds objects of that type:

- `ShipmentService(RateTable.default(), LabelPrinter(carrier), carrier)` when
  `build_shipment_service` assembles that graph;
- `Invoice(order_id=order.id, lines=[...], total=sum(...))` built from an order, to use
  as the input of a test, when `invoice_from_order` derives an invoice from an order;
- a fixture that creates a Django or SQLAlchemy object's related objects one by one
  when a production factory creates the object with them.

The violation is the constructor call.

Not a violation:

- calling the factory, with a test double for a boundary collaborator:
  `build_shipment_service(carrier=FakeCarrier(rate=12))`;
- building the factory's input and calling the factory: `invoice_from_order(order)`;
- constructing a type no production factory builds: a value object, a record, an input
  such as `Order(id="ord-1", items=[...])`;
- constructing the factory's output type as the expected value an assertion compares
  against: `assert invoice_from_order(order) == Invoice(order_id="ord-1", ...)`.

### Saved around a production creator

A creator is the production code that makes and saves a kind of record: a service
method (`InvoiceService(db).create(...)`, `CustomerService(db).register(...)`), a
repository's `create` or `add`, a planner, a domain factory such as
`create_order(customer, items)`. A direct insert is test code that saves the record
some other way: `session.add(Invoice(...))`, `session.execute(insert(invoices)...)`,
`Invoice.objects.create(...)` or `.bulk_create(...)`, `.save()` on a record it
constructed, raw SQL `INSERT`, or a hand-written insert helper.

Violation: test code saves a record by a direct insert when a production creator for
that kind of record exists:

- `db_session.add(Invoice(account_id=account.id, amount=...))` when the file imports
  `InvoiceService`, whose `create` makes invoices;
- `Customer.objects.create(email=...)` when `accounts.signup.sign_up` creates customers;
- a fixture that runs `INSERT INTO orders ...` when `OrderRepository.create` exists.

The violation is the call that saves (`db_session.add(...)`, `.save()`,
`.objects.create(...)`, `.execute(...)`).

Not a violation:

- calling the creator, directly or from a thin helper or fixture that only calls it;
- inserting a kind of record that no production code creates (reference rows such as
  countries or currencies, when nothing in the imported modules creates them), or that
  no file the test can read shows a creator for;
- constructing a record without saving it, to pass to code that doesn't read storage.

### Values no real record holds

A reference is a field, argument or payload key that names another record: `order_id`,
`customer_id`, `account_pk`, `parent`, a foreign key. A matched value is one the
receiving code compares to fixed values or branches on, which the receiver's definition
shows: a `kind`, `status` or `channel` a `match`, an `if` or a lookup table reads.

Violation, in a constructor, a creator call, a request payload or an attribute
assignment in test data:

- a reference whose value is not the id of a record the test or the fixtures it
  requests created: a fresh `uuid4()`, a `UUID("...")` literal, a made-up string or
  number, a random value (`ShipmentService(db).ship(order_id=uuid4(), ...)` with no
  order created, `client.post("/shipments/", {"order_id": 999})` when no order 999
  exists, `line.invoice_id = "inv-404"`);
- a matched value given a generated or random value: `kind=uuid4().hex`,
  `channel=random.choice(["sms", "email"])` where the receiver branches on it.

The violation is the argument, key or assignment.

Not a violation:

- the id of a created record: `order_id=order.id`, `parent=category`;
- a literal equal to the id of a record the test or its fixtures created:
  `customer_id="cus-1"` next to `Customer(id="cus-1", ...)`;
- a record's own id, generated or literal: `Order(id=uuid4(), ...)`;
- a matched value written as a literal or an enum member: `kind="export"`;
- a value the receiver only stores or shows, in any form: a name, a note, an amount;
- a missing record as the case under test: the test asserts what happens when the
  referenced record doesn't exist (`pytest.raises(OrderNotFound)`, a 404, `is None`).

## Violation

Test data made by a path production doesn't use, or holding a value no real record
has: an object built by hand when a production factory builds it, a record saved by a
direct insert when a production creator makes it, a reference to a record the test
never created, or a matched value that is generated.
