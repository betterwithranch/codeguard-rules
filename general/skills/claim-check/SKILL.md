---
name: claim-check
description: A stored record crosses a task or queue boundary as its identity; passing a stored record, or a copy of all its fields, to work that runs later or in another process is a violation.
---

# Claim Check

A stored record crosses a task or queue boundary as its identity.

A boundary is a call that serializes its arguments and runs the work later or in
another process: enqueuing a background job or task, publishing to a message broker,
starting a workflow or activity, putting onto a queue another process reads. A task is
the function such a call runs. Handing work to a thread, or to a queue between threads
of one process, is not a boundary: nothing is serialized.

A stored record is an object the program saves and loads again by its id: a database
model instance, a document from a document store, an entity a repository returns. A
whole-record copy is all its fields copied into a dictionary or plain object.

## Violation

Code the change adds or edits that sends a stored record across a boundary instead of
its id:

- a call that passes a stored record, or a whole-record copy of one, to a task, job,
  message or workflow;
- a task the change defines that takes a stored record, or a whole-record copy of one,
  as a parameter.

Report it on the argument that carries the record, or on the task's parameter.

## Not a violation

- Passing the record's id or key, and having the task load the record.
- A value that is not a stored record: a date, an amount, a list of ids, a computed
  result, a file path.
- An event message built from chosen fields that states what happened, such as an order
  id and the total it was placed for.
- Handing a record to a thread or to an in-process queue.

## Why

The task runs later, from a copy made when it was queued. By then the record may have
changed or been deleted, and the task acts on the stale copy: it emails an old address,
or charges an order that was cancelled. A whole record can also be large, or fail to
serialize. Passing the id lets the task load the record as it is when it runs.

Source: the claim check pattern (Gregor Hohpe and Bobby Woolf, *Enterprise Integration
Patterns*, 2003); Celery's task guidance and Sidekiq's best practices, which both say to
pass ids, not database objects.
