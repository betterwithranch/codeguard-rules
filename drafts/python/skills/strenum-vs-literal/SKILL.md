---
name: strenum-vs-literal
description: StrEnum vs Literal
---

# `StrEnum` vs `Literal`

- `StrEnum` when code branches on the value or uses it as a dict or registry key.
- `Literal["x"] = "x"` as the fixed tag on one variant of a discriminated union.
- `Literal["a", "b"]` for a constrained field nothing branches on.
