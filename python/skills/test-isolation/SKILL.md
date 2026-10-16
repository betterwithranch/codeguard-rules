---
name: test-isolation
description: Test isolation
---

# Test isolation

- Revert global state and release resources after each test.
- Do not keep mutable state in class attributes shared across test methods.
- A session-scoped fixture must return an immutable resource.
- An `autouse` fixture's scope must match the cleanup it does.
- Delete empty or placeholder fixtures.
