---
name: types-live-with-producer
description: Types live with their producer
---

# Types live with their producer

A type lives in the package whose code constructs it: instantiates it, returns it, raises it, or subclasses it. The number of packages that import it does not move it.

- Group a package's passive shapes into concept-named modules (a union family in one file, an enum and its small companions in another). Do not group them by construct kind.
- A type many packages depend on lives in a low-level package that imports no sibling package.
- Dependency and context classes live beside the stage or service that consumes them, not beside output schemas.
- A validator stays on its model only for intrinsic invariants: required field combinations, normalized fields, allowed ranges. Validation that needs runtime dependencies, registries, stored data, or peer collections belongs to the service that has that context.
