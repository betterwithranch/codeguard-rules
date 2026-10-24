---
name: arrange-act-assert-in-body
description: A test shows its arrange, act and assert in its own body; no fixture or helper hides the subject it acts on, the scenario it starts from, or the act it checks.
---

# Arrange, act and assert are in the test body

A reader of one test sees what it builds, what it does and what it expects, without
reading fixtures and helpers to find out.

The act is the call into the code under test whose result or effect a test's
assertions check: the function or method whose return value the test compares, or
whose change to state (a ledger entry, a sent message, a saved row, a status) it
asserts. The subject is the application object the act calls a method on: the service,
repository, workflow, mapper or model whose behavior the test checks. A driver the act
goes through (a test client, a CLI runner, a browser page) is not the subject; the view
or command it reaches is. Input data is everything else the act receives: records,
values, settings, collaborators and fakes passed as arguments.

A fixture is a function pytest calls for a test that names it (`@pytest.fixture`,
`@pytest_asyncio.fixture`), or `setUp`, `setup_method` and class-scoped setup that set
attributes on `self`. A helper is any other function or class in test code a test or
fixture calls. A fixture or helper may build input data and hand it to the test whole;
that is arrange the test names and shows.

## The test

For each test, fixture, helper and type in test code, ask: does a fixture or helper
hide the subject, the scenario or the act from the test body, in one of the forms
below?

### The subject is handed in

Violation: a test whose act calls a method on a subject it receives already built:

- a test parameter a fixture provides, and the act calls a method on it:
  `def test_pay(invoice_service): invoice_service.pay("inv-1")`, or
  `def test_cancel(order): order.cancel(...)` on a record the fixture created;
- an attribute of `self` that `setUp`, `setup_method` or a class-scoped fixture set, in
  a unittest `TestCase` or a pytest test class: `self.service.pay("inv-1")`.

The violation is the test.

Not a violation:

- the subject built in the test body (`service = InvoiceService(ledger)`), by a helper
  or factory the body calls (`mapper = make_mapper()`), or in the test's own
  `@pytest.mark.parametrize` list;
- a fixture that provides input data the body passes to the subject (`ledger`,
  `customer`, `db_session`, a fake gateway, a record handed to a function under test),
  or a driver (`client`, `runner`, `tmp_path`).

### The act runs in a fixture

Violation: a fixture makes the call a test's assertions check, so the test that
requests it has no act of its own:

- a fixture returns the result of calling the code under test, and the test only
  asserts on it: `@pytest.fixture def receipt(cart): return checkout(cart)`, a fixture
  that returns `client.post("/checkout/")`'s response;
- a fixture calls the code under test for its effect (`service.pay("inv-42")`,
  `notifier.send_reminders()`, `call_command("close_month")`), and the test asserts on
  that effect without making the call itself.

The violation is the fixture.

Not a violation: the test calls the code under test, directly or through a helper the
body calls, and asserts on the result or on what its own act did to the inputs
fixtures provide.

### The scenario runs in a fixture

An application operation is a call into the code under test that changes the state of
an object or record that already exists: starting a workflow or job, issuing,
submitting, approving, paying, cancelling, adding an item to a cart, moving a record to
another status. It may be a method call (`workflow.start(order)`), a service call that
takes the record's id (`OrderService(db).submit(order.id)`), or a request through a
test client (`client.post(f"/orders/{order.pk}/submit/")`).

Violation: a fixture runs an application operation on an object or record that exists
before the call, so the test that requests it starts from the state that operation
leaves. The violation is the operation's call.

Not a violation:

- building: a constructor, factory or builder (`OrderBuilder().with_total(5).build()`),
  or a creator whose result is the new record the fixture returns or builds with
  (`CustomerService(db).register(email=...)`, `Order.objects.create(...)`);
- readying the environment every test in the file runs in, whatever its scenario:
  starting and stopping a worker, server or broker, opening a transaction, creating
  tables, setting a feature flag or setting, registering a handler or plugin, freezing
  the clock, logging the test client in.

### A helper returns what it got by using an object

Building is making an object or record: a constructor, a factory, a builder chain that
returns the built object, or a creator that makes and returns a new record. Using an
object is anything else done to it to get a value out: calling a method that maps,
runs, selects, classifies or computes; reading an attribute; indexing; filtering it in
a comprehension.

