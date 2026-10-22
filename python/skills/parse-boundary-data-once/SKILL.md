---
name: parse-boundary-data-once
description: Parse boundary data once
---

# Parse boundary data once

Boundary data is data whose shape something outside the program defines: external JSON, a file format, a command's output, or a dict or tuple a third-party library returns, even when the library declares a `TypedDict` for it (pydantic's `ErrorDetails`). It is parsed once, at the seam where it enters, into a named frozen value object the program defines. Code uses that type, never the raw shape.

A violation is code that reads boundary data's raw shape for anything other than building its named type: to compute a result, format it, branch on it, or pass it deeper. Signs:

- Index arithmetic or string keys on it: `loc[2:]`, `parts[0]`, `details["msg"]`.
- The same raw layout read in more than one function or method that doesn't build the type.
- `isinstance` used to decide what a raw segment means outside the parse.
- A foreign primitive type passed several calls deep into domain methods.

Not a violation:

- The parse itself. It may span the function that receives the raw data and the helpers and constructors it calls to build the type (`from_ref`, `from_details`, a loader that classifies each raw document into a typed value). Indexing, keys and `isinstance` there are the parse. So is splitting a command's output into lines and fields when each piece goes straight into the type's constructor (`from_ref(line.split("\t")[-1])`); reading a raw value to compute or format anything else is still a violation. So is handing the raw data straight to code that parses it: a validator (`Model.model_validate(raw)`) or a dispatcher that binds it to a typed function's parameters (`handler(**raw)`).
- A third-party object with its own typed methods and attributes, such as an exception, a response or a client. Calling them is not reading a raw shape; the dicts and tuples they return are boundary data.
- Data the program builds itself, whatever its shape: a `tuple[SyntaxNode, bytes]` passed between its own methods, a union of its own types (`NodeKind | str`), an enum.
