---
name: parse-boundary-data-once
description: Parse boundary data once
---

# Parse boundary data once

Untyped data entering from outside (`dict[str, Any]`, `list[str | int]`, a positional tuple, a third-party error format, external JSON, the lines of a command's output) is parsed once, at the seam where it enters, into a named frozen value object. Domain code uses that type, never the raw shape.

A violation is code that reads the raw shape for anything other than building its named type: to compute a result, format it, branch on it, or pass it deeper. Signs:

- Index arithmetic on an untyped sequence: `loc[2:]`, `parts[0]`, `isinstance(x[-1], int)`.
- The same raw layout read in more than one function or method that doesn't build the type.
- `isinstance` used to decide what a raw segment means outside the parse.
- A foreign primitive type passed several calls deep into domain methods.

Not a violation:

- The parse itself. It may span the function that receives the raw data and the helpers and constructors it calls to build the type (`from_ref`, `from_json`, a loader that classifies each raw document into a typed value). Indexing, keys and `isinstance` there are the parse.
- A value whose type is already declared, such as a union of named types (`NodeKind | str`) or an enum. `isinstance` on it is ordinary narrowing.
