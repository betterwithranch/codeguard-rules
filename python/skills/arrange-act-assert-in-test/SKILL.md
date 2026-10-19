---
name: arrange-act-assert-in-test
description: Arrange, act, and assert stay in the test body
---

# Arrange, act, and assert stay in the test body

- Construct the system under test in the test body. Fixtures supply its collaborators and inputs. A test parameter that is the object the test acts on is a violation.
- A fixture supplies a thing. It must not perform arrange actions: starting a workflow or job, advancing a clock (`sleep`, `freeze_time` ticks, skips), or making the calls that drive the system into its precondition. It must never perform the act. This holds even when the fixture returns a real object.
- A setup fixture used by only one test hides that test's arrange. Inline it.
- A setup fixture is allowed only when it is shared by more than one test and sets up ambient environment (workers, queues, feature flags, registries), not one scenario.
- An arrange too large to read inline is a design problem in the code under test (a missing seam, an uninjected collaborator, too many responsibilities). Do not hide it in a fixture.
