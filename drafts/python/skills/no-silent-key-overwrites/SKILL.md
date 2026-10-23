---
name: no-silent-key-overwrites
description: A mapping built from a collection, keyed by a value two items can share, that silently keeps only one item per key is a violation.
---

# No silent key overwrites

A mapping built from many items keeps every item, or says which one it keeps, and never
drops the others silently.

A mapping build is code that fills a dict from a collection: `index[key] = item` in a
`for` or `while` loop, a dict comprehension, `dict(...)` over pairs or `zip`,
`setdefault(key, item)`, or `update({key: item})` in a loop. Its key is unique when no
two items can have it: the items' own id or primary key, a field the model declares
unique, the keys of another mapping, an `enumerate` index. A key two items can share is
anything else: a foreign key (`order.customer_id`), a status, a category, a date, a
name. A build keeps one item per key when a later item replaces an earlier one
(assignment, comprehension, `dict()`, `update`) or an earlier one blocks a later one
(`setdefault` with the item itself).

## The test

For each mapping build in the file, ask: can two items produce the same key, with the
build keeping only one of them, and nothing in the code choosing which one or noticing
the duplicate?

Yes is a violation. No is not, because:

- the key is unique;
- every item is kept: grouped into lists (`setdefault(key, []).append(item)`,
  `defaultdict(list)`), or merged (`totals[key] = totals.get(key, 0) + item.cents`);
- a duplicate raises (`if key in index: raise DuplicateKey(key)`);
- the code chooses the item kept: iterating items sorted by the field that decides
  (`for event in sorted(events, key=lambda e: e.at)` to keep the latest), or comparing
  before replacing (`if event.at > latest[key].at`).

## Violation

A mapping build in the file under review keyed by a value two items can share, which
keeps one item per key without choosing which or detecting the duplicate:
`{order.customer_id: order for order in orders}`.
