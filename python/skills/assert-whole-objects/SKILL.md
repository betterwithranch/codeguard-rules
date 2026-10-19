---
name: assert-whole-objects
description: Assert whole result objects
---

# Assert whole result objects

Build the expected object and compare once: `assert result == Invoice(number="42", total=120)`. Do not assert one field and leave the siblings unchecked.

- When the result type has `__eq__`, separate `==` lines for each field are a violation even if they cover every field today. They miss fields added later.
- A bare `len()` check, or `len(x) == 1` followed by checks on `x[0]`, is incomplete. Assert the full collection: `assert [i.sku for i in items] == ["A1", "B2"]`.
- Field-by-field checks are correct only when equality is impossible (no `__eq__`, generated keys, timestamps) or the result is a scalar. Then assert every observable field.
