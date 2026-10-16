---
name: one-home-for-defaults
description: One home for defaults
---

# One home for defaults

A field's default is declared once, on the owning type. Callers omit it rather than supply it. A fallback in a consumer (`x or uuid4()`, `x if x is not None else default`) that duplicates a default the type could declare is a default in the wrong place. A type that defaults one field but leaves a sibling required, while a consumer fills in that sibling, is the clearest case.
