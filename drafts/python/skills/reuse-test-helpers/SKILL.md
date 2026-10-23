---
name: reuse-test-helpers
description: A test file defines no fake, stub, fixture or helper that does the same job as one a shared test module already provides
---

# Reuse shared test helpers

A test file defines no test helper that a shared test module already provides.

A test helper is a class or function a test file defines for its tests: a fake, stub
or spy class, a pytest fixture, or a function that builds test data or performs setup.

A shared test module is test support other test files use: each `conftest.py` in the
file's directory or a directory above it (pytest hands its fixtures to the file without
an import), and test-support modules such as `tests/fakes.py`, `tests/factories.py`
or `tests/helpers.py`. The judge reads them: the `conftest.py` files on the path from
the file to the repository root, the test modules the file imports, and test-support
modules it finds with Glob under the tests directory.

Two helpers do the same job when they stand for the same thing and behave the same
way for what the file's tests use: a `StubClock` whose `now()` returns the time it was
given and a shared `FakeClock` that does the same; a fixture building the same object
as a `conftest.py` fixture; a `make_order(...)` function building the `Order` a shared
`build_order(...)` builds.

## The test

For each helper the file under review defines, ask: does a shared test module already
provide one that does the same job?

Not a violation:

- a helper for something no shared module provides;
- a fixture with the same name as a `conftest.py` fixture that returns a different
  value for this file's tests (a pytest override: `order` returning a paid order where
  the shared `order` is unpaid);
- a fake that behaves differently in a way the file's tests rely on (a clock that
  advances on each call, where the shared fake clock stays fixed).

A violation:

- `class StubClock` with `now()` returning a fixed time, where `tests/fakes.py` has
  `FakeClock` doing the same;
- a fixture `db_session` building the same session as the shared `conftest.py`'s
  `db_session`;
- `def make_customer(name="Ada")` building the same `Customer` as a shared
  `build_customer`.

## Violation

A helper defined in the file under review that does the same job as one a shared test
module provides.
