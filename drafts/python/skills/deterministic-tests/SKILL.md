---
name: deterministic-tests
description: Tests are deterministic
---

# Tests are deterministic

A test must not pass or fail based on timing, ordering, or environment. Every assertion compares against a known, fully predictable value. Control unpredictable values (ids, timestamps, random numbers) with a fixture or a frozen clock; do not ignore them. A containment check (`in`, `<=`) written because the full result is unknown is a sign to pin the value instead.
