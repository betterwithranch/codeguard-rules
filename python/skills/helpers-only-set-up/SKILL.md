---
name: helpers-only-set-up
description: Helpers set up; they never perform the act
---

# Helpers set up; they never perform the act

A test helper or fixture builds inputs, collaborators, and records. A violation is a helper or fixture that takes over the act the test verifies:

- Computing a value production already computes (an id, key, hash, ordering) by calling the same builder or allocator. A helper named after one scenario or domain is a sign.
- Ending by calling a method or reading an attribute on the object it just built, and returning that instead of the object: `return InvoiceMapper(rules).map(raw)`, `return build_runtime(...).context`. This applies even when the method is not the one under test. Calling methods while building (builder chains, constructors) is not a violation.

Not a violation: calling a production function inside the expected value when all hold: the value is a deterministic output field computed from other fields asserted in the same expected object; the code under test hands that computation to a collaborator; and that collaborator's function has its own test built another way.
