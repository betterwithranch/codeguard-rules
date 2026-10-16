---
name: typed-dispatch-registries
description: Typed registries for dispatch
---

# Typed registries for dispatch

When a class takes a `dict[str, Callable]` for dispatch, wrap it in a named registry class with a `resolve` method and take the registry instead.
