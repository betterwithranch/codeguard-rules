---
name: typevar-variance
description: Variance matches use
---

# Variance matches use

- Leave a TypeVar invariant (the default) when the class both reads and writes values of that type.
- Use a covariant TypeVar (`T_co = TypeVar("T_co", covariant=True)`) only for a type that appears in return positions.
- Use a contravariant TypeVar (`T_contra = TypeVar("T_contra", contravariant=True)`) only for a type that appears in parameter positions.
