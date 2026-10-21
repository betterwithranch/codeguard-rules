---
name: one-responsibility-per-function
description: One responsibility per function
---

# One responsibility per function

A violation is:

- A function whose description needs "and" (fetches and decides, parses and looks up), even a short, simple one.
- Branching that maps inputs to outputs, or repeats one pattern with different values.
- A helper that is an arbitrary chunk of its caller, with no conceptual identity.
- `**kwargs` used to cut a parameter count.
- A wrapper that forwards all its parameters to another API.
- A dataclass that only groups one call's arguments: built at the call site and unpacked at once.
