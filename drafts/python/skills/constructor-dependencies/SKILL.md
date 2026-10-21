---
name: constructor-dependencies
description: Constructor state over repeated arguments
---

# Constructor state over repeated arguments

A method parameter that is a provider, strategy, registry, formatter, client, repository, or similar collaborator is a dependency. Its kind decides it; you do not need to check the callers. Take dependencies in `__init__`. Method signatures hold only per-call data, such as the records the method works on.
