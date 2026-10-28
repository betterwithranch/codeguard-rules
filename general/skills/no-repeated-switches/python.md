# In Python

A switch is an `if`/`elif` chain of `isinstance` or `issubclass` checks or of
`type(x) is` comparisons; a `match` with class patterns (`case Wire():`) or with an
enum's members or a tag's values as patterns; an `if`/`elif` chain comparing an enum
member or a tag field (`x.kind == Kind.WIRE`, `x.kind == "wire"`); and a `dict` keyed by
classes, `type(x)`, enum members or tag values that a function indexes with the value's
kind.

A `match` or `if`/`elif` chain is checked complete when its last branch passes the value
to `typing.assert_never` (`case _: assert_never(x)`, `else: assert_never(x)`), and the
project runs pyright or basedpyright, which reject the call if any kind can reach it. A
`case _:` or `else:` that returns, raises or logs for whatever is left, and a chain that
falls off the end of the function, are not. No `dict` is checked complete: its type
doesn't demand a key per kind.

## Violation

- A module function gaining an `isinstance` chain over the same family of classes that
  another function's `isinstance` chain or `match` in the module already chooses among,
  ending in an `else` that returns a fallback.
- A `match` on an enum field with a `case _:` default, beside another such `match` on the
  same field.
- A dispatch `dict` keyed by the same enum members or classes as another `dict` or
  switch in the file.

## Not a violation

- A family of classes, dataclasses or pydantic models that each define the method the
  code calls.
- Several `match` statements on one enum or union, each ending in
  `case _: assert_never(x)`.
- A pydantic discriminated union, or a function reading a payload's `"type"` key, that
  builds the matching model.
- A single `isinstance` check that rejects or narrows one type, such as in a validator or
  `__eq__`, and `except` clauses.
