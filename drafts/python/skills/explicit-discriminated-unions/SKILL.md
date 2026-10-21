---
name: explicit-discriminated-unions
description: Discriminated unions are explicit
---

# Discriminated unions are explicit

- Tag every variant with a `kind: Literal[...]` field and declare the union as discriminated on that tag. Never rely on inferring the variant from field shape.
- Define a union's variant classes together, next to the alias, with no unrelated types between them. For nested unions, define the inner union first.
