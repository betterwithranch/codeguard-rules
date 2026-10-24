---
name: knowledge-has-one-home
description: Each piece of knowledge (a computation, a job on a concept, a pipeline's sequence, behaviour computed from one object's data, a value an object holds, a set of things) has one home, and other code calls or reads that home; code that copies what another place already owns is a violation.
---

# Each piece of knowledge has one home

Each piece of knowledge the program holds is written in one place, and other code
reaches it there, so a change to it lands everywhere it is used.

A piece of knowledge is something the code knows that could change: the steps of a
computation, a job done to a domain concept, the order of a pipeline's stages, an
answer computed from one object's data, a value an object holds, the set of things a
part of the program supports. Its home is the one place that states it: a function, a
type that owns the job, a pipeline, the type whose data the answer reads, the object
that holds the value, the collection that lists the set.

The other place is in the file under review or in a file of the program it imports,
receives as a type, or (for a job) defines elsewhere; read that file to compare.

## The test

For each piece of code the forms below describe, ask: does this code know something
another place already owns, in the way the form names?

Yes is a violation; no is not. Code that calls, reads or derives from the home
(`domain_fee(...)`, `pipeline.run(...)`, `self.customer.email`, `tuple(HANDLERS)`)
uses the knowledge without owning a copy of it.

### Copied logic

A function is a module function, method, `@staticmethod`, `@classmethod`, `@property`,
nested function or `async def`. Two functions are copies when their bodies do the same
steps in the same order on corresponding inputs, and differ only in names (of the
function, its parameters and its locals), in the order of their parameters, or in
formatting. A body that contains another's steps plus steps of its own is a copy of
that part when the shared part is at least two statements, or one expression with at
least two operations (`max(round((subtotal - discount) * (1 + rate)), 0)`). The other
side is a function in the file under review or in a module it imports
(`from shipments.fees import domestic_fee`, `import invoices.totals`); read each
imported module of the project to compare its functions.

