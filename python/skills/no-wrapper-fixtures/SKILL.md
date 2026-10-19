---
name: no-wrapper-fixtures
description: No wrapper or projection fixtures
---

# No wrapper or projection fixtures

- Do not write a fixture or helper whose body only calls one constructor or factory with arguments that all equal its defaults. Inline the call. Keep it only if it applies real, non-default configuration.
- Do not write a fixture that builds objects, calls selection or filter methods on them, and returns the projection. Put the projection call in the test body, or move it into production code that owns the concept.
