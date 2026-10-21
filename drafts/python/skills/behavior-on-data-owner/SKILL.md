---
name: behavior-on-data-owner
description: Behavior lives on the type whose data it reads
---

# Behavior lives on the type whose data it reads

A `@staticmethod`, a method that ignores `self`, or a free function whose body reads only one parameter's own fields belongs on that parameter's type. This covers sort keys, formatted lines, derived properties, and comparisons. Where the helper currently lives does not matter.

Bad:

```python
class InvoiceSummaryComposer:
    def _sort_key(self, line: InvoiceLine) -> tuple[str, int]:
        return (line.sku.casefold(), line.position)
```

Good:

```python
@dataclass(frozen=True)
class InvoiceLine:
    sku: str
    position: int

    def __lt__(self, other: "InvoiceLine") -> bool:
        return (self.sku.casefold(), self.position) < (other.sku.casefold(), other.position)
```

- Behavior that reads only the type's own fields is intrinsic. Keep it on the type.
- Behavior that queries or traverses other types is a service. Extract it to a named domain service.
- Rendering for another subsystem belongs to that subsystem's formatter, not to the data type.
- If a formatter type already owns a rendering, a second site must call it, not re-derive the same output inline. If the formatter lacks a needed variant, extend the formatter.
