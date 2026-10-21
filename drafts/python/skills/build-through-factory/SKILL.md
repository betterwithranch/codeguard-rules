---
name: build-through-factory
description: Build through the production factory
---

# Build through the production factory

When a production factory or builder assembles an object graph, the test calls that factory. Inject a test double for the boundary collaborator through a constructor parameter. Do not rebuild the same graph by hand in a fixture. If the factory does not accept the double, the fix is a constructor parameter with a production default, not a bypass.

The same holds for derivation. If the factory computes intermediate values from its input, build the factory's input and call the factory. Do not re-derive those values in the fixture to construct the output type directly.
