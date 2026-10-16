---
name: function-has-owner
description: Every loose function has an owner
---

# Every loose function has an owner

A public module-level function needs a reason not to be a method. Place it by what it does:

- Constructs one return type: a `classmethod` or factory method on that type.
- Interprets one instance's own data: an instance method on that type.
- Coordinates several peer types: a small domain service named after the operation.
- Formats or adapts for another subsystem: a type named after the target, such as `InvoicePresenter` or `ShipmentComposer`.

Keep it module-level only when no type would be more coherent with it as a method.
