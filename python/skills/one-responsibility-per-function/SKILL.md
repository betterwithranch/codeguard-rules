---
name: one-responsibility-per-function
description: One responsibility per function
---

# One responsibility per function

- If a method's description needs "and" (fetches and decides, parses and looks up), split it. This holds for short, simple methods too.
- Replace branching that maps inputs to outputs, or repeats one pattern with different values, with data-driven dispatch (a dict lookup, an ordered tuple, iteration over metadata).
- Do not extract a helper that is an arbitrary chunk of the original with no conceptual identity.
- Do not use `**kwargs` to reduce a parameter count.
- Do not write a wrapper that forwards all its parameters to another API.
- Group parameters into a dataclass only when the group is a concept you would store, pass on, or test as a unit. A parameter object built at the call site and unpacked at once is indirection.
