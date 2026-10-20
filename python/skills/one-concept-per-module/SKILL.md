---
name: one-concept-per-module
description: One concept per module
---

# One concept per module

A module holds one cohesive concept and is named after its domain purpose or its primary type.

- A well-named module is still a bucket if it defines a second, unrelated public class. Judge by contents, not by filename. A second public class may stay only if it is `_`-private to the primary type, or part of one family a reader would look for under this module's name.
- "The primary type builds it" does not make a second class part of the module. A `RetryBackoffPolicy` that a `NotificationDispatcher` creates in `__init__` is its own concept and belongs in its own module, even if the dispatcher is its only caller.
