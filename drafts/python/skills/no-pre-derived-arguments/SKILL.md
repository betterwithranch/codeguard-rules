---
name: no-pre-derived-arguments
description: No pre-derived arguments
---

# No pre-derived arguments

A call must not pass both a value and the input it was derived from: `quote(lines=select_lines(cart, ctx), context=ctx)`. Move the derivation into the callee, which takes `ctx` and computes `lines` itself.
