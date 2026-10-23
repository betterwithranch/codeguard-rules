---
name: no-test-setup-bundles
description: Test code defines no type whose only job is to carry the objects a helper or fixture built
---

# No setup bundle types in tests

Test code hands each object it builds to the test on its own, not packed into a type
made for carrying them.

A setup bundle is a type defined in test code that has no behavior of its own and whose
fields hold objects a helper or fixture built (records, services, fakes, clients), so
that tests reach them as `setup.cart` or `resources.customer`. It may be a dataclass, a
`NamedTuple`, a `TypedDict`, an attrs or pydantic class, a plain class whose `__init__`
only stores its arguments, or a `SimpleNamespace` or `namedtuple(...)` built on the fly.

## The test

For each type defined in test code, and each `SimpleNamespace` or `namedtuple` a helper
or fixture builds, ask: is its only job to group objects a helper or fixture built, so
tests can unpack them?

Not a violation:

- a fake, stub or spy with behavior: `class FakeLedger` with `record()` and `entries`;
- a test driver whose methods act: a page object, a `class CheckoutDriver` with
  `add_item()` and `pay()`;
- a parametrize case type whose fields hold literal inputs and expected values:
  `@dataclass class Case: text: str; expected_total: int`.

A setup bundle:

- `@dataclass class CheckoutSetup: customer: Customer; cart: Cart`, returned by
  `make_checkout_setup()`;
- `class OrderResources(NamedTuple): order: Order; service: OrderService`;
- `return SimpleNamespace(customer=customer, cart=cart)` from a fixture.

## Violation

A setup bundle defined or built in test code.
