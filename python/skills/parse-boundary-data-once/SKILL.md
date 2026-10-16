---
name: parse-boundary-data-once
description: Parse boundary data once
---

# Parse boundary data once

Untyped data entering from outside (`dict[str, Any]`, `list[str | int]`, a positional tuple, a third-party error format, external JSON) is parsed once, at the seam where it enters, into a named frozen value object. Domain code uses that type, never the raw shape.

Signals of in-place interpretation:

- Index arithmetic on an untyped sequence: `loc[2:]`, `parts[0]`, `isinstance(x[-1], int)`.
- The same raw layout read in more than one method.
- `isinstance` used to decide what a raw segment means.
- A foreign primitive type passed several calls deep into domain methods.
