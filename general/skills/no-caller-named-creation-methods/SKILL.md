---
name: no-caller-named-creation-methods
description: A creation method is named for what it makes, never for who calls it; a creation method name the change adds or renames that names a screen, endpoint, client app, team, job or feature using its product is a violation.
---

# No Caller-Named Creation Methods

A creation method is named for what it makes, never for who calls it.

A creation method is a function or method whose job is to return a new product: an
alternative constructor, a method of a factory class, or a function, at module level or
in a class, whose name starts with create, make, build, new, for or from. Its product
is the new value it returns. What it makes is how its product differs from the type's
other products (the state, settings or contents it is given), or the input it is made
from.

A caller is something outside the creation method that uses its product: a screen,
endpoint, client app, team, job or feature.

## Violation

A creation method whose name the change adds or renames, when the name names a caller
instead of what it makes: `create_for_admin_dashboard`, `make_checkout_order`,
`for_mobile_app`.

Report it on the line that defines the name.

## Not a violation

- A creation method named for the difference in its product: `create_draft`.
- A creation method named for the input it is made from: `from_csv_row`.
- A creation method whose "for" names a value its product holds, not a caller:
  `for_currency`, which returns a product set to that currency.
- A creation method name with words that fit any code, or words false of its body.
  Separate rules judge those.

## Why

A creation method named for its caller says who uses it, not what it makes, so the next
caller that needs the same product can't find it, and the name goes stale when the
caller changes.

Source: Robert C. Martin, *Clean Code* (2008), chapter 2, "Use Intention-Revealing
Names".