Violation: a test helper or fixture returns or yields a value it got by using an
object it built or received: `return InvoiceMapper(rules).map(raw)`,
`return build_runtime(config).context`, `return ledger.overdue_invoices(today=...)`,
`return [invoice for invoice in ledger.invoices if invoice.overdue]`,
`return client.get("/orders/").json()`, `yield service.run()`. The violation is the
return or yield.

Not a violation: returning an object the helper built or received, whole
(`return InvoiceMapper(MappingRules(currency="EUR"))`,
`return InvoiceService(db_session).create(...)`), or a collection of objects it built
(`return [make_line(sku) for sku in skus]`).

### A fixture both sets a condition and provides a value

A condition is state outside the value a fixture returns: a setting or environment
variable, a feature flag, a patched or monkeypatched name whose replacement the fixture
doesn't return, a frozen or moved clock, a registered handler, a row or file the
returned value doesn't hold.

Violation: a fixture returns or yields a value and also establishes a condition that
the value doesn't carry: `monkeypatch.setenv("REGION", "eu")` and then
`return OrderService()`; `settings.FEATURES = {...}` and then `return employee`;
registering a handler, enabling a flag or freezing the clock, then yielding a client.
The violation is the fixture.

Not a violation:

- a setup fixture that returns nothing, autouse or not;
- a fixture whose effects are all part of its value: a record it creates and returns, a
  temporary directory it makes and returns, a server it starts, yields and stops, a
  patch whose replacement it yields, a fake it installs and returns;
- a fixture that requests a setup fixture as a parameter.

### A fixture only one test uses

A fixture defined in a test module is visible only to that module, so the module shows
every use of it. A test or fixture requests it by naming it as a parameter, by
`@pytest.mark.usefixtures(...)` on the test or on its class (a request for every test
in the class), or by the fixture's `autouse=True`.

Violation: a fixture defined in a test module that exactly one test or fixture in the
module requests, directly or through `usefixtures`. The violation is the fixture, both
when the change adds it and when the change adds or removes a request that leaves it
with exactly one.

Not a violation: a fixture two or more tests request, or a test and another fixture;
an `autouse=True` fixture; a class-level `usefixtures` on a class of more than one
test; a fixture in a `conftest.py`, whose users are in other modules.

### A type bundles what setup built

A setup bundle is a type defined in test code that has no behavior of its own and
whose fields hold objects a helper or fixture built (records, services, fakes,
clients), so that tests reach them as `setup.cart` or `resources.customer`: a
dataclass, a `NamedTuple`, a `TypedDict`, an attrs or pydantic class, a plain class
whose `__init__` only stores its arguments, or a `SimpleNamespace` or `namedtuple(...)`
built on the fly.

Violation: a setup bundle defined or built in test code. The violation is the type's
definition, or the `SimpleNamespace` or `namedtuple` call.

Not a violation: a fake, stub or spy with behavior; a test driver whose methods act (a
page object, a `CheckoutDriver` with `add_item()` and `pay()`); a parametrize case
type whose fields hold literal inputs and expected values.

### A helper takes one input two ways

Two parameters of a helper or fixture factory are alternatives when the caller passes
one or the other: each supplies the same value in a different form, and the body uses
whichever was passed. An object and its id (`account` and `account_id`), an object and
the key it is looked up by (`author` and `author_username`), one quantity in two units
(`amount` and `amount_cents`), a path and the text it holds.

Violation: a test helper that declares two parameters for the same value and chooses
between them in its body, in any form that chooses
(`account.id if account is not None else account_id`, `account_id or account.id`, an
`if`/`elif` on which was passed), so a call doesn't show which input the helper builds
from. The violation is the helper's signature.

Not a violation: parameters that each supply a different value, two optional
parameters for different values (`billing_account` and `shipping_account`), or one
optional parameter with a fallback that isn't another parameter
(`account = account or make_account(db_session)`).

## Violation

Test code where a fixture or helper hides part of a test's arrange, act or assert from
its body: a subject handed in already built, an act or a scenario run in a fixture, a
helper that returns what it got by using an object, a fixture that sets a condition and
provides a value, a fixture only one test uses, a type that bundles what setup built,
or a helper that takes one input two ways.
