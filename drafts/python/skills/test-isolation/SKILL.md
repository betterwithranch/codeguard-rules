---
name: test-isolation
description: A test, or a fixture it uses, undoes every change it makes to state that outlives the test and releases every resource it acquires
---

# Tests leave no state behind

A test, and every fixture it uses, undoes each change it makes to state that outlives
the test and releases each resource it acquires.

State that outlives the test is anything the next test in the same process can see:

- environment variables (`os.environ`);
- module attributes and constants (`billing.tax.RATE = 0`, `settings.PAYMENTS_MODE =
  "live"`), class attributes of the program's classes (`Order.max_items = 2`), and
  `global` variables;
- `sys.path`, `sys.modules`, `sys.argv`, the current directory (`os.chdir`);
- logging configuration and log levels, `locale.setlocale`, the default socket
  timeout, the event loop policy;
- registries and singletons the program keeps (`plugins.register(CsvExporter)`,
  `cache.set(...)` on a module-level cache);
- a patcher started with `.start()`.

A resource is something the test opens: a file, a database connection, a socket, a
thread, a subprocess, a temporary directory made outside `tmp_path`.

Undone means code that runs whether the test passes or fails restores the old state
or releases the resource before the next test: `monkeypatch` (`setenv`, `setattr`,
`chdir`, `syspath_prepend`), `patch` as a decorator or context manager, `patch.dict`,
pytest-django's `settings` fixture or `override_settings`, a `with` block, a yield
fixture whose code after `yield` restores it, `request.addfinalizer`,
`self.addCleanup`, a `try`/`finally`, `tmp_path` and `tmp_path_factory`.

## The test

For each change to state that outlives the test, and each resource it acquires, ask:
does code that runs whether the test passes or fails undo it?

Not a violation:

- `monkeypatch.setenv("PAYMENTS_MODE", "live")`;
- a fixture that saves `plugins.registered()`, yields, and restores it after `yield`;
- `with open(tmp_path / "orders.csv") as handle:`;
- `patcher.start()` with `self.addCleanup(patcher.stop)`.

A violation:

- `os.environ["PAYMENTS_MODE"] = "live"` with nothing that restores it;
- `billing.tax.RATE = Decimal("0")` in a test body;
- `del os.environ["X"]` at the end of the test body, after the assertions, which
  doesn't run when an assertion fails;
- `connection = sqlite3.connect(path)` that is never closed;
- `logging.getLogger("billing").setLevel(logging.DEBUG)` left set.

## Violation

A change to state that outlives the test, or a resource the test acquires, that no
code running whether the test passes or fails undoes.
