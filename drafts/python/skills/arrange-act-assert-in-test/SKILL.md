---
name: arrange-act-assert-in-test
description: Arrange, act, and assert stay in the test body
---

# Arrange, act, and assert stay in the test body

A violation is:

- A test parameter that is the object the test acts on. Building it in the test body, directly or through a helper call such as `make_mapper()`, is not a violation.
- A fixture that performs arrange actions: starting a workflow or job, or making the calls that drive the system into its precondition. This holds even when the fixture returns a real object.
- A fixture that performs the act.
- A setup fixture used by only one test.
- A setup fixture that sets up one scenario rather than ambient environment (workers, queues, feature flags, registries).
