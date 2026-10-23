---
name: no-unpacked-argument-groups
description: Code does not build an object only to take its fields back out as the arguments of one call; an argument group is handed whole to the callee or not built.
---

# No unpacked argument groups

An object built to group a call's arguments is passed to the callee whole, never taken
apart again at the call that consumes it.

An argument group is an object of a class the program declares only to carry values
together: a dataclass, attrs class, pydantic model, `NamedTuple` or `TypedDict`, or a
plain class whose `__init__` only stores its parameters. Unpacking it is reading its
fields back out as the arguments of a call: as attributes (`build_quote(args.cart,
args.region)`, `build_quote(cart=args.cart)`), or by splatting a dump of it
(`build_quote(**asdict(args))`, `*astuple(args)`, `**args.model_dump()`, `**vars(args)`,
`**args._asdict()`).

The group's class is declared in the file under review or a file it imports; read it
there to see what it holds.

## The test

For each call that takes its arguments from an object's fields, ask two questions:

1. Was the object built in the same function, from values that function already had,
   and is it an argument group (by the definition above)?
2. Are reads that feed this call, or calls like it, the only uses of the object: it is
   not passed whole to any call, returned, yielded, stored on `self` or in a collection,
   and none of its methods are called?

A violation needs yes to both.

## Violation

A function that builds an argument group and then only unpacks it into a call's
arguments:

```python
def quote(cart: Cart, region: Region) -> Quote:
    args = QuoteArgs(cart=cart, region=region)
    return build_quote(args.cart, args.region)
```

`build_quote(**asdict(QuoteArgs(cart=cart, region=region)))` is the same violation in
one expression.

Not a violation:

- an argument group handed whole to the callee, which reads its fields itself:
  `QuoteFactory().create(QuoteParams(cart=cart, region=region))`;
- an object the function received as a parameter or got from another call, whose fields
  it passes on (`ship(order.id, order.address)`);
- an object that is also used whole, as listed in question 2: returned, stored, logged
  as one value, or passed to another call;
- an object whose construction does work beyond storing values: it validates, converts
  or defaults them (a pydantic model that parses strings into dates, a dataclass with a
  `__post_init__` that normalizes), so its fields differ from the values it was given;
- a splat of a dict that is not a dump of an argument group (`**headers_for(payload)`,
  `**kwargs`).
