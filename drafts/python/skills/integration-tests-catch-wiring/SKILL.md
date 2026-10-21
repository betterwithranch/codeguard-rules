---
name: integration-tests-catch-wiring
description: Integration tests catch a wiring bug
---

# Integration tests catch a wiring bug

An integration or end-to-end test must catch a bug no unit test on either side of the seam can: a key two components must agree on, a reference one side must register, a step order the pipeline must keep. Running one more real type through already-tested generic code is a replay, not integration signal. A test under an integration or end-to-end path that calls one function or class and crosses no seam is a violation, whatever other tests exist. Move it to the unit tests. Needing to normalize framework noise out of the result is a sign the test sits at the wrong level.
