---
name: tests-survive-refactoring
description: A test depends only on what the program does at its edges, so it keeps passing when the internals change and every observable result stays the same; it doesn't replace or assert on the program's own code, make shared fakes check or record, or keep its own copy of shared test support.
---

# Tests survive refactoring

A test depends only on the results the program produces and the work it hands outside
its process, so it keeps passing when the program's internals change and every
observable result stays the same.

The internals are how the program produces its results: which of its own functions,
classes and methods run, in what order and with which arguments, and how its parts are
wired. An observable result is what a caller sees: a return value, a raised error, the
state the program leaves in its database or files, and the work it hands to something
outside its process. A test double is what a mocking tool makes: `Mock`, `MagicMock`,
`AsyncMock`, `create_autospec`, `patch`, `patch.object`, `patch.dict`, pytest-mock's
`mocker.patch` and `mocker.Mock`, `monkeypatch.setattr`, `setitem` and `delattr`, and a
plain `setattr` or assignment that swaps a module's or class's attribute for a
stand-in. A hand-written fake class the test constructs is not one.

The process boundary is where the program hands work to something it doesn't run
itself:

- another service over the network: an HTTP call (`requests.post`, an `httpx` client),
  a third-party or cloud SDK call (`stripe.PaymentIntent.create`, a `boto3` client's
  `put_object`), email or SMS delivery, a subprocess;
- the operating system: the clock (`datetime.now`, `time.time`), the random source,
  environment variables and the settings or feature flags read from them, and a
  failure only the OS or network produces (a refused connection, a timeout, a full
  disk).

The program's own code is everything else: its functions, methods (public or private),
classes, factories, module-level callables and constants, its own wrapper around an
outside service, and its database and the code that reads it. The import paths and the
modules the test imports say which package is the program's: a target under that
package names the program's code unless its last part is a library it imported
(`billing.payments.stripe...`).

## The test

For each piece of code the forms below describe, ask: if the program's internals
changed (a function renamed, split or inlined, a collaborator replaced, a call
reordered, a helper extracted) but every observable result stayed the same, would this
test still pass, and would it need no second copy of test support changed with it?

Each form below says what is a violation and where it is reported.

### Test doubles inside the process

Violation: a test double that replaces the program's own code:

- `patch("billing.invoices.calculate_tax")`, `patch.object(OrderService, "_validate")`,
  `monkeypatch.setattr(report_module, "load_catalog", lambda: {...})`,
  `billing.invoices.calculate_tax = lambda amount: 0`;
- the database and the code that reads it: a Django manager or queryset
  (`patch.object(Order.objects, "filter")`), a SQLAlchemy `Session` or query, a
  repository, a query result or a row built as a `Mock`;
