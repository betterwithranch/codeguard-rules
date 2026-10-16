---
name: real-test-data
description: Use real data, real parents, and real ids
---

# Use real data, real parents, and real ids

- Do not replace real inputs with empty or dummy data to get past a failure. That failure is a production bug. Empty inputs are allowed only in wiring tests where the code under test provably does not use them.
- When production has one creator for a record (a service, a planner, a repository `create`), seed test data through that creator or a thin helper that calls it. Do not hand-write a parallel insert path in shared fixtures.
- Do not give a child record a fresh `uuid4()` foreign id that points at a parent that was never created. Create the parent.
- Do not put a fixed UUID or other id constant in a fixture unless the code under test correlates on that id and the matching object exists or is asserted. If the id is only there because a wide setup object requires it, narrow the setup to the real inputs.
