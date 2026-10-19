---
name: one-concept-per-module
description: One concept per module
---

# One concept per module

A module holds one cohesive concept and is named after its domain purpose or its primary type.

- A well-named module is still a bucket if it defines a second, unrelated public class. Judge by contents, not by filename. A second public class may stay only if it is `_`-private to the primary type, or part of one family a reader would look for under this module's name.
- "The primary type builds it" does not make a second class part of the module. A `RetryBackoffPolicy` that a `NotificationDispatcher` creates in `__init__` is its own concept and belongs in its own module, even if the dispatcher is its only caller.
- A `models.py` is acceptable only for a tight family of passive shapes with no behavior. Split it if it mixes output schemas, dependency/context classes, input builders, validators, formatters, or persistence code.
- Do not split one concept across one-symbol files. A behavior-bearing type's own parameter and result shapes, used by nothing else, live in that type's module. A `*_params.py` or `*_result.py` whose only user is one type's method signature is the defect.
- A value several peer types share is its own concept. It does not move into any one peer's module.
- All variants of a discriminated union live in one module named after the union alias.

Bad: `retry_attempt_policy.py`, `retry_attempt_params.py`, `retry_attempt.py`, each with one symbol, where the params and result exist only for the policy's one method.

Good: `retry_attempt_policy.py` holds `RetryAttemptPolicy`, `RetryAttemptParams`, and `RetryAttempt`.
