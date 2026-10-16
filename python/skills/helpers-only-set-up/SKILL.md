---
name: helpers-only-set-up
description: Helpers set up; they never perform the act
---

# Helpers set up; they never perform the act

A test helper or fixture builds inputs, collaborators, and records. It must not take over the act the test verifies. Three forms cross the line:

- Computing a value production already computes (an id, key, hash, ordering) by calling the same builder or allocator. A helper named after one scenario or domain is a sign. Get the value from the production path, or mock at a higher seam so the test never has to predict it. If the value must appear in a mock, build it in the test body and bind it to a named variable.
- Ending by calling a method or reading an attribute on the object it just built, and returning that instead of the object: `return InvoiceMapper(rules).map(raw)`, `return build_runtime(...).context`. This applies even when the method is not the one under test. Calling methods while building (builder chains, constructors) is fine. Split into a helper that returns the built object and a separate action-named helper, or an inline line in the test.
- An action helper that takes a result, asserts on it, drives the next workflow step, and returns the new result. Inline the step in the test body. Simulate out-of-band actors (a queue worker, a callback) inline by reading the boundary fake and running the real component. Drop repeated assertions a unit test already owns.

Exception: calling a production function inside the expected value is fine when all hold: the value is a deterministic output field computed from other fields asserted in the same expected object; the code under test hands that computation to a collaborator; and that collaborator's function has its own test built another way.

Bad:

```python
def submit_and_resume(workflow, result):
    assert result.status == Status.WAITING
    return workflow.resume(result.job_id)
```

Good:

```python
result = workflow.resume(result.job_id)
```
