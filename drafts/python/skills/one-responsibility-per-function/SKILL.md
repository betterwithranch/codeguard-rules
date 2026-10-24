---
name: one-responsibility-per-function
description: A function either does one job's logic or coordinates calls to functions that each do one, never a job's logic alongside other jobs
---

# One responsibility per function

Each function does one job, so each job can be named, called and changed on its own.

## Definitions

- A **job** is a step a caller could want by itself, with its own result: fetch a
  record, decide whether a rule holds, compute a value, format text, write a row, send
  a message, parse input.
- A function **coordinates** when its body only calls other functions, each doing one
  job, and passes results between them (`order = orders.get(id)`;
  `approved = is_refundable(order)`; `mailer.send(id, notice(approved))`). Coordinating
  calls is one job: running that sequence.
- A **step written inline** is a job's own logic in the function body: the arithmetic,
  the conditions, the string building, the query, rather than a call to a function that
  does it.

## The test

For each function the change adds or edits, list the jobs its body does, whether written
inline or done by a call, and mark which are written inline. Ask: does the body do two
or more jobs with at least one of them written inline, so its one-sentence description
needs "and" (fetches the order **and** decides whether it is refundable; parses the line
**and** looks up the customer)?

No (one job, or only calls to functions that each do one): not a violation.
Yes: violation.

The test reads these forms the same way:

- a coordinator that calls one function per job is one job, however many calls it makes;
- one job written inline with its own sub-steps is one job (computing a total from
  lines, then rounding it; building a dict of fields, then serializing it);
- a guard clause that rejects bad input (`if not lines: raise EmptyInvoice()`) is part
  of the job it guards;
- methods, `@property`, `@staticmethod`, `async def`, Django views and DRF actions,
  SQLAlchemy queries, pydantic validators and CLI commands are read the same way: a
  Django view that builds a query inline **and** renders the totals inline does two
  jobs; one that calls a query function and a template does one;
- a function short enough for one line can still do two jobs
  (`return orders.get(id).delivered and orders.get(id).days_since <= WINDOW` fetches and
  decides inline).

## Violation

A function added or edited in the file under review that does two or more jobs, at least
one written inline: `process_refund_request` that fetches the order, works out inline
whether it is refundable from its fields, and sends the email; `import_line` that splits
a CSV line into fields inline and queries the customer table for the name it found.
