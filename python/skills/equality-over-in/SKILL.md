---
name: equality-over-in
description: Prefer == over in
---

# Prefer `==` over `in`

Use exact equality when the value is deterministic.

```python
assert result.name == "Invoice 42"
assert result.lines == [expected_line]
assert result.totals == {"net": 100, "tax": 20}
```

`in` is allowed only when all of these hold:

- The asserted fragment is exact and complete (a whole line, token, or value the code under test produces), not a loose substring.
- It sits inside a larger value whose content another component authors (a template, a loaded text file, a separate formatter). A unit that only joins sections does not own their content.
- Asserting the whole value with `==` would pin that other component's content.

Check: breaking the logic under test fails the assertion, and editing the unrelated component does not.
