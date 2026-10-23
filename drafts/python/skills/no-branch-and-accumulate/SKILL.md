---
name: no-branch-and-accumulate
description: No loop that branches to work out each item's result and appends it to a collection, when no state passes from one item to the next
---

# No branch-and-accumulate loops

Working out one item's result is kept apart from collecting the results, so the
per-item rule can be named, tested and reused.

## Definitions

- A **loop** is a `for` or `async for` statement.
- An **accumulation** adds each item's result to a collection made for the loop:
  `results.append(x)`, `results.add(x)`, `results.extend(xs)`, `results.insert(i, x)`,
  `results += [x]`.
- A **per-item branch** chooses or computes an item's result from that item alone: an
  `if`/`elif`/`else`, a `match`, a conditional expression (`-x if refund else x`), or a
  `continue` guard followed by more branching.
- **State between items** is a value one iteration leaves for a later one to read, other
  than the collection being filled by plain appends: a running total read into the
  result, a `seen` set checked before appending, the previous item, a counter, reading
  the collection itself (`results[-1]`), or `break` on a condition.

## The test

For each loop in the file under review that accumulates, ask: does the loop body use a
per-item branch to choose or compute the value it accumulates, with no state between
items?

Yes: violation. No: not a violation.

The test reads these forms the same way:

- one filtering `if` (or one `continue` guard) around a plain append of the item, or of
  one call on it, and nothing else branching: not a violation;
- branches that assign a local (`label = "EXPRESS"` / `label = "STANDARD"`) appended
  after the `if`: violation;
- a `continue` guard and then an `if`/`else` that appends different values: violation;
- a conditional expression inside the appended value
  (`amounts.append(-line.amount if line.is_refund else line.amount)`): violation;
- a `match` on the item whose cases pick the value appended: violation;
- branches that add to different collections (`paid.append(o)` / `unpaid.append(o)`)
  partition the items rather than compute one result each: not a violation;
- a running balance appended after each item, a `seen` set, a counter, a `break`, or a
  value read from the previous item: state between items, not a violation;
- a loop whose branches do I/O or other effects per item (`mailer.send`, `session.add`,
  `logger.warning`) besides appending, so a comprehension couldn't hold it: not a
  violation.

## Violation

A loop in the file under review that accumulates a value its body chooses or computes
through a per-item branch, with no state passing between items:

```python
amounts = []
for line in lines:
    if line.is_voided:
        continue
    if line.is_refund:
        amounts.append(-line.amount)
    else:
        amounts.append(line.amount)
```

Report the violation on the `for` line.
