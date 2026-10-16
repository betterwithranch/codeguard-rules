---
name: typevar-bound-by-class
description: Every TypeVar in an annotation is bound by the class
---

# Every TypeVar in an annotation is bound by the class

A TypeVar used in a class attribute annotation must appear in that class's `Generic[...]` parameters. If the class does not need the parameter, use a concrete type or `Any` in that position.

Bad:

```python
class OrderHolder(Generic[TOrder]):
    pricer: Pricer[TOrder, TCurrency]
```

Good:

```python
class OrderHolder(Generic[TOrder, TCurrency]):
    pricer: Pricer[TOrder, TCurrency]
```
