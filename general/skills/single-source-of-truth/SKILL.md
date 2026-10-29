---
name: single-source-of-truth
description: A class doesn't store a value it can derive from one other value it holds; a field that repeats what another field, or a field of an object the class holds, already says is a violation.
---

# Single Source of Truth

A class doesn't store a value it can derive from one other value it holds.

A value is derived from another when one rule computes it from that value alone, with
nothing else: whether an order is shipped from its shipped time, how many items a cart
has from its list of items, a customer's email from the customer object the shipment
holds, whether a payment is paid from its status.

The other value is a field of the same class, or a field of an object the class holds
in one of its fields.

## Violation

Code the change adds or edits that gives a class a field derived from one other value
it holds: the field's declaration, or an assignment that sets it on the instance, such
as a constructor setting both, or a method that updates the field to keep it in step
with its source.

Report it on the derived field's declaration, or its first assignment where the class
declares no fields.

## Not a violation

- A property or method that computes the value from its source each time it is read.
- A field holding a fact of its own that no other field holds: whether an order is a
  gift beside when it shipped.
- A value worked out from several fields or from data outside the class, such as a total
  from a list of lines and a tax rate.
- A value recorded at a moment that its source may later stop matching, kept as history:
  the price paid beside the product, the address an order shipped to beside the
  customer.
- A key or identifier of an object the class doesn't also hold, and a database model's
  foreign key column beside its relationship to the same row.
- A different class that copies both values, such as a response or read model built
  from a record.

## Why

Two fields that must agree drift apart: the next change sets one and forgets the other,
and readers see an order that is shipped with no ship time, or a count that doesn't
match its items. Computing the value from its one source leaves nothing to keep in
step.

Source: single source of truth; database normalization (E. F. Codd, 1970s), which keeps
each fact in one place so it can't be updated in one row and not another.
