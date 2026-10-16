---
name: type-name-suffixes
description: Standard type-name suffixes
---

# Standard type-name suffixes

- Use `Builder` only for the GoF Builder pattern, where a product is assembled step by step through a builder interface. Otherwise name the type after what it creates (`Factory`, `Composer`, or the output).
- Use `Params`, not `Request`, for an object that groups arguments to a method or constructor. Reserve `Request` for real external or API requests.
- A factory exposes `create(params) -> X`. It does not expose one method per caller or use case with overlapping arguments. Choose a variant by what the type does, not by who calls it.
