---
name: parse-boundary-data-once
description: Parse boundary data once
---

# Parse boundary data once

Boundary data is data whose shape something outside the program defines: external JSON, a file format, a command's output, or a dict or tuple a third-party library returns, even when the library declares a `TypedDict` for it (pydantic's `ErrorDetails`).

Only the parse knows boundary data's raw layout: its keys, its positions, its nesting and what its raw values mean. The parse reads the raw data and returns what the data says as typed values: a value object, or typed values such as a path, a number, a datetime, an enum member, or a tuple or list of them. All other code works with those values.

Judge what the code does with the raw data, not where the code sits or what it is called. Code either converts raw data into typed values, or it uses the data to answer a question, produce output or decide what to do. Code that does both in one step, using the data straight from its raw layout, is a violation.

A violation is any of:

- Raw data used to compute a result, format output or decide behavior: `f"{error['carrier']}: {error['reason']}"`, `if alert["urgent"]`, hours computed from `payload["events"][-1]["timestamp"]`.
- The same raw layout read in more than one place, by code that doesn't make up one parse.
- Raw data read where a parsed value for it already exists.
- Raw data passed on to code that does any of the above.

Not a violation:

- The parse itself, however many functions, constructors, helpers or generators it spans, and whether it returns a value object or typed values. Indexing, string keys, splitting text into lines and fields, and `isinstance` checks are the parse when what comes out is the data's content as typed values: a `ReleaseBranch` from each line of `git ls-remote`, typed steps from YAML documents, or the file paths a tool's output lists.
- Handing raw data straight to code that parses it: a validator (`Model.model_validate(raw)`) or a dispatcher that binds it to a typed function's parameters (`handler(**raw)`).
- A third-party object with its own typed methods and attributes, such as an exception, a response or a client. Calling them is not reading a raw shape. The dicts and tuples they return are boundary data.
- Data the program builds itself, whatever its shape: a `tuple[SyntaxNode, bytes]` passed between its own methods, a union of its own types (`NodeKind | str`), an enum.
