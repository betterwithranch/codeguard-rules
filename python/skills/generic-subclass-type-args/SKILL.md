---
name: generic-subclass-type-args
description: Pass type arguments through subclasses
---

# Pass type arguments through subclasses

A subclass of a generic class either binds concrete type arguments or keeps them generic by re-declaring `Generic` with the same parameters. It never drops them.

```python
class Ledger(Generic[TEntry, TAccount]): ...

class InvoiceLedger(Ledger[InvoiceEntry, CustomerAccount]): ...

class AuditedLedger(Ledger[TEntry, TAccount], Generic[TEntry, TAccount]): ...
```
