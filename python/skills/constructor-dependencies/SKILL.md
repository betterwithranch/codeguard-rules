---
name: constructor-dependencies
description: Constructor state over repeated arguments
---

# Constructor state over repeated arguments

Arguments that every caller passes with the same values (providers, strategies, registries, formatters) are the object's dependencies. Take them in `__init__`; method signatures hold only per-call data.
