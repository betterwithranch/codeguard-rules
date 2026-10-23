---
name: one-verb-per-operation
description: Functions and methods that do the same operation for collaborating code use the same verb
---

# One verb per operation

Code that works together names one operation with one verb, so a reader who knows one
name can find and predict the others.

## Definitions

- An **operation** is what a function or method does, stated without the type it does
  it to: "turn text into records", "construct a document from an order", "look up a
  record by its code", "send a message to a customer". Two functions do the same
  operation when they take the same kind of input to the same kind of result in the same
  role, differing only in the format, carrier, document or record they handle.
- The **verb** is the action word of the name: `parse` in `parse_orders`, `build` in
  `InvoiceBuilder.build`, `fetch` in `fetch_quote`.
- **Collaborating code** is the functions and methods the file under review defines,
  plus those of the modules it imports and of the objects it calls. Read those modules
  to see their names. Code the file neither defines, imports nor calls is not
  collaborating.

## The test

For each function or method name the change adds or renames, state its operation. Then
find the collaborating functions and methods that do the same operation, and ask: do
they all use the same verb?

Yes, or no other collaborating code does that operation: not a violation.
No: violation.

Forms the test reads the same way:

- sibling classes in one role (`CsvOrderReader` and `JsonOrderReader`, `UpsRates` and
  `DhlRates`), whether or not they share a base class or `Protocol`;
- module functions in parallel (`parse_orders` and `parse_refunds`);
- methods of one class that do the same operation to different inputs;
- a class that implements an imported `Protocol` or ABC method under its declared name
  uses that name's verb, which matches;
- different operations with different verbs (`parse_orders` and `render_orders`) match;
- synonyms count as different verbs: `build`/`assemble`/`compose`/`construct`,
  `parse`/`interpret`/`decode`, `fetch`/`retrieve`/`load`/`get`,
  `resolve`/`find`/`lookup`.

## Violation

A function or method name added or renamed in the file under review whose verb differs
from the verb collaborating code uses for the same operation: `JsonOrderReader.interpret`
beside `CsvOrderReader.parse`, both turning text into orders; `ReceiptComposer.assemble`
called next to an imported `InvoiceBuilder.build`, both constructing a document from an
order.
