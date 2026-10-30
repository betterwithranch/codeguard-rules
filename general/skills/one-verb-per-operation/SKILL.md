---
name: one-verb-per-operation
description: One operation goes by one verb; a function or method name the change adds or renames whose verb differs from the one collaborating code uses for the same operation is a violation.
---

# One Verb per Operation

One operation goes by one verb.

An operation is what a function or method does, stated without the type it does it to:
"turn text into records", "construct a document from an order", "look up a record by
its code", "send a message to a customer". Two functions do the same operation when
they take the same kind of input to the same kind of result in the same role, differing
only in the format, carrier, document or record they handle.

The verb is the action word of the name: `parse` in `parse_orders`, `build` in
`InvoiceBuilder.build`, `fetch` in `fetch_quote`. Synonyms are different verbs:
`build`, `assemble`, `compose` and `construct`; `parse`, `interpret` and `decode`;
`fetch`, `retrieve`, `load` and `get`; `find`, `resolve` and `lookup`.

Collaborating code is the functions and methods the file under review defines, plus
those of the modules it imports and the objects it calls. Read those modules to see
their names.

## Violation

A function or method whose name the change adds or renames, when collaborating code
does the same operation under a different verb: `JsonOrderReader.interpret` beside
`CsvOrderReader.parse`, both turning text into orders; `ReceiptComposer.assemble` called
next to an imported `InvoiceBuilder.build`, both constructing a document from an order.

Sibling classes in one role, module functions in parallel, and methods of one class
doing the same operation to different inputs are read the same way, whether or not
they share a base class or interface.

Report it on the line that defines the name.

## Not a violation

- An operation no other collaborating code does.
- Different operations with different verbs: `parse_orders` and `render_orders`.
- A method implementing an imported interface's or base class's method under the name
  it declares.
- Code the file neither defines, imports nor calls.

## Why

One operation under two verbs reads as two operations. A reader who knows `parse`
looks for `parse_json` and doesn't find it, or reads `interpret` and wonders how it
differs from `parse`. One verb per operation lets names predict each other.

Source: Robert C. Martin, *Clean Code* (2008), chapter 2, "Pick One Word per Concept".
