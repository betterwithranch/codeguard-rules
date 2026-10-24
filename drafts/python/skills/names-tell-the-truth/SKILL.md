---
name: names-tell-the-truth
description: Names, comments and docstrings say what the code does, in the domain's one word for it, and nothing it doesn't; a name that claims or hides behavior, a second verb for one operation, a type or factory method named for its caller or a call it serves, a one-shot maker named `...Builder`, a comment that narrates the code and a docstring that repeats it are violations.
---

# Names, comments and docstrings tell the truth

Every name, comment and docstring says what the code does, in the one word the code's
domain uses for it, and nothing the code doesn't do.

A reader learns what code does from its names first and its comments and docstrings
second. Each is a claim about the code. A claim is false when the code doesn't do what
it says, vague when it fits any code, inconsistent when collaborating code says the same
thing with another word, and empty when it only repeats what the code already says.

**What the code says** is everything a reader learns from the names, parameter names
and types, return type, decorators, values, calls and control flow in the file: that a
loop adds line totals, that a function returns early on an empty list, that a constant
is 500.

## The test

For each name the change adds or renames, and each comment and docstring it adds or
edits, ask: does it say what the code does, in the word collaborating code uses for it,
and nothing the code doesn't, in the way the form below for it describes?

### Names of functions, methods and classes

The **name** is the identifier a `def` or `class` statement gives, read as words
(`fail_dependent_tasks` is "fail", "dependent", "tasks"; `InvoiceRenderer` is
"invoice", "renderer"). The **body** is what the code under that name does: the values
it returns or yields, the state it changes (attributes it assigns, rows it saves,
messages it sends), and the calls it makes for their effect. A class's body is what its
methods do together. The **summary** is one sentence stating what the body does, in the
words a caller would use: "sets the order's status to submitted", "fails each task
waiting on the file".

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

Violation: either answer is no, reported on the name: `validate()` whose body sets
`status = SUBMITTED`; `_reconcile_dependencies()` whose body only fails the tasks waiting
on a file; `cached_rates()` that fetches the rates on every call; `process_data(shipments)`
that marks each shipment delivered; `class ReportPreparer` whose one method builds a
`QuarterlyReport`.

Not a violation:

