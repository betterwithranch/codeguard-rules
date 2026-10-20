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

`in` on a string is allowed only when both of these hold in the test itself:

- The test supplies or loads another component's content and passes it to the code under test, such as a template from `load_template` or a text file it reads.
- The asserted fragment is a whole line the code under test inserts into that content.

Any other `in` on a string is a violation, including a short value inside a result the code under test builds alone, such as `"7" in order_label(order)`. Assert the whole result with `==`.
