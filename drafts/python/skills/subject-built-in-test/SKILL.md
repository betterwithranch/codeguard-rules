---
name: subject-built-in-test
description: The object a test acts on is built where the test shows it, never handed in by a fixture or by setup state
---

# The subject is built in the test

A test builds the object it acts on where its reader can see it.

The act is the call in a test whose result or effect the test's assertions check. The
subject is the application object the act calls a method on: the service, repository,
workflow, mapper or model whose behavior the test checks. A driver the act goes through
(a test client, a CLI runner, a browser page) is not the subject; the view or command it
reaches is. Inputs the act receives (records, settings, fakes passed as arguments) are
not the subject either.

## The test

For each test, find the act and its subject. Ask: is the subject built where the test
shows it, or handed to the test already built?

Built where the test shows it, so not a violation:

- built in the test body: `service = InvoiceService(ledger)`, `repo = OrderRepository(db_session)`;
- built by a helper or factory the body calls: `mapper = make_mapper()`,
  `service = build_shipment_service(carrier=carrier)`;
- built in the test's own `@pytest.mark.parametrize` list;
- a fixture that provides an input or collaborator the body passes to the subject
  (`ledger`, `customer`, `db_session`, a fake gateway), or a driver (`client`, `runner`,
  `tmp_path`).

Handed in already built:

- a test parameter that a fixture provides and the act calls a method on:
  `def test_pay(invoice_service): invoice_service.pay("inv-1")`;
- an attribute of `self` that `setUp`, `setup_method` or a class-scoped fixture set, in a
  unittest `TestCase` or a pytest test class: `self.service.pay("inv-1")`.

## Violation

A test whose act calls a method on a subject the test receives already built: a fixture
parameter, or an attribute of `self` set outside the test method.
