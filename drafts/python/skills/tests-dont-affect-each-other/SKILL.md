---
name: tests-dont-affect-each-other
description: No test or fixture leaves a change to state behind for the next test, or hands several tests state one of them can change; each test runs as if it ran alone.
---

# Tests don't affect each other

Each test runs as if it ran alone: nothing one test, or a fixture it uses, changes is
seen by another test.

A test affects another in two ways: it changes state that outlives it and doesn't undo
the change, or it changes state that several tests share. The forms below are where
each appears: state of the process left changed, data stored on a test class, and a
fixture value or teardown shared by a wider scope than one test.

Undone means code that runs whether the test passes or fails restores the old state
or releases the resource before the next test: `monkeypatch` (`setenv`, `setattr`,
`chdir`, `syspath_prepend`), `patch` as a decorator or context manager, `patch.dict`,
pytest-django's `settings` fixture or `override_settings`, a `with` block, a yield
fixture whose code after `yield` restores it, `request.addfinalizer`,
`self.addCleanup`, a `try`/`finally`, `tmp_path` and `tmp_path_factory`.

## The test

For each change a test, setup method or fixture makes to state, and each resource it
acquires, ask: does the change outlive this test, or reach state other tests share,
in a way the form below names as a violation?

A change to an object the test itself built (a local `Cart()`, a value a
function-scoped fixture made for this test) or to an attribute on `self` reaches no
other test.

### State left behind

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

Violation: a change to state that outlives the test, or a resource the test or its
fixture acquires, that no code running whether the test passes or fails undoes:

- `os.environ["PAYMENTS_MODE"] = "live"` with nothing that restores it;
- `billing.tax.RATE = Decimal("0")` in a test body;
- `del os.environ["X"]` at the end of the test body, after the assertions, which
  doesn't run when an assertion fails;
- `connection = sqlite3.connect(path)` that is never closed;
- `logging.getLogger("billing").setLevel(logging.DEBUG)` left set.

The violation is the line that makes the change or acquires the resource.

Not a violation:

- `monkeypatch.setenv("PAYMENTS_MODE", "live")`;
- a fixture that saves `plugins.registered()`, yields, and restores it after `yield`;
- `with open(tmp_path / "orders.csv") as handle:`;
- `patcher.start()` with `self.addCleanup(patcher.stop)`.

### Data stored on the test class

A class attribute of a test class belongs to the class, so every test of the class
sees the same object: it is assigned in the class body, through `cls` (in
`setup_class`, `setUpClass` or a classmethod), through `type(self)`, or through the
class's name. pytest and unittest make a new instance for each test, so an attribute
the test or its setup assigns on `self` (`self.skus = []` in `setup_method` or `setUp`)
belongs to that test alone.

A change is an assignment (`cls.last_cart = cart`, `TestCart.count += 1`), an item
assignment (`self.totals["A-1"] = 3`), or a mutating call (`append`, `extend`,
`insert`, `add`, `update`, `setdefault`, `pop`, `remove`, `discard`, `clear`) on the
attribute's object.

Violation: a test or setup method that changes data stored on its test class, reached
through `self`, `cls`, `type(self)` or the class's name:

- `added_skus = []` in the class body, and a test that calls
  `self.added_skus.append(...)`;
- `seen = {}` in the class body, and a test that sets `self.seen["A-1"] = 1`;
- a test that sets `TestCart.last_cart = cart` or `type(self).last_cart = cart` for
  another test to read.

The violation is the change.

Not a violation:

- `self.skus = []` in `setup_method`, then `self.skus.append("BOOK-1")` in a test;
- a class attribute the tests only read: `skus = ("BOOK-1", "PEN-2")`, or a list no
  test changes;
- `setup_class` that sets `cls.catalog = load_catalog()` when no test changes it.

### Wide-scope fixtures

A wide-scope fixture has a pytest scope wider than one test: `scope="session"`,
`"package"`, `"module"` or `"class"`, or a scope a function picks. It runs once for all
the tests in that scope, so each of them gets the same value, and its code after
`yield` runs once, after the last of them.

A changeable value is one a test can change in place: a `list`, `dict` or `set`, an
instance of a class with assignable fields (a plain class, a dataclass without
`frozen=True`, a pydantic model without `frozen`, an ORM record), or an in-memory store
or fake the tests write to. A `str`, number, `tuple`, `frozenset`, frozen dataclass,
frozen pydantic model or `MappingProxyType` is not changeable.

Violation: a wide-scope fixture that returns or yields a changeable value, or whose
code after `yield` resets state the tests in its scope change, so the reset runs once,
after the last of them, rather than after each:

- `@pytest.fixture(scope="module")` returning `Cart()` that a test adds items to;
- `@pytest.fixture(scope="session")` returning `{"EUR": Decimal("1.1")}`;
- `@pytest.fixture(scope="module", autouse=True)` whose code after `yield` calls
  `registry.clear()` while each test registers plugins.

The violation is the fixture.

Not a violation:

- `@pytest.fixture(scope="session")` returning a frozen dataclass, a tuple of ids or a
  `Path` to read-only data;
- a function-scoped fixture (no `scope`, or `scope="function"`) returning a list or a
  `Cart()`;
- a module-scoped fixture that yields nothing and resets, after `yield`, state the
  tests don't change.

## Violation

Code in the file under review through which one test affects another: a change to
state that outlives the test, or a resource it acquires, that nothing running whether
the test passes or fails undoes; a test or setup method that changes data stored on
its test class; or a fixture with a scope wider than one test that returns or yields a
changeable value, or whose teardown resets state its tests change.
