---
name: mock-only-at-boundary
description: A test replaces code with a mock or patch only where that code leaves the process
---

# Mock only at the process boundary

A test replaces part of the program with a test double only where the program hands
work to something outside its own process.

A test double here is what a mocking tool makes: `Mock`, `MagicMock`, `AsyncMock`,
`create_autospec`, `patch`, `patch.object`, `patch.dict`, pytest-mock's
`mocker.patch` and `mocker.Mock`, `monkeypatch.setattr`, `setitem` and `delattr`, and
a plain `setattr` or assignment that swaps a module's or class's attribute for a
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

## The test

For each test double, ask what it replaces: a call or object that leaves the process,
as above, or code that runs inside the program?

Leaves the process, so not a violation:

- `patch("billing.payments.stripe.PaymentIntent.create", side_effect=card_error)`,
  `patch("orders.sync.requests.get", return_value=response)`,
  `mocker.patch.object(s3_client, "put_object")`, `Mock(spec=boto3_client)`;
- `patch("orders.clock.datetime")`, `monkeypatch.setattr(time, "time", lambda: 1000.0)`,
  `patch("random.random", return_value=0.1)`;
- `patch.dict(os.environ, {"MODE": "live"})`, `monkeypatch.setattr(settings,
  "PAYMENTS_ENABLED", False)`, `override_settings(...)`;
- `patch("builtins.open", side_effect=OSError(errno.ENOSPC, "disk full"))`.

Runs inside the program, so a violation:

- the program's own functions, methods (public or private), classes, factories and
  module-level callables or constants: `patch("billing.invoices.calculate_tax")`,
  `patch.object(OrderService, "_validate")`,
  `monkeypatch.setattr(report_module, "load_catalog", lambda: {...})`,
  `billing.invoices.calculate_tax = lambda amount: 0`;
- the database and the code that reads it: a Django manager or queryset
  (`patch.object(Order.objects, "filter")`), a SQLAlchemy `Session` or query, a
  repository, a query result or a row built as a `Mock`;
- a `Mock()` or `MagicMock()` passed to the code under test in place of one of the
  program's own objects (`repository = Mock()`), including the program's own wrapper
  around an outside service (`gateway = Mock(spec=PaymentGateway)` where
  `PaymentGateway` is the program's class that calls Stripe).

The import paths and the modules the test imports say which package is the
program's: a patch target under that package names the program's code unless the
last part is a library it imported (`billing.payments.stripe...`).

## Violation

A test double that replaces code that runs inside the process: one of the program's
own functions, classes, methods, constants or objects, or its database access.
