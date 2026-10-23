---
name: wide-scope-fixtures-share-no-state
description: A fixture shared by several tests gives them nothing one test can change for the next, and doesn't defer per-test cleanup to the end of its scope
---

# Wide-scope fixtures share no changeable state

A fixture that several tests share hands them nothing one test can change for the
next.

A wide-scope fixture has a pytest scope wider than one test: `scope="session"`,
`"package"`, `"module"` or `"class"`, or a scope a function picks. It runs once for all
the tests in that scope, so each of them gets the same value, and its code after
`yield` runs once, after the last of them.

A changeable value is one a test can change in place: a `list`, `dict` or `set`, an
instance of a class with assignable fields (a plain class, a dataclass without
`frozen=True`, a pydantic model without `frozen`, an ORM record), or an in-memory store
or fake the tests write to. A `str`, number, `tuple`, `frozenset`, frozen dataclass,
frozen pydantic model or `MappingProxyType` is not changeable.

## The test

For each wide-scope fixture, ask:

1. Does it return or yield a changeable value?
2. Does its code after `yield` reset state that the tests in its scope change, so the
   reset runs once, after the last of them, rather than after each?

Either answer yes is a violation.

Not a violation:

- `@pytest.fixture(scope="session")` returning a frozen dataclass, a tuple of ids or a
  `Path` to read-only data;
- a function-scoped fixture (no `scope`, or `scope="function"`) returning a list or a
  `Cart()`;
- a module-scoped fixture that yields nothing and resets, after `yield`, state the
  tests don't change.

A violation:

- `@pytest.fixture(scope="module")` returning `Cart()` that a test adds items to;
- `@pytest.fixture(scope="session")` returning `{"EUR": Decimal("1.1")}`;
- `@pytest.fixture(scope="module", autouse=True)` whose code after `yield` calls
  `registry.clear()` while each test registers plugins.

## Violation

A fixture with a scope wider than one test that returns or yields a changeable value,
or whose teardown resets state its tests change.
