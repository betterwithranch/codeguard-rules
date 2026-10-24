---
name: one-responsibility-per-type
description: A class whose methods serve two or more unrelated concerns, so a change to one concern touches a class that also serves another, is a violation.
---

# One responsibility per type

Every method of a type serves the same concern, so a change to one concern never touches
a type that also serves another.

A concern is a body of rules, an outside system, or a data format whose change would
force code to change: order placement, marketing email, warehouse restocking, the
supplier's API, the CSV export layout. A method serves the concern whose rules it
decides or whose collaborator it calls. Two concerns are related when one's methods
call the other's, read its data, or feed it their results; then a change to one can
require a change to the other, and they are one responsibility.

## The test

For each class in the file, name the concern each method serves, from what the method
reads, calls and decides. Then ask: do the methods split into two or more groups, where
each group serves its own concern, uses its own collaborators or data, and no method of
one group calls, reads from or feeds a method of another?

Yes is a violation. No, because every method serves one concern or the groups are
related, is not. Size is not the test: a large class whose many methods serve one
concern keeps the rule, and a two-method class serving two unrelated concerns breaks
it.

One concern, whatever the number of methods:

- a frozen dataclass, `NamedTuple`, attrs or pydantic value object whose methods read
  only its own fields, even when they cover several topics (arithmetic, comparison,
  formatting of a `Money`);
- a pydantic model's validators and computed fields over its own fields;
- a Django or SQLAlchemy model's methods and properties over its own columns and
  relations, and a Django manager or repository whose queries all read one model;
- a DRF `ViewSet` or Django class-based view whose actions all serve one resource;
- a service or orchestrator whose methods carry out the steps of one workflow, calling
  each other or feeding each other's results, even through several collaborators;
- `__init__`, dunder methods, and properties that expose the class's own state.

Two concerns:

- a service that places orders and also sends marketing campaigns through a mailer it
  uses for nothing else;
- a model or view that serves its own data and also restocks a warehouse, exports a
  report in another system's format, or syncs to an unrelated outside API.

## Violation

A class in the file under review with two or more groups of methods that serve
unrelated concerns: no method of one group calls, reads from or feeds a method of
another, and each group uses collaborators or data the other doesn't.
