---
name: configure-shared-fakes
description: A subclass of a shared fake only configures it; its overrides never assert, reach another subsystem, or record that they ran
---

# Extend shared fakes by configuration

A test changes a shared fake only by configuring what it returns or holds, never by
overriding its behavior to check or record things.

A shared fake is a hand-written stand-in class defined in another test module (a
`tests/fakes.py`, a `conftest.py`, a test-support package) and imported by the file
under review. A subclass of it in the file under review overrides a method when it
defines a method the fake defines or inherits, including `__init__`.

Configuring sets what the fake returns, raises or holds: canned responses, seeded
records, a fixed rate, an error to raise, a value passed to `super().__init__`.

## The test

For each method a subclass of a shared fake defines, ask: does it only configure the
fake, or does it also do one of these?

- assert (`assert`, `pytest.fail`, a `self.assert...` call);
- read or query another subsystem: the database (`Order.objects.filter(...)`,
  `session.query(...)`, `self._db.count_orders(...)`), another fake, the filesystem;
- record that it ran: append to a list, bump a counter, or set a flag the shared fake
  doesn't have, so the test can check the call happened.

Not a violation:

- `__init__` that calls `super().__init__()` and seeds `self.rates = {"EUR": 1.1}`;
- `def fetch_rate(self, currency): raise RateUnavailable(currency)`;
- `def fetch_rate(self, currency): return Decimal("1.10")`;
- a subclass that sets only class attributes (`delay_seconds = 0`);
- a subclass of a class that is not a shared fake (one of the program's classes, a
  `TestCase`).

A violation:

- `def enqueue(self, name, message): assert message["order_id"]` then `super()`;
- `def send(self, message): self.sent_calls.append(message); return super().send(message)`
  where the shared fake has no `sent_calls`;
- `def charge(self, amount): self.charged = True; ...`;
- `def save(self, invoice): assert Invoice.objects.filter(number=invoice.number).exists()`.

## Violation

A method of a subclass of a shared fake, in the file under review, that asserts,
reads another subsystem, or records that it ran.
