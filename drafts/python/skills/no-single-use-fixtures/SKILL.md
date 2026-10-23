---
name: no-single-use-fixtures
description: A fixture defined in a test module is requested by more than one test or fixture in that module
---

# No single-use fixtures

A fixture exists to share setup, so a fixture a test module defines is used by more
than one test or fixture there.

A fixture defined in a test module is visible only to that module, so the module shows
every use of it. A test or fixture requests a fixture by:

- naming it as a parameter: `def test_pay(ledger)`, `def invoice_service(ledger)`;
- naming it in `@pytest.mark.usefixtures("ledger")` on the test, or on a test class,
  which requests it for every test in the class;
- `autouse=True`, which requests it for every test in its scope.

## The test

For each fixture defined in the module under review, count the tests and fixtures in
that module that request it. Is the count exactly one?

Not a violation:

- two or more tests request it, or a test and another fixture do;
- it is `autouse=True`, or a class-level `usefixtures` names it for a class with more
  than one test;
- a `conftest.py` fixture: its users are in other modules.

A violation:

- one test requests it, directly or through `usefixtures`, and nothing else does:
  `@pytest.fixture def overdue_ledger(): ...` used only by `test_sends_reminder`;
- one other fixture requests it and no test does.

## Violation

A fixture defined in a test module that exactly one test or fixture in the module
requests.
