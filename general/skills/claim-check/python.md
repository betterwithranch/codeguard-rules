# In Python

Boundaries are Celery's `.delay`, `.apply_async`, `.s` and `.si`, RQ's `enqueue`,
Dramatiq's `.send`, a broker client's `publish`, a multiprocessing queue's `put`, a
process pool's `submit`, and Temporal calls that start a workflow or run an activity.
Tasks are functions decorated `@shared_task`, `@app.task`, `@dramatiq.actor`,
`@activity.defn` or `@workflow.run`. A thread pool's `submit`, `queue.Queue` and
`asyncio.Queue` are not boundaries.

Stored records are Django and SQLAlchemy model instances, and documents or entities a
repository loads. Whole-record copies are `model_to_dict(order)`, `order.model_dump()`,
`asdict(order)`, `vars(order)`, `order.__dict__`, and a serializer's `.data`.

## Violation

- `send_receipt.delay(order)`, where `order` is an `Order` model instance.
- `reindex.delay(model_to_dict(product))`.
- `@shared_task def send_receipt(order: Order)`.

## Not a violation

- `send_receipt.delay(order.id)`, with the task calling `Order.objects.get(id=order_id)`.
- `publisher.publish("order.placed", {"order_id": order.id, "total_cents": order.total_cents})`.
- `thread_pool.submit(render, order)`.
