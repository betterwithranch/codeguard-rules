---
name: one-responsibility
description: Each function and class has one responsibility, whose job can be stated without "and"; a function doing a job's logic inline beside another job, a class serving two unrelated concerns, or a loop that works out each item's result and collects it is a violation.
---

# One responsibility

Each function and class has one responsibility, so each job can be named, called,
tested and changed on its own.

## Definitions

- A **job** is a step a caller could want by itself, with its own result: fetch a
  record, decide whether a rule holds, compute a value, format text, write a row, send
  a message, parse input.
- A function **coordinates** when its body only calls other functions, each doing one
  job, and passes results between them (`order = orders.get(id)`;
  `approved = is_refundable(order)`; `mailer.send(id, notice(approved))`). Running that
  sequence is one job, however many calls it makes. A body that also holds a job's own
  logic inline beside those calls (reading and parsing a file, filtering rows,
  computing a value, building text) is not a coordinator: the inline logic is one job
  and the calls are others.
- A **step written inline** is a job's own logic in the function body: the arithmetic,
  the conditions, the string building, the query, rather than a call to a function that
  does it.
- A **concern** is a body of rules, an outside system, or a data format whose change
  would force code to change: order placement, marketing email, warehouse restocking,
  the supplier's API, the CSV export layout. A method serves the concern whose rules it
  decides or whose collaborator it calls. Two concerns are related when one's methods
  call the other's, read its data, or feed it their results; then they are one
  responsibility.

## The test

For each function, method, class and loop the forms below describe, ask: can its job be
stated without "and", in the way the form describes? A coordinator's job is always
stated without "and": it runs one sequence.

### A function doing two jobs

For each function the change adds or edits, list the jobs its body does, whether
written inline or done by a call, and mark which are written inline.

Violation: a body doing two or more jobs with at least one written inline, so its
one-sentence description needs "and": `process_refund_request` that fetches the order,
works out inline whether it is refundable from its fields, and sends the email;
`import_line` that splits a CSV line into fields inline and queries the customer table
for the name it found; `import_customers` that reads and filters the CSV rows inline
and then calls the steps that convert and save them. Reported on the function.

Read these forms the same way:

- a coordinator that calls one function per job is one job;
- one job written inline with its own sub-steps is one job (computing a total from
  lines, then rounding it; building a dict of fields, then serializing it);
- a guard clause that rejects bad input (`if not lines: raise EmptyInvoice()`) is part
  of the job it guards;
- methods, `@property`, `@staticmethod`, `async def`, Django views and DRF actions,
  SQLAlchemy queries, pydantic validators and CLI commands alike: a Django view that
  builds a query inline and renders the totals inline does two jobs; one that calls a
  query function and a template does one;
- a function short enough for one line can still do two jobs
  (`return orders.get(id).delivered and orders.get(id).days_since <= WINDOW` fetches
  and decides inline).

### A class serving two concerns

For each class in the file, name the concern each method serves, from what it reads,
calls and decides.

Violation: a class whose methods split into two or more groups, each serving its own
concern with its own collaborators or data, where no method of one group calls, reads
from or feeds a method of another: a service that places orders and also sends
marketing campaigns through a mailer it uses for nothing else; a model or view that
serves its own data and also restocks a warehouse, exports a report in another system's
format, or syncs to an unrelated outside API. Reported on the class.

Size is not the test: a large class whose many methods serve one concern keeps the
rule, and a two-method class serving two unrelated concerns breaks it. One concern,
whatever the number of methods:

- a frozen dataclass, `NamedTuple`, attrs or pydantic value object whose methods read
  only its own fields, even across several topics (arithmetic, comparison, formatting
  of a `Money`);
- a pydantic model's validators and computed fields over its own fields;
- a Django or SQLAlchemy model's methods and properties over its own columns and
  relations, and a Django manager or repository whose queries all read one model;
- a DRF `ViewSet` or Django class-based view whose actions all serve one resource;
- a service or orchestrator whose methods carry out the steps of one workflow, calling
  each other or feeding each other's results, even through several collaborators;
- `__init__`, dunder methods, and properties that expose the class's own state.

### A loop that works out and collects each item's result

A loop is a `for` or `async for` statement. It accumulates when it adds each item's
result to a collection made for the loop: `results.append(x)`, `results.add(x)`,
`results.extend(xs)`, `results.insert(i, x)`, `results += [x]`. A per-item branch
chooses or computes an item's result from that item alone: an `if`/`elif`/`else`, a
`match`, a conditional expression (`-x if refund else x`), or a `continue` guard
followed by more branching. State between items is a value one iteration leaves for a
later one to read, other than the collection filled by plain appends: a running total
read into the result, a `seen` set checked before appending, the previous item, a
counter, reading the collection itself (`results[-1]`), or `break` on a condition.

Violation: a loop that accumulates a value its body chooses or computes through a
per-item branch, with no state between items, so the loop both works out each item's
result and collects the results:

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

The same holds for branches that assign a local appended after the `if`
(`label = "EXPRESS"` / `label = "STANDARD"`), a conditional expression inside the
appended value, and a `match` whose cases pick the value appended. Reported on the
`for` line.

Not a violation:

- one filtering `if` (or one `continue` guard) around a plain append of the item, or of
  one call on it, and nothing else branching;
- branches that add to different collections (`paid.append(o)` / `unpaid.append(o)`),
  partitioning the items rather than computing one result each;
- a running balance appended after each item, a `seen` set, a counter, a `break`, or a
  value read from the previous item: state between items;
- a loop whose branches do I/O or other effects per item (`mailer.send`,
  `session.add`, `logger.warning`) besides appending, so a comprehension couldn't hold
  it.

## Violation

Code in the file under review whose job needs "and" to state, in one of the forms
above: a function doing two or more jobs with at least one written inline, a class
whose methods serve two or more unrelated concerns, or a loop that works out each
item's result through a per-item branch and collects it, with no state between items.
