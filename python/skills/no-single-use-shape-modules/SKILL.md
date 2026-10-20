---
name: no-single-use-shape-modules
description: No single-use shape modules
---

# No single-use shape modules

Do not split one concept across one-symbol files. A behavior-bearing type's own parameter and result shapes, used by nothing else, live in that type's module. A `*_params.py` or `*_result.py` whose only user is one type's method signature is the defect.

Bad: `retry_attempt_policy.py`, `retry_attempt_params.py`, `retry_attempt.py`, each with one symbol, where the params and result exist only for the policy's one method.

Good: `retry_attempt_policy.py` holds `RetryAttemptPolicy`, `RetryAttemptParams`, and `RetryAttempt`.
