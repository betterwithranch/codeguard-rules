---
name: configure-shared-fakes
description: Extend shared fakes by configuration
---

# Extend shared fakes by configuration

A shared fake stands in for one layer. Configure it and assert on its in-layer state in the test body. Do not subclass a shared fake to override a method so that the override asserts, or queries a different subsystem. Signs: an overridden method containing `assert`, a database query, or a list that exists only to record that the override ran. A subclass that only configures the fake (canned responses, queue setup) is fine.

Bad:

```python
class CheckingFakeQueue(FakeQueue):
    def enqueue(self, queue_name, message):
        assert self._db.count_orders(message["order_id"]) == 1
        return super().enqueue(queue_name, message)
```

Good:

```python
queue = FakeQueue()
OrderSubmitter(queue).submit(order)
assert [m.body for m in queue.drain("orders")] == [{"order_id": order.id}]
```
