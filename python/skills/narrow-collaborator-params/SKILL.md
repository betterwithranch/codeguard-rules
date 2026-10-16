---
name: narrow-collaborator-params
description: Pass only what a collaborator needs
---

# Pass only what a collaborator needs

Do not hand a wide context object to a collaborator that reads a few of its fields. Build a narrow `...Params` at the call site. Do not add a `build_params()` method to the context object for each consumer.
