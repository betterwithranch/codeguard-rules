---
name: no-anonymous-tuples
description: No anonymous tuples or dicts for concepts
---

# No anonymous tuples or dicts for concepts

- A method returning a `tuple` of answers to different questions does too much. Return a named type, or return the fetched data and let callers ask each question separately.
- A helper whose whole body is `return {...}` or `return (...)` packing its own arguments under the same names is not an abstraction. Inline the literal, or define a named type if the shape recurs and means something.
- A single-call-site function whose whole body is `[f(x) for x in xs]` over an already-named `f` should be inlined. Keep it if it filters, sorts, deduplicates, handles errors, or is used at many sites.

Bad:

```python
def _evaluate_order(self, order_id: str) -> tuple[str | None, bool]:
    order = self._fetch(order_id)
    return self._rejection_reason(order), bool(order.holds)
```

Good:

```python
@dataclass(frozen=True)
class OrderReview:
    rejection_reason: str | None
    is_on_hold: bool
```
