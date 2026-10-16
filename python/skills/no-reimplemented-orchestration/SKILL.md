---
name: no-reimplemented-orchestration
description: Do not re-implement orchestration
---

# Do not re-implement orchestration

When a component already runs a multi-step pipeline (a graph you invoke, a resolver that chains stages, a service with one `run()`), callers invoke it as a unit. A method body that calls two or more pipeline stages in sequence, passing one's output into the next (`capture` then `resolve`, `plan` then `apply`, `extract` then `validate`), is the sign. Search for any component that already calls those collaborators in that order. If the owner lacks the entry point a caller needs, add a narrow one to the owner; do not copy its steps.
