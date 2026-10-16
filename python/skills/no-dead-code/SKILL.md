---
name: no-dead-code
description: No dead code
---

# No dead code

Every production symbol must have a production reference. Search the whole repository before reporting. Orphan shapes:

- Referenced only by its own definition.
- Referenced only by tests. Either delete it with its tests or wire it into production.
- Referenced only by an `__init__.py` re-export.
- An unused method on a live type, such as a stale `with_*` copy helper or factory.
- A package directory whose only file is a code-less `__init__.py`. An empty `__init__.py` beside real modules is correct.

A symbol is live if reached dynamically: decorator registration, route or handler registries, string-keyed dispatch, framework configuration, entry points, or use within its own module.
