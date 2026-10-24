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

A shape read picks out a part of the data by something the outside source's format
defines: a key (`error["carrier"]`), an index or position (`events[-1]`), or a
delimiter-separated field (`line.split(":")[0]` on grep output). Treating text only as
text is not a shape read: splitting it into lines to number, window, count or show
them, hashing it, storing or passing it on.

For each shape read, ask which code states the shape being read.

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

## The parse

The parse is the code that turns undeclared data into declared values: an object, a
model, a declared dict, a typed value such as a path, a number, a datetime or an enum
member, or a collection of these (`list[Path]`, `Iterator[TrackingEvent]`). It may span
several functions, constructors and helpers, including one that receives the raw data
from another and yields part of the result. Handing undeclared data straight to a
declaration that checks it is the parse: `Model.model_validate(raw)`,
`Serializer(data=raw)`, `Diagnostic.from_json(item)` for each item of a raw list, a
dispatcher that binds it to a typed function's parameters (`handler(**raw)`). So is
choosing which declaration parses it (routing on a document's `kind` key), and checking
it to accept or reject it: a validator, including a pydantic `mode="before"` validator
that reads raw keys, or a check that raises an error about the data's format before
the parse proceeds.

"Once" is about where, not when: one piece of code reads each raw field, however many
times it runs.

For each shape read of undeclared data, follow the value it produces: does it go into
building a declared value, as a field of it, an argument to its constructor or
validator, the choice of which one parses the data, or the decision to reject it? Yes
is the parse, unless another
function in the file also reads the same raw field.

## Violation

A shape read of undeclared data whose value goes somewhere other than building a
declared value, reported on the line of the read:

- into a formatted message, a count or a computed result, or a decision about what the
  program does next, other than rejecting the data (`f"{error['carrier']}: {error['reason']}"`, `len(lines)` of grep matches,
  `if alert["urgent"]: page(on_call)`, hours computed from
  `payload["events"][-1]["timestamp"]`);
- a second read of a raw field another function in the file also reads
  (`payload["events"][-1]` in three functions, each picking a different key);
- a read where a parsed value for the same data already exists;
- undeclared data passed on to code outside the parse that reads it in one of these
  ways.

Data the program builds itself is not outside data, whatever its shape: a
`model_dump()` of its own model, a `tuple[SyntaxNode, bytes]` passed between its own
methods, a union of its own types. A third-party object's typed methods and attributes
are declared; calling them is not reading a raw shape. What such a method returns is
undeclared when its type is a raw dict, a list of raw dicts, or text
(`failure.errors() -> list[dict[str, Any]]`).
