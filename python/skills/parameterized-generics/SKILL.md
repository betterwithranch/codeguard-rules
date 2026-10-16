---
name: parameterized-generics
description: Parameterize generic annotations
---

# Parameterize generic annotations

Do not leave a generic type bare on a class attribute. A bare `Pricer` is silently `Pricer[Any, Any]`.

Bad:

```python
class Checkout:
    pricer: Pricer
```

Good:

```python
class Checkout(Generic[TOrder]):
    pricer: Pricer[TOrder, Any]
```
