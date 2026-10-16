---
name: no-normalized-results
description: Do not normalize the result before asserting
---

# Do not normalize the result before asserting

Do not rebuild the actual result with `dataclasses.replace`, a copy-with-update, a dump that excludes fields, or a comprehension that strips fields before `==`. Each removed field is unguarded. Assert the noisy field's meaningful part directly (`assert error.context["input"] == "abc"`) and assert the rest of the object normally.
