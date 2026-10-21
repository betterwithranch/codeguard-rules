---
name: reuse-test-helpers
description: Reuse shared fakes and helpers
---

# Reuse shared fakes and helpers

Do not define an inline stub, fake, or helper that duplicates one already in a shared fixture module or test utility module. Do not redefine a fixture the shared fixture module already provides. Never import a type from conftest.py or another shared fixture module; import it from its defining module.
