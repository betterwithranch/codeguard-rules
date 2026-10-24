---
name: seed-through-creator
description: Test data for a record is created through the production code that creates that record, never by inserting the record another way
---

# Seed test data through the production creator

Tests create a record the way production does, so test data holds what production
data holds.

A creator is the production code that makes and saves a kind of record: a service
method (`InvoiceService(db).create(...)`, `CustomerService(db).register(...)`), a
repository's `create` or `add`, a planner, a domain factory such as
`create_order(customer, items)`. A direct insert is test code that saves the record
some other way: `session.add(Invoice(...))`, `session.execute(insert(invoices)...)`,
`Invoice.objects.create(...)` or `.bulk_create(...)`, `.save()` on a record it
constructed, raw SQL `INSERT`, or a hand-written insert helper.

## The test

For each record test code saves, ask: does a production creator exist for that kind of
record, and does the test code save the record without it? Look for the creator in
what the file imports, and in the module the file imports the record type from.

Not a violation:

- calling the creator, directly or from a thin helper or fixture that only calls it;
- inserting a kind of record that no production code creates (reference rows such as
  countries or currencies, when nothing in the imported modules creates them);
- constructing a record without saving it, to pass to code that doesn't read storage.

A direct insert:

- `db_session.add(Invoice(account_id=account.id, amount=...))` when the file imports
  `InvoiceService`, whose `create` makes invoices;
- `Customer.objects.create(email=...)` when `accounts.signup.sign_up` creates customers;
- a fixture that runs `INSERT INTO orders ...` when `OrderRepository.create` exists.

## Violation

The call that saves a record by a direct insert (`db_session.add(...)`, `.save()`,
`.objects.create(...)`, `.execute(...)`) when a production creator for that kind of
record exists.
