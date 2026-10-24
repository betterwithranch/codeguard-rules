---
name: one-concept-per-module
description: A module's public classes all belong to one concept; a second public class that is its own concept is a violation, whatever the module is named.
---

# One concept per module

A module holds one concept: its primary type, or one family of types, and the shapes
that belong to them.

The module's public classes are its module-level classes whose names don't start with
`_`, in any form: plain classes, dataclasses, pydantic models, attrs classes, enums,
`TypedDict`s, `NamedTuple`s, `Protocol`s, exceptions, Django models and DRF serializers.

A public class belongs to the module's concept when it is one of these:

- the primary type: the class the module is about;
- a member of one family: classes that share a base defined in the module (an exception
  hierarchy, the subclasses of one abstract base), or the variants of a union declared
  in the module, with the base or the union being the concept;
- a passive shape of the primary type: a class that only holds data (no methods beyond
  the ones its library generates, a `@property` over its own fields, or a validator)
  and that appears in the primary type's own fields or method signatures, as a
  parameter, result or field type, and in no other public class of the module.

A class with behavior of its own (methods that do work) is its own concept, even when
the primary type is its only caller or builds it in `__init__`. Constructing or using a
class doesn't make it part of the one that does.

## The test

For each public class in the file, ask: is it the primary type, a member of the
module's one family, or a passive shape of the primary type? Judge by the classes the
module defines, not by its file name: a well-named module with a second unrelated
class fails, and `enums.py` holding three unrelated enums fails.

Not a violation:

- a module with one public class and any number of functions and `_`-private classes;
- an exception family (`NotificationError` and its subclasses);
- a union family: the union's variants and the alias;
- a service with its request and result dataclasses that only its methods take and
  return;
- a nested class (`class Meta:` on a Django model, `class Config:`).

## Violation

A module that defines a public class outside its concept: a behavior-bearing class
beside the primary type (a `RetryBackoffPolicy` with a `delay()` method in the
`NotificationDispatcher` module), a class unrelated to the primary type
(`InvoiceTotals` in `notifications/dispatcher.py`), or two or more unrelated public
classes grouped by construct kind (`CarrierCode`, `RefundReason` and `InvoiceStatus` in
`enums.py`).
