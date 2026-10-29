---
name: intention-revealing-names
description: A name says what its body mainly does; a function, method or class name built only from words that fit any code, or a creation method named for the caller that uses it instead of what it makes, is a violation.
---

# Intention-Revealing Names

A name says what its body mainly does.

A name is the identifier a function, method or class is defined with, read as words. Its
body is what the code under the name does: the values it returns, the state it changes,
and the calls it makes for their effect. A class's body is what its methods do
together. The body's main action or result is what a caller would say it does in one
sentence: "marks each shipment delivered", "builds the quarterly report".

A word fits any code when it names no particular action or thing: `process`, `handle`,
`do`, `manage`, `run`, `execute`, `perform`, `data`, `info`, `items`, `stuff`, `thing`,
`helper`, `util`, `manager`, `processor`, `handler`.

A creation method is a method or factory that returns a new product: an alternative
constructor, a factory class's method, a function named `create_...`, `make_...` or
`build_...`. A caller is a screen, endpoint, client app, team, job or feature that calls
it.

## Violation

A function, method or class whose name the change adds or renames, when:

- the name has no word for the body's main action or result, only words that fit any
  code: `process_data` that marks shipments delivered, `handle` on a function that
  refunds an order, `class DataHelper` whose methods compute shipping rates; or
- it is a creation method named for its caller instead of a difference in the product
  or the input it is made from: `create_for_admin_dashboard`, `make_checkout_order`,
  `for_mobile_app`.

Report it on the line that defines the name.

## Not a violation

- A name shorter than its body but naming its main action or result: `submit` for code
  that sets the status to submitted and stamps the time.
- A generic word together with a word for the main action or result:
  `handle_refund_request`, `process_payment`.
- A name the language or a framework chose: constructors, operator methods, framework
  hooks and entry points such as `handle` on a management command, `run` on a thread,
  `dispatch` on a view.
- A data type named for the thing it describes.
- A creation method named for the difference in its product or input:
  `create_draft`, `from_csv_row`, `for_currency`.
- A name whose words are false of its body. A separate rule judges disinformation.

## Why

A vague name sends readers to the body: they can't tell what `process` does without
reading it, so every call site reads as a question. A creation method named for its
caller says who uses it, not what it makes, so the next caller that needs the same
product can't find it and the name goes stale when the caller changes.

Source: Robert C. Martin, *Clean Code* (2008), chapter 2, "Use Intention-Revealing
Names".
