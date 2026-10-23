---
name: builder-names-step-builders
description: A class named `...Builder` that makes its product from one call's arguments, rather than assembling it through several calls on the builder, is a violation.
---

# Builder names a step-by-step builder

The name `Builder` is kept for a type that assembles its product step by step.

A step-by-step builder is one that callers use through several calls on the same
instance: each call sets or adds a part of the product (methods that store parts on the
instance, often returning `self` so the calls chain), and a separate final call
(`build()`) returns the product made from those parts. A one-shot maker produces its
product from the arguments of a single call: a `build(order_id, total)` method, a
`build()` that only uses what the constructor took, or a static or class method.

## The test

For each class in the file whose name ends in `Builder`, ask: does it have methods that
store parts of the product on the instance, called before a separate method returns the
product?

Yes is not a violation, whether the part methods return `self` or nothing, and whether
the parts are attributes, a list of lines, or a dataclass's fields. No is a violation:
the class makes its product in one call, under any method name (`build`, `create`,
`make`, `__call__`).

## Violation

A class in the file under review whose name ends in `Builder` and that makes its
product from the arguments of one call, with no methods that add parts to the instance
before a separate call returns the product.
