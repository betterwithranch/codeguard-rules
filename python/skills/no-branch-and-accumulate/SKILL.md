---
name: no-branch-and-accumulate
description: No branch-and-accumulate loops
---

# No branch-and-accumulate loops

A loop that branches to compute a per-item result and append it to a shared list mixes mapping one item with iterating. Extract the body to a function that returns one result (each `continue` becomes `return`) and use a comprehension.

Report the violation on the `for` line, not on the line that creates the list.

Not a violation: a single filtering guard, or a loop with real cross-item state (running totals, dedup sets).
