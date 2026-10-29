---
name: no-disinformation
description: A name claims nothing its body doesn't do; a function, method or class name with a verb, noun or qualifier its body makes false is a violation.
---

# No Disinformation

A name claims nothing its body doesn't do.

A name is the identifier a function, method or class is defined with, read as words:
`get_cached_rates` is "get", "cached", "rates"; `PdfInvoiceRenderer` is "PDF",
"invoice", "renderer". Its body is what the code under the name does: the values it
returns, the state it changes (fields it sets, rows it saves, messages it sends), and
the calls it makes for their effect. A class's body is what its methods do together.

A word of the name is a claim about the body. It is false when the body doesn't do it:
a verb for an action the body doesn't take, a noun for a thing it doesn't touch, a
qualifier that isn't true of it.

## Violation

A function, method or class whose name the change adds or renames, when a word of the
name is false of the body:

- a verb the body doesn't do: `validate` on code that only sets a status, `delete` on
  code that marks a row disabled, `send` on code that only builds a message;
- a noun the body doesn't touch: `orders` on code that reads shipments;
- a qualifier the body makes false: `cached` on code that fetches on every call, `pdf`
  on code that renders HTML, `sorted` on a result that isn't sorted.

Report it on the line that defines the name.

## Not a violation

- A name shorter than its body but true of it: `submit` for code that sets the status
  to submitted and stamps the time.
- A name vague enough to fit any code, such as `process_data` or `handle`: a separate
  rule judges it.
- A name the language or a framework chose, whose words are not the author's claim: a
  constructor or operator method, a framework hook such as a model's `save`.
- A name that implements an interface's method under the name the interface declares.
- A data type named for the thing it describes.

## Why

Readers trust names, and read the body only when the name leaves them unsure. A false
name sends them wrong without a reason to look: they call `validate` expecting an error
for bad input and get none, or rely on `cached` and pay for a fetch on every call.

Source: avoid disinformation (Robert C. Martin, *Clean Code*, 2008, chapter 2).
