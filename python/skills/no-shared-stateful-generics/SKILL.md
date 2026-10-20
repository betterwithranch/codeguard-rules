---
name: no-shared-stateful-generics
description: No shared instances of stateful classes
---

# No shared instances of stateful classes

If a class accumulates state in its methods (for example, collecting issues), do not share one module-level instance. Create a fresh instance per use, such as through a factory function.

Bad:

```python
validator = OrderValidator(region="eu")
```

Good:

```python
def create_order_validator() -> OrderValidator:
    return OrderValidator(region="eu")
```