- a `Mock()` or `MagicMock()` passed to the code under test in place of one of the
  program's own objects (`repository = Mock()`), including the program's own wrapper
  around an outside service (`gateway = Mock(spec=PaymentGateway)` where
  `PaymentGateway` is the program's class that calls Stripe).

The violation is reported on the double's creation or the patch.

Not a violation, because the replaced code leaves the process:
`patch("billing.payments.stripe.PaymentIntent.create", side_effect=card_error)`,
`patch("orders.sync.requests.get", return_value=response)`,
`mocker.patch.object(s3_client, "put_object")`, `Mock(spec=boto3_client)`,
`patch("orders.clock.datetime")`, `monkeypatch.setattr(time, "time", lambda: 1000.0)`,
`patch.dict(os.environ, {"MODE": "live"})`, `monkeypatch.setattr(settings,
"PAYMENTS_ENABLED", False)`, `override_settings(...)`, `patch("builtins.open",
side_effect=OSError(errno.ENOSPC, "disk full"))`.

### Assertions on internal calls

A recorded call is what a mocking tool records about the calls a test double receives,
read through `assert_called`, `assert_called_with`, `assert_called_once_with`,
`assert_any_call`, `assert_has_calls`, `assert_not_called`, the `assert_awaited`
family, `call_args`, `call_args_list`, `mock_calls`, `method_calls`, `call_count`,
`called`, or a `mocker.spy`. The callee is the function, method or object the double
stands in for.

Violation: an assertion on a recorded call to the program's own code, whether it was
called, how often, or with which arguments: `calculate_tax.assert_called_once_with(
Decimal("100.00"), "CA")` after patching `billing.invoices.calculate_tax`; `assert
repository.save.call_args == call(invoice)` where `repository` stands in for the
program's `InvoiceRepository`; `spy = mocker.spy(OrderService, "_reserve_stock")` then
`assert spy.call_count == 1`; `notifier.notify.assert_not_called()` where `notifier`
stands in for the program's `Notifier`. The violation is reported on the assertion.

Not a violation: a recorded call to something outside the process
(`session.post.assert_called_once_with("https://api.example.com/charges", json=body)`
where `session` stands in for a `requests.Session`, a `boto3` client's `put_object`);
an assertion on a result or on a hand-written fake's state (`assert queue.messages ==
[{"order_id": "A-1"}]`, `assert mailer.outbox == [...]`), which is not a recorded call.

### Shared fakes made to check or record

A shared fake is a hand-written stand-in class defined in another test module (a
`tests/fakes.py`, a `conftest.py`, a test-support package) and imported by the file
under review. A subclass of it in the file under review overrides a method when it
defines a method the fake defines or inherits, including `__init__`. Configuring sets
what the fake returns, raises or holds: canned responses, seeded records, a fixed rate,
an error to raise, a value passed to `super().__init__`.

Violation: a method of a subclass of a shared fake that, besides configuring it,
asserts (`assert`, `pytest.fail`, a `self.assert...` call), reads or queries another
subsystem (the database, another fake, the filesystem), or records that it ran (appends
to a list, bumps a counter, or sets a flag the shared fake doesn't have):
`def send(self, message): self.sent_calls.append(message); return super().send(message)`,
`def charge(self, amount): self.charged = True; ...`, `def save(self, invoice): assert
Invoice.objects.filter(number=invoice.number).exists()`. The violation is reported on
the method.

Not a violation: an `__init__` that calls `super().__init__()` and seeds data; a
method that returns or raises a canned value; a subclass that sets only class
attributes; a subclass of a class that is not a shared fake (one of the program's
classes, a `TestCase`).

### Copies of shared test support

A test helper is a class or function a test file defines for its tests: a fake, stub
or spy class, a pytest fixture, or a function that builds test data or performs setup.
A shared test module is test support other test files use: each `conftest.py` in the
file's directory or a directory above it, and test-support modules such as
`tests/fakes.py`, `tests/factories.py` or `tests/helpers.py`. Read the `conftest.py`
files on the path from the file to the repository root, the test modules the file
imports, and test-support modules found with Glob under the tests directory.

Two helpers do the same job when they stand for the same thing and behave the same way
for what the file's tests use: a `StubClock` whose `now()` returns the time it was
given and a shared `FakeClock` that does the same; a fixture building the same object
as a `conftest.py` fixture; a `make_order(...)` building the `Order` a shared
`build_order(...)` builds.

Violation: a helper defined in the file under review that does the same job as one a
shared test module provides. The violation is reported on the helper's definition.

Not a violation: a helper for something no shared module provides; a fixture with the
same name as a `conftest.py` fixture that returns a different value for this file's
tests (a pytest override); a fake that behaves differently in a way the file's tests
rely on (a clock that advances on each call, where the shared fake clock stays fixed).

## Violation

Code in the file under review that ties a test to the program's internals: a test
double replacing the program's own code or database access, an assertion on a recorded
call to the program's own code, a subclass of a shared fake that asserts, reads another
subsystem or records that it ran, or a helper duplicating one a shared test module
provides.
