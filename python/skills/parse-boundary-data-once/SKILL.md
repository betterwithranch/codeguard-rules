---
name: parse-boundary-data-once
description: Parse boundary data once
---

# Parse boundary data once

Outside data is read only through the part of the program that declares and checks its
shape.

Outside data is data whose shape something outside the program decides: a request body,
a file, a command's output, an external API's response. Its shape is undeclared until
code in the program, or a typed library API, states it. The parse is the code that
turns undeclared data into declared values, and every other read goes through what the
parse returns.

## The test

For each read of data by a key, an index, a position, or by splitting text, ask which
code states the shape being read.

Declared, so reading it by attribute or by its declared keys is not a violation, whether
it is an object or a dict:

- a class, dataclass, pydantic model, `TypedDict` or enum, the program's own or a
  library's (pydantic's `ErrorDetails`);
- a DRF serializer's `validated_data`, a Django query's `.values()` or `.values_list()`
  rows, or a column spec that maps a file's columns to names;
- a mapping after a check of every key and value (`isinstance` over the whole mapping),
  read by keys that are themselves data (`fallbacks.get(name)`).

Undeclared:

- `json.loads`, `yaml.safe_load` and `requests`' `.json()` results, `request.data` or
  `request.body` before a serializer, `csv.reader` and `csv.DictReader` rows, and text a
  command or file returns;
- a value annotated `dict[str, Any]`, `Any`, or a bare `dict` that holds one of these.

## Violation

Undeclared data read outside the parse:

- used to compute a result, format output or decide what to do
  (`f"{error['carrier']}: {error['reason']}"`, `if alert["urgent"]`, hours computed from
  `payload["events"][-1]["timestamp"]`);
- passed on to code that reads it that way;
- read where a parsed value for the same data already exists.

## The parse

Code whose job is to turn undeclared data into declared values. It reads the raw keys,
positions and text and returns declared values: an object, typed values such as a path,
a number, a datetime or an enum member, or a declared dict. It may span any number of
functions, constructors and helpers. Handing undeclared data straight to a declaration
that checks it is the parse: `Model.model_validate(raw)`, `Serializer(data=raw)`, a
dispatcher that binds it to a typed function's parameters (`handler(**raw)`).

Data the program builds itself is not outside data, whatever its shape: a
`model_dump()` of its own model, a `tuple[SyntaxNode, bytes]` passed between its own
methods, a union of its own types. A third-party object's typed methods and attributes
are declared; calling them is not reading a raw shape.
