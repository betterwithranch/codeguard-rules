---
name: test-has-signal
description: Every test has signal
---

# Every test has signal

A test must fail for some plausible bug in the project's own code. Ask: if this went red, would you fix the code or the test? If the test, delete it. Three defects have no signal:

- Tautology: the expected value is copied from the code under test's own declarations, so only editing the declaration can break it. Example: asserting a model's declared config equals a hand-written copy of the same config.
- Framework behavior: the test checks what the language, standard library, or a library guarantees, with no decision of the project under test. Examples: a field defaults to its declared default; a field without a validator accepts any value of its type; a model without custom serializers round-trips; every enum member is accepted.
- Redundancy: another test already covers the behavior. Examples: tests of a subclass that adds no logic; `isinstance` or protocol-conformance tests when other tests already use the object; tests that stub a collaborator and assert its stubbed output passes through unchanged.

Not tautology: a test of a constraint that answers to something outside the declaration. A test that a 0-100 percentage field rejects 150 has signal. A test that a label equals `"Frequency"` does not.

Do not find an item by a field value and then assert that same field. Assert the set of keys present, or find by one field and assert a different one.

Bad:

```python
assert next(i for i in result.items if i.sku == "A1").sku == "A1"
```

Good:

```python
assert {i.sku for i in result.items} == {"A1", "B2"}
```
