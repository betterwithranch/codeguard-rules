---
name: no-normalized-results
description: Do not normalize the result before asserting
---

# Do not normalize the result before asserting

Do not build a stripped copy of the actual result in a variable and compare that copy: `dataclasses.replace`, a copy-with-update, a dump that excludes fields, `del` of a key, or a comprehension that drops fields. Each removed field is unguarded. Assert the noisy field's meaningful part directly (`assert error.context["input"] == "abc"`) and assert the rest of the object normally.
