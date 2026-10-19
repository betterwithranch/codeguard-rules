---
name: fixture-shape
description: Fixture shape
---

# Fixture shape

- A fixture returns one object. Do not return or yield a tuple built in a variable.
- Keep setup-only fixtures (they establish a condition) apart from data fixtures (they return a value).
- Construct test data in fixtures, not in module-level constants. Flag a module-level `SCREAMING_SNAKE` value that constructs domain objects or stands in for an id a test asserts on. Plain opaque scalars (a token string) are exempt.
- A test that asserts on an identity value owns that value; it does not read it from a shared constant.
