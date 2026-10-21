---
name: one-responsibility-per-type
description: One responsibility per type
---

# One responsibility per type

A type has exactly one reason to change. Two unrelated reasons is already a violation, whatever the size.

- Group the methods by what change would force each to change. One group: keep. Two or more unrelated groups: split into focused services or value objects, one per concern.
- Size is not the test. A large cohesive class is fine. A small two-method class serving two unrelated concerns is not.
- A frozen value object with no injected collaborators is not a god object. Methods that read only its own immutable fields are its behavior, even if they fall into several topics. Do not split them out.
- A very long entry method (such as a 100-line `execute()`) or repeated `isinstance` branching across sibling methods: extract an orchestrator or per-shape handlers so the entry method reads as named steps.
- A function with several responsibilities is a class. Signs: a conjunction name (`fetch_and_validate`), a long list of unrelated collaborator arguments, or sibling functions that all take the same arguments. Promote it to a type whose fields are the collaborators and whose methods are the steps.
