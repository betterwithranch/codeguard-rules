---
name: no-single-use-map-wrappers
description: No function whose whole body maps an already-named function over a collection and that has one call site
---

# No single-use map wrappers

A function earns its name by adding behavior or by being reused; one that only applies
an existing function to each item, for one caller, adds a name without either.

## Definitions

- A **map wrapper** is a function whose whole body returns one comprehension, generator
  or `map` that calls an already-named function or method on each item and does nothing
  else: `return [label(shipment) for shipment in shipments]`,
  `return {s.id: label(s) for s in shipments}`, `return list(map(label, shipments))`,
  `return [self.label(s) for s in shipments]`.
- It **adds behavior** when the comprehension does more than call the named function:
  it filters (`if shipment.active`), computes inline (`shipment.weight * RATE`, an
  f-string, a constructor with several fields), unpacks (`for sku, qty in rows`), sorts,
  deduplicates, or handles errors.
- A **call site** is a call or reference to the function anywhere in the project: in the
  file under review, or in any other file (search the repository for its name). A
  reference passed as a value (`sorted(..., key=labels)`, a registry entry, a framework
  hook name, an overridden or `Protocol` method) counts as more than one, since the
  caller is outside the code.

## The test

For each map wrapper in the file under review, ask: does it add behavior, does it have
two or more call sites or a reference passed as a value, or does it implement a method a
base class or `Protocol` declares?

Yes to either: not a violation. No to both: violation.

## Violation

A map wrapper in the file under review that adds no behavior and is called from exactly
one place: `_labels(shipments)` returning `[label(s) for s in shipments]`, called once
by `dispatch`.
