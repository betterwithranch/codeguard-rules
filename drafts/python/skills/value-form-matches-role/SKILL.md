---
name: value-form-matches-role
description: A supplied value's form matches its role
---

# A supplied value's form matches its role

- Omit a value that is irrelevant to the case.
- Use a fixed literal when the code asserts or branches on that exact value.
- Use a real created record's id when the code reads, joins, or correlates on that id. Never pass a fresh `uuid4()` there.