Violation: a function added or edited in the file under review whose body is a copy of
another function's body in that file or in a module it imports, whether the copy keeps
the parameter order (`credit_note_total(subtotal, tax_rate, discount)` with
`invoice_total`'s body) or reorders it (`return_fee(weight_grams, order_total)` with
`domestic_fee(order_total, weight_grams)`'s body). The violation is the copy.

Not copies, whatever their size:

- a function that calls the other one (`return domestic_fee(total, weight) + SURCHARGE`);
- bodies that differ in a step: a different operator, condition, constant or call
  (`>= FREE_SHIPPING_THRESHOLD` against `> 0`, `round` against `int`);
- bodies that share only one statement or one simple expression (`return self.total`,
  `if not items: return []`, `return Order(**fields)`);
- structure a framework or library asks every implementation to repeat: two DRF
  serializers' `Meta` classes, two Django models' `__str__` returning a field, two
  pydantic validators that each strip their own field, two classes' `__eq__` methods
  comparing their own fields;
- overloads and `Protocol`/ABC method stubs (`...`, `pass`, `raise NotImplementedError`).

### Overlapping responsibility

A job is what a type's public methods do to a domain concept: create it, price it,
validate it, send it, compute a projection of it (a summary, a report row, a dashboard
figure). Two types own the same job when each has a public method that does that job
to the same concept, whatever their names, method names or bodies: an
`InvoiceFactory.create_invoice` and an `InvoiceService.create_invoice`, an
`OrderTotals.compute` and an `OrderSummary.total`, two DRF views or Django admin
classes that each build the same revenue figure. Bodies need not match: two methods
that build the same `Invoice` from the same order own the same job even if one also
clamps the total. For each type the change adds, and each public method the change adds
to a type, look in this file and in the program (Grep for the domain noun and the verb)
for another type doing this job to this concept.

Violation: a second type that owns a job another type already owns on the same
concept: both `InvoiceFactory` and `InvoiceService` with a `create_invoice` that builds
an `Invoice` from an order; two report classes that each compute monthly revenue from
the same orders; two passive shapes with the same fields at the same boundary (two
models of one API's response) that change for the same reason. The violation is the
second type or method.

Not a violation:

- one type delegating to the owner (`InvoiceService.issue` calls
  `InvoiceFactory.create_invoice` and then sends it);
- two types doing different jobs on one concept (one creates invoices, one sends them);
- the same job on different concepts (creating invoices and creating refunds);
- two passive shapes with the same fields at different boundaries, mapped explicitly
  where they meet (an `InvoiceRow` from the database and an `InvoicePayload` for an
  API): each changes when its own boundary does;
- a subclass that overrides its base's method: one job, specialized.

### Re-implemented orchestration

A pipeline is a method or function that calls two or more stages in order, passing one
stage's output into the next: `run()` calling `planner.plan(order_id)` and then
`packer.pack(plan)`; a resolver calling `capture`, then `resolve`; a service calling
`extract`, then `validate`. A stage is a call to a collaborator's method or a function.
The pipeline is in the file under review or a file of the program it imports or
receives as a type (a constructor parameter typed `FulfillmentPipeline`); read that
file to see the stages its method calls.

Violation: code outside a pipeline that calls that pipeline's stages — the same
methods of the same collaborator types, or the same functions — in the pipeline's
order, feeding each output into the next stage. The sequence takes any of these forms:

- through locals: `plan = planner.plan(order_id)` then `return packer.pack(plan)`;
- nested: `packer.pack(planner.plan(order_id))`;
- reached through the pipeline's own collaborators: `self._pipeline.planner.plan(...)`;
- with `await`: `plan = await planner.plan(order_id)`;
- with the collaborators taken in this class's own constructor, or imported functions
  called in order (`validate(extract(document))`).

The violation is the code that chains the stages.

Not a violation:

- the pipeline itself, the one place that sequence is defined;
- a sequence no visible component calls in that order;
- a call to the pipeline's entry point (`pipeline.run(order_id)`), or to one stage
  alone (`planner.plan(order_id)` to show a preview);
- a different sequence: other stages, another order, or a stage between them that the
  pipeline doesn't have.

### Behaviour away from its data

The data owner is a class the program declares with its own fields: a plain class, a
dataclass, a pydantic model, an attrs class, a `NamedTuple`, a Django or SQLAlchemy
model, declared in the file under review or in a file of the program that file imports.
A domain answer is a fact about the owner the program decides with: a predicate
(`weight_kg > 30`, an invoice being overdue), a derived amount (a total, a volume), a
sort key, a classification.

Look at each function defined with `def` outside the class it reads: a module-level
function, a nested function, a `@staticmethod`, a `@classmethod`, or a method whose
body never uses `self`. It reads only one parameter's own data when it reads that
parameter's attributes or calls its methods, and nothing else besides literals, module
constants, builtins (`len`, `sorted`, `round`), and methods of the field values
themselves (`line.sku.casefold()`, `event.at.date()`). These count as something else:

- a second parameter, even one of the same type (`a.total < b.total`);
- a variable of an enclosing function, read by a nested function;
- `self` or `cls` state, or any collaborator: a client, a repository, a clock, a
  registry;
- module state that changes at run time, a file, the environment, the network.

Violation: such a function that reads only one parameter's own data, whose parameter
type is a class the program declares, and that returns a domain answer about it,
whether public or private. The violation is the function.

Not a violation:

- the parameter's type is not the program's: `str`, `int`, `datetime`, `dict`, a
  `Path`, a third-party class (`requests.Response`), a `Protocol` or abstract
  interface;
- the function formats or presents the value for something outside the program: a
  line of text (a manifest line, a log line), HTML, a response body or an export row,
  CLI output;
- the function is a method the class's base class or `Protocol` declares, so the
  interface sets its signature (`def render(self, invoice)` on a `Renderer` subclass);
- the function builds and returns a new instance of a different class the program
  declares (`Shipment(...)` from an `Order`): that is construction, not behaviour of
  the parameter;
- a lambda (`key=lambda line: line.position`);
- a method defined on the parameter's own type (`def is_heavy(self)` on `Shipment`).

### Copied owner values

A class can reach a value in two ways:

- through an object it stores: when the class stores `customer` (an attribute, or a
  dataclass, attrs or pydantic field), `customer.email` is reachable;
- through the key it is registered under: when the file, or a module it imports from,
  maps a key to the class or an instance of it (`STRATEGIES = {"express":
  ExpressShipping()}`, `@register("express")`, an enum member's value), that key is
  where the class is found, and so already known wherever the class is looked up.

A copy is an attribute, field or class attribute that the class stores whose value is
read from, or always equal to, a field of another object this class also stores, or
equal to the key this class, or an instance of it, is registered under.

Violation: a class in the file under review that stores a copy, in any form:
`self.email = customer.email` in `__init__`, `__post_init__` or another method beside
`self.customer = customer`; fields `customer: Customer` and `customer_email: str`
filled from the customer; a class attribute `kind = "express"` or `format_name = "csv"`
on a class registered under `"express"` or `"csv"`. The violation is the copy.

Not a violation:

- a value stored without the object it came from: a `SentReceipt` that keeps the email
  it was sent to and stores no customer;
- a key kept to look an object up later (`self.customer_id`), when the class does not
  also store that object;
- a value computed from several sources (`self.total = sum(line.cents for line in
  lines)`), which is no single object's field;
- a class attribute that differs from the registration key (`base_cents = 1500` on the
  class registered as `"express"`);
- a property or method that reads the value where it lives (`return
  self.customer.email`).

### Hand-synced lists

A declared set is a collection literal assigned to a module-level name: a tuple, list,
set or dict literal, or one wrapped in a call (`frozenset({...})`). An enum's members
are a declared set too. The set it lists is its items, or a dict's keys.

Violation: a module-level collection literal in the file under review whose items are
exactly the members of another declared set, in the same file or in a module the file
imports (its items, its keys, or an enum's members or their values), and that states
nothing more than that membership, so adding or removing one of the things means
editing both: `SUPPORTED = ("card", "bank")` beside `HANDLERS = {"card": ...,
"bank": ...}`; `ALL_KINDS = [Kind.CARD, Kind.BANK]` listing every member of `Kind`.
The violation is the literal that only repeats the set.

Not a violation:

- a collection derived from the other (`SUPPORTED = tuple(HANDLERS)`,
  `frozenset(Kind)`, `[kind.value for kind in Kind]`);
- a subset that selects some members, which is a fact of its own
  (`REFUNDABLE = {"card"}` beside `HANDLERS` keyed by `"card"` and `"bank"`);
- two mappings over the same keys that each hold their own values
  (`FEES = {"card": 30, "bank": 50}` and `LABELS = {"card": "Card", "bank": "Bank"}`);
- collections that list different things that happen to share a value.

## Violation

Code in the file under review that copies knowledge another place owns, in one of the
forms above: a function body copying another function's steps, a second type owning a
job another type already owns, a chain of a pipeline's stages outside the pipeline, a
domain answer about one object computed outside its class, a class storing a copy of a
value it can already reach, or a collection that repeats another's set by hand.
