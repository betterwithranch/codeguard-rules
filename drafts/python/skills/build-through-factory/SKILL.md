---
name: build-through-factory
description: Test code gets an object a production factory builds by calling that factory, never by assembling the object by hand
---

# Build through the production factory

When production code has a factory for an object, tests get that object from the
factory, so they exercise the same assembly production runs.

A production factory is application code that builds an object: a function, a
classmethod or a builder that assembles a graph of collaborators
(`build_shipment_service(carrier=...)`, `ShipmentService.from_settings(settings)`), or
derives an object from an input (`invoice_from_order(order)`). Hand assembly is test
code, in a helper, a fixture or a test body, that calls the factory's output type's
constructor with the collaborators the factory would create or the values it would
derive.

## The test

For each object test code builds by calling a constructor with collaborators or
derived values, ask: does a production factory build objects of that type? Look in
what the file imports, and in the module the file imports the type from.

Not a violation:

- calling the factory, with a test double for a boundary collaborator:
  `build_shipment_service(carrier=FakeCarrier(rate=12))`;
- building the factory's input and calling the factory: `invoice_from_order(order)`;
- constructing a type no production factory builds: a value object, a record, an
  input such as `Order(id="ord-1", items=[...])`;
- constructing the factory's output type as the expected value an assertion compares
  against: `assert invoice_from_order(order) == Invoice(order_id="ord-1", ...)`.

Hand assembly:

- `ShipmentService(RateTable.default(), LabelPrinter(carrier), carrier)` when
  `build_shipment_service` assembles that graph;
- `Invoice(order_id=order.id, lines=[...], total=sum(...))` built from an order, to use
  as the input of a test, when `invoice_from_order` derives an invoice from an order;
- a fixture that creates a Django or SQLAlchemy object's related objects one by one
  when a production factory creates the object with them.

## Violation

Test code that builds an object by calling its type's constructor with collaborators
or derived values, for use as an input or subject, when a production factory builds
objects of that type.
