---
name: type-args-in-init-subclass
description: Read type arguments in __init_subclass__
---

# Read type arguments in `__init_subclass__`

When a generic base needs the concrete type argument a subclass binds, capture it once in `__init_subclass__` with `get_origin` and `get_args` over `__orig_bases__`. Do not require each subclass to restate the type as a separate attribute.

```python
class Repository(Generic[TRecord]):
    record_type: type[TRecord]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in cls.__orig_bases__:
            if get_origin(base) is Repository and get_args(base):
                cls.record_type = get_args(base)[0]
                return
```
