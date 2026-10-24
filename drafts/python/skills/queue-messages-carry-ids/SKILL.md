---
name: queue-messages-carry-ids
description: Handing a stored record, or a whole-record dump of it, across a queue, task or workflow boundary (as a task argument or a task function's parameter) instead of its id is a violation.
---

# Queue messages carry ids

Work handed across a queue or workflow boundary names stored records by id, so the
receiver reads the current record instead of a stale copy.

A stored record is an object the program saves and loads again by id: a Django or
SQLAlchemy model instance, a document from a document store, or a domain object a
repository returns. A whole-record dump is a copy of all its fields: `model_to_dict(order)`,
`order.model_dump()`, `asdict(order)`, `vars(order)`, `order.__dict__`, or a serializer's
`.data` for it. A boundary is a call that serializes its arguments and runs the
receiver later or in another process: Celery's `.delay`, `.apply_async`, `.s` and
`.si`, RQ's `enqueue`, Dramatiq's `.send`, a broker client's `publish`, a
multiprocessing queue's `put` or a process pool's `submit`, and Temporal or other
workflow calls that start a workflow or run an activity. A task function is the
function such a call runs: one decorated `@shared_task`, `@app.task`, `@dramatiq.actor`,
`@activity.defn` or `@workflow.run`.

## The test

For each argument passed across a boundary in the file, and each parameter of a task
function defined in it, ask: is it a stored record, or a whole-record dump of one?

Yes is a violation. No is not: an id or key (`order.id`, `str(order.pk)`), a value that
is not a stored record (a date, an amount, a list of ids, a computed result), or a
message built from chosen fields that states an event (`{"order_id": order.id,
"total_cents": order.total_cents}`).

In-process hand-offs do not serialize and are not boundaries: an `asyncio.Queue`, a
`queue.Queue` between threads, a thread pool's `submit`, a direct call.

## Violation

A stored record, or a whole-record dump of one, passed across a boundary or taken as a
task function's parameter in the file under review.
