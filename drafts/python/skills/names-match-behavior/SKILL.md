---
name: names-match-behavior
description: A function, method or class name states what its body does, and nothing its body does not do
---

# Names match what the code does

A function, method or class is named for what its code does, and every word of its name
is true of that code.

## Definitions

- The **name** is the identifier a `def` or `class` statement gives, read as words
  (`fail_dependent_tasks` is "fail", "dependent", "tasks"; `InvoiceRenderer` is
  "invoice", "renderer").
- The **body** is what the code under that name does: the values it returns or yields,
  the state it changes (attributes it assigns, rows it saves, messages it sends), and the
  calls it makes for their effect. A class's body is what its methods do together.
- The **summary** is one sentence stating what the body does, in the words a caller
  would use: "sets the order's status to submitted", "fails each task waiting on the
  file".

## The test

For each name the change adds or renames, write the body's summary, then ask two
questions:

1. Does every word of the name describe something in the summary? A verb the body
   doesn't do (`validate` on code that only sets a status), a noun the body doesn't touch
   (`orders` on code that reads shipments), or a qualifier that is false (`cached` on code
   that never caches) answers no.
2. Does the name contain a word for the main action or result in the summary? A name
   built only from words that fit any code (`process_data`, `handle_items`, `do_work`,
   `manage_state`, `Helper`, `Processor`, `Manager` on a class whose body makes one
   specific thing) answers no.

Both yes: the name matches. Either no: violation.

Forms the test reads the same way:

- module functions, methods, `@staticmethod`, `@classmethod`, `@property`,
  `async def`, nested functions;
- classes, dataclasses, attrs classes, pydantic models, enums, `Protocol`s, Django
  models and views, DRF serializers and viewsets, SQLAlchemy models: a model or schema
  class is named for the thing it describes (`Invoice`, `InvoiceLineSerializer`), and
  that matches;
- dunder methods (`__init__`, `__eq__`) and framework hook names (`setUp`, `save`,
  `get_queryset`, `validate_<field>` on a serializer) are names the language or framework
  chose; their words are not the author's claim, so they match whatever the body does;
- a name that is shorter than the summary but true of it matches (`submit` for "sets the
  status to submitted and stamps the time").

## Violation

A name added or renamed in the file under review that fails either question:

- it claims what the body doesn't do: `validate()` whose body sets `status = SUBMITTED`;
  `_reconcile_dependencies()` whose body only fails the tasks waiting on a file (nothing
  is reconciled); `cached_rates()` that fetches the rates on every call;
- it names nothing the body does: `process_data(shipments)` that marks each shipment
  delivered; `class ReportPreparer` whose one method builds a `QuarterlyReport`.
