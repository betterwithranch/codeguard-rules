---
name: types-model-domain-concepts
description: Types model real domain concepts
---

# Types model real domain concepts

- Do not wrap a bare identity. A type that only wraps an existing key or id, with no behavior or invariant, should be replaced by the key itself.
- Do not model an `XCreate` type for the act of creating something. Group a factory's arguments in a `...Params` object beside the factory method.
- Do not store a copy of a value another object in hand already owns. Read it from the owner. This includes a strategy carrying a `kind` attribute equal to the key it is registered under.
- A stored record that crosses a queue, workflow, or graph boundary is passed by its id and re-fetched on the other side, not copied into a travelling object.
- Promote a bare `dict`/`list`/`set` to a named index type when it is queried with the same idiom at three or more sites, when two collections index the same data different ways, or when the build loop has a silent last-writer-wins or merge rule. The index owns the lookups and the collision policy, and builds itself with a `classmethod`.
