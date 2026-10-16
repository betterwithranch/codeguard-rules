---
name: one-form-per-input
description: One way to specify each input
---

# One way to specify each input

A function accepts one form for each input.

- No two mutually exclusive parameters for the same value reconciled by a guard (`if a is None and b: a = derive(b)`).
- No deriving one input from another inside the function.
- A single default (`x or default`) and `**overrides` passed untouched to one typed target are fine.

Take the already-derived value and move the derivation to the call site. A separate derivation helper is allowed only if it reads a value the source already holds (`catalog.price_index`). It must not run a construction backwards: if production builds `Shipment(parcels=[...])`, a helper that builds shipments from a registry of parcel keys is the defect.