- module functions, methods, `@staticmethod`, `@classmethod`, `@property`,
  `async def`, nested functions, read the same way, and a name that is shorter than the
  summary but true of it (`submit` for "sets the status to submitted and stamps the
  time");
- a model or schema class named for the thing it describes (`Invoice`,
  `InvoiceLineSerializer`): dataclasses, attrs classes, pydantic models, enums,
  `Protocol`s, Django models and views, DRF serializers and viewsets, SQLAlchemy models;
- dunder methods (`__init__`, `__eq__`) and framework hook names (`setUp`, `save`,
  `get_queryset`, `validate_<field>` on a serializer): names the language or framework
  chose, whose words are not the author's claim, so they match whatever the body does.

### One verb per operation

An **operation** is what a function or method does, stated without the type it does it
to: "turn text into records", "construct a document from an order", "look up a record
by its code", "send a message to a customer". Two functions do the same operation when
they take the same kind of input to the same kind of result in the same role, differing
only in the format, carrier, document or record they handle. The **verb** is the action
word of the name: `parse` in `parse_orders`, `build` in `InvoiceBuilder.build`, `fetch`
in `fetch_quote`. **Collaborating code** is the functions and methods the file under
review defines, plus those of the modules it imports and of the objects it calls; read
those modules to see their names. Code the file neither defines, imports nor calls is
not collaborating.

For each function or method name the change adds or renames, state its operation, find
the collaborating functions and methods that do the same operation, and ask: do they
all use the same verb?

Violation: no, reported on the added or renamed name: `JsonOrderReader.interpret`
beside `CsvOrderReader.parse`, both turning text into orders; `ReceiptComposer.assemble`
called next to an imported `InvoiceBuilder.build`, both constructing a document from an
order. Synonyms count as different verbs: `build`/`assemble`/`compose`/`construct`,
`parse`/`interpret`/`decode`, `fetch`/`retrieve`/`load`/`get`,
`resolve`/`find`/`lookup`. Sibling classes in one role (`CsvOrderReader` and
`JsonOrderReader`, `UpsRates` and `DhlRates`), module functions in parallel
(`parse_orders` and `parse_refunds`) and methods of one class doing the same operation
to different inputs are read the same way, whether or not they share a base class or
`Protocol`.

Not a violation: no other collaborating code does that operation; different operations
with different verbs (`parse_orders` and `render_orders`); a class implementing an
imported `Protocol` or ABC method under its declared name.

### Types named as requests or actions

An argument group is a type whose instances carry the inputs of one call to a function,
method or constructor of the program itself: the caller builds it to make that call,
and the callee reads its fields. A boundary request is data that crosses the process
boundary as a request: a request or response body bound by a web framework (a FastAPI
route parameter, a DRF serializer, a Django form, a Flask view's parsed body), a message
read from or written to a queue or broker, or a payload sent to or returned by an
outside API client. A request or action name ends in `Request`, `Create`, `Update` or
`Delete` after another word (`QuoteRequest`, `OrderCreate`), or starts with `Create`,
`Update` or `Delete` before another word (`CreateOrder`).

For each type in the file with a request or action name, whether a class, dataclass,
pydantic model, `TypedDict`, `NamedTuple` or one built with `TypedDict(...)` or
`namedtuple(...)`, find where it is built and read, in the file or by searching the
repository for its name, and ask: is it a boundary request?

Violation: no, it only groups the arguments of a call inside the program, reported on
the type's name: `PriceCalculationRequest` built by a view and read only by
`PriceCalculator.calculate`; `CreateInvoice`, a dataclass passed from one service
method to another in the same process.

Not a violation: `OrderCreate`, a pydantic model a FastAPI route takes as its body;
`ShipmentQuoteRequest`, the payload a carrier API client sends.

### Creation methods named for their caller

A factory is a class whose job is to create instances of a type: a class named
`...Factory`, `...Creator` or `...Maker`, or a class's own alternative constructors
(class methods that return `cls(...)`). A creation method is a method that returns a
new product. A caller or use case is a screen, endpoint, client app, team, job or
feature that calls the method (`admin_dashboard`, `checkout`, `mobile_app`,
`nightly_import`).

For each creation method in the file, ask: does its name state the caller or use case
that calls it, instead of a difference in the product (`create_draft`,
`create_recurring`) or in the input it is made from (`from_csv_row`, `from_order`)?

Violation: yes, reported on the method's name, whether the method is on a `...Factory`
class, a service, or the product's own class method (`Invoice.for_checkout(...)`), and
whether or not its body matches a sibling's.

Not a violation: a name stating the product variant or the input, or a single `create`.

### Classes named `...Builder`

The name `Builder` is kept for a type that assembles its product step by step. A
step-by-step builder is one that callers use through several calls on the same
instance: each call sets or adds a part of the product (methods that store parts on the
instance, often returning `self` so the calls chain), and a separate final call
(`build()`) returns the product made from those parts. A one-shot maker produces its
product from the arguments of a single call: a `build(order_id, total)` method, a
`build()` that only uses what the constructor took, or a static or class method.

For each class in the file whose name ends in `Builder`, ask: does it have methods that
store parts of the product on the instance, called before a separate method returns the
product?

Violation: no, the class makes its product in one call, under any method name (`build`,
`create`, `make`, `__call__`), reported on the class name.

Not a violation: a class with part methods called before a separate method returns the
product, whether the part methods return `self` or nothing, and whether the parts are
attributes, a list of lines, or a dataclass's fields.

### Comments

A comment is a `#` line or trailing `#` text. Tool directives (`# noqa`,
`# type: ignore`, `# pragma: no cover`, `# fmt: off`, `# pyright:`) are not comments
here. A reason the code cannot hold is a fact from outside the code that explains it: an
external system's limit or quirk (`# Stripe rejects metadata values over 500
characters`), a law or contract, a measured cause (`# the carrier API times out above
50 parcels per request`), a bug in a library with a link, or why a choice that looks
wrong is right (`# sorted first so the cache key is stable`).

For each comment the change adds or edits, ask: does it state a reason the code cannot
hold?

Violation: no, reported on the comment:

- a comment that restates or narrates the code (`# loop over the lines and add them
  up`, `# return the total`, `# increment counter`, a heading comment over each step of
  a function);
- a comment about what the code used to do or no longer does (`# this used to read the
  legacy table`, `# removed the retry`), or what it does not do (`# doesn't handle
  refunds`), since none of it is in the code;
- commented-out code;
- a bare `# TODO: clean up`;
- a comment that labels a value's unit or source where the name already says it
  (`timeout_seconds = 30  # seconds`).

Not a violation: a `TODO` or `FIXME` that names a concrete outside reason or tracker
link (`# TODO(#412): drop once the carrier ships v2`); a comment that gives a fact the
name can't (`TIMEOUT = 30  # the gateway closes idle sockets after 35s`). Comments in
Django settings, SQLAlchemy models, pydantic models, CLI modules and scripts are read
the same way.

### Docstrings

A docstring is the string literal that opens a module, class, function or method body.
Information is anything a caller needs that the code doesn't show: units or ranges the
types don't carry, which exceptions are raised and when, side effects (writes a file,
sends a request), behavior on edge inputs (empty list, `None`, a missing key), a reason
or outside constraint (`The carrier API accepts at most 50 parcels`), thread-safety, or
the format of a string it takes or returns.

For each docstring the change adds or edits, ask: does it give the reader information,
beyond what the code says?

Violation: no, reported on the docstring:

- a docstring that rewords the name or signature (`"""Return the total."""` on
  `def total(self) -> int`, `"""Order model."""` on `class Order`, `Args: order: the
  order` sections that repeat parameter names);
- a docstring that narrates the body step by step;
- a docstring that describes what the code used to do or does not do;
- a docstring that props up a vague name by saying what the body plainly does
  (`"""Sets the order to submitted and emails the customer."""` on `def handle`).

Not a violation: a docstring with at least one piece of information (a unit, a raised
exception and when, an edge case, a side effect, an outside constraint), even when it
also restates the name; a CLI command's docstring that is its `--help` text. Module,
class, `@property`, Django model, DRF view, pydantic model, Click or Typer command
docstrings are read the same way.

## Violation

A name, comment or docstring added or edited in the file under review that doesn't tell
the truth about the code: a name that claims what its body doesn't do or names nothing
it does, a verb that differs from the one collaborating code uses for the same
operation, a request or action name on a type that only groups a call's arguments
inside the program, a creation method named for its caller, a `...Builder` class that
makes its product in one call, a comment that states no reason the code cannot hold, or
a docstring that gives no information beyond what the code says.
