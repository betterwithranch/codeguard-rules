---
name: separate-setup-and-data-fixtures
description: A fixture either establishes a condition and returns nothing, or provides a value; never both
---

# Separate setup fixtures from data fixtures

Each fixture does one of two jobs: it establishes a condition the tests run under, or
it provides a value they use.

A condition is state outside the value a fixture returns: a setting or environment
variable, a feature flag, a patched or monkeypatched name whose replacement the fixture
doesn't return, a frozen or moved clock, a registered handler, a row or file the
returned value doesn't hold. A setup fixture establishes conditions and returns or
yields nothing. A data fixture returns or yields a value.

## The test

For each fixture, ask: does it return or yield a value, and also establish a condition
that the value doesn't carry?

Not a violation:

- a setup fixture that returns nothing: `settings.FEATURES = {...}`,
  `monkeypatch.setenv("REGION", "eu")`, `freezer.move_to(...)`, autouse or not;
- a data fixture whose effects are all part of its value: a record it creates and
  returns, a temporary directory it makes and returns, a server it starts, yields and
  stops, a patch whose replacement it yields (`with patch("billing.gateway") as gateway:
  yield gateway`), or a fake it installs with `monkeypatch.setattr` and returns;
- a data fixture that requests a setup fixture as a parameter: the condition lives in
  the other fixture.

A violation:

- `monkeypatch.setenv("REGION", "eu")` and then `return OrderService()`;
- `settings.FEATURES = {"instant_payouts": True}` and then `return employee`;
- registering a handler, enabling a flag or freezing the clock, then yielding a client.

## Violation

A fixture that returns or yields a value and also establishes a condition outside that
value.
