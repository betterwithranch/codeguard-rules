---
name: test-helper-parameters
description: Construction helper parameters
---

# Construction helper parameters

- Declare typed parameters. A `**kwargs` or `**overrides` parameter is allowed only when passed untouched to one typed target.
- Do not raise `TypeError` for unexpected `**kwargs` keys by hand.
- No alternative-input branching: do not accept two parameters for the same value and pick between them.
- No test-only bundle types (`...Setup`, `...Resources`) and no setting attributes on an object after it is built.
- Do not give a test-only shape a production-sounding name.
- Remove unused parameters, and do not re-pass a value equal to the callee's default.
