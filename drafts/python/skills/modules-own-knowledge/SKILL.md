---
name: modules-own-knowledge
description: Modules and packages are organized around what they know, so what changes together lives together; a definition kept apart from the code it changes with, or a module split by execution phase rather than by what it knows, is a violation.
---

# Modules own knowledge

Modules are organized around what they know: a definition lives with the code it
changes with, and a module or package is split by concept, never by when its code runs.

## Definitions

- A module's **public classes** are its module-level classes whose names don't start
  with `_`, in any form: plain classes, dataclasses, pydantic models, attrs classes,
  enums, `TypedDict`s, `NamedTuple`s, msgspec `Struct`s, `Protocol`s, exceptions,
  Django models and DRF serializers.
- A **passive shape** is a class that only holds data: no methods beyond the ones its
  library generates, a `@property` over its own fields, or a validator. A class with
  methods that do work has **behavior of its own**, and is a type, not a shape.
- A **package** is the directory a module is in (`payments/gateway.py` is in
  `payments/`); a subpackage is a different package. Two **sibling packages** are the
  first directories that differ under the directory they share:
  `shop/billing/invoices/line.py` and `shop/shipping/labels/slip.py` make `shop/billing`
  and `shop/shipping` siblings. Top-level packages are siblings of each other. A module
  in the shared directory itself (`shop/money.py`), or in a package that contains the
  other, has no sibling package. The standard library and installed libraries are not
  packages for this rule.
- A type's **producers** are the packages whose code constructs it: instantiates it
  (`Invoice(...)`, `Invoice.model_validate(...)`, `Invoice.objects.create(...)`),
  returns one it built, raises it, or subclasses it (an interface's subclasses are
  implementers, placed below); an enum's producers assign or return its members
  (`invoice.status = InvoiceStatus.PAID`). Its **consumers** are the code that only
  imports it, annotates with it, reads its fields or catches it.

Where a type lives follows from what changes with it, and this decides between producer
and consumer:

- a data type, result, record, exception or enum changes with the code that builds it,
  so it lives with its producer, however many packages consume it;
- a dependency or context class changes with the stage that reads it, so it lives with
  its consumer, wherever the caller that fills it in is;
- an interface (`Protocol`, ABC) changes with the code that depends on it, so it lives
  with its consumer; a class that subclasses or implements it is an implementer, neither
  producer nor consumer.

Find a type's producers, consumers and implementers in the file and in the rest of the
program (Grep for its name, and read the files that import it).

## The test

The changed lines alone never decide this test: every form places a definition by
code the change may not show, such as the union a new function sits inside, the
class a changed method belongs to, or the module an imported shape comes from. So
first Read the whole file under review and each program module it imports, then judge.

For each definition and import in the file, ask: is it kept apart from the code it
changes with, or does it sit in a module split by execution phase rather than by what it
knows? Each form below names one way this happens. Go through the forms one by one,
and for each find the code in the file it describes and decide it by that form's
violation: a definition is a violation when any one form names it one, and a form's
"not a violation" clears it of that form only, never of the others.

### More than one concept in a module

A module holds one concept: its primary type, or one family of types, and the shapes
that belong to them. A public class belongs to the module's concept when it is one of
these:

- the primary type: the class the module is about;
- a member of one family: classes that share a base defined in the module (an exception
  hierarchy, the subclasses of one abstract base), or the variants of a union declared
  in the module, with the base or the union being the concept;
- a passive shape of the primary type: one that appears in the primary type's own
  fields or method signatures, as a parameter, result or field type, and in no other
  public class of the module.

A class with behavior of its own is its own concept, even when the primary type is its
only caller or builds it in `__init__`. Constructing or using a class doesn't make it
part of the one that does. Judge by the classes the module defines, not by its file
name: a well-named module with a second unrelated class fails, and `enums.py` holding
three unrelated enums fails.

Violation: a public class outside the module's concept: a behavior-bearing class beside
the primary type (a `RetryBackoffPolicy` with a `delay()` method in the
`NotificationDispatcher` module), a class unrelated to the primary type
(`InvoiceTotals` in `notifications/dispatcher.py`), or two or more unrelated public
classes grouped by construct kind (`CarrierCode`, `RefundReason` and `InvoiceStatus` in
`enums.py`). Reported on the class outside the concept.

Not a violation: a module with one public class and any number of functions and
`_`-private classes; an exception family; a union's variants and its alias; a service
with its request and result dataclasses that only its methods take and return; a
nested class (`class Meta:`, `class Config:`).

### A shape apart from its one owner

A shape's users are the places outside its own module that name it: imports,
annotations, constructor calls, `isinstance` checks, tests excluded. Its owner is the
one type whose module holds all of those uses: the shape appears only as that type's
method parameters, results or fields, or is built only inside its methods. For a shape
the file imports, read the module that defines it and Grep for the shape's name to find
its users.

Violation: a passive shape whose only user is one type defined in another module
(`RetryAttemptParams` in `retry/retry_attempt_params.py`, used only by
`RetryAttemptPolicy.next_attempt` in `retry/retry_attempt_policy.py`). Reported where
the file under review defines the shape, or where the owner's file imports it.

Not a violation: a shape used by two or more types, modules or packages, including a
function in another module or a second class; a shape that crosses a boundary in its
own right (a request or response body a route or DRF view declares, a message a queue
consumer reads, a row a repository returns to several callers); a shape in its owner's
module; a class with behavior of its own.

### Threaded state outside its own module

A state model is a type that a workflow, pipeline or graph run threads through its
steps: each step receives it and returns an updated copy (`replace(state, ...)`,
`state.model_copy(update=...)`, `state.with_step(...)`), mutates it in place, merges
partial updates into it with a reducer (a LangGraph `TypedDict` state with
`Annotated[list[str], operator.add]` fields), or checkpoints it between steps, with or
without methods of its own. Shared by every step, it is a concept of its own. Its own
module is one whose public definitions are the state model and what is part of its
declaration (its methods, the reducers its fields name, a type used only in its
fields), and whose name names it (`checkout_state.py` for `CheckoutState`, or
`state.py` inside `checkout/`). Find the steps in the file or the files that import it.

Violation: a state model defined in a module that also defines workflow code (steps,
nodes, the runner, the graph builder), or other public types that aren't part of its
declaration, or that is named for something else (`checkout/models.py`,
`checkout/workflow.py`). Reported on the state model's class.

Not a violation: a state model alone in its own module with its methods and reducers;
a passive shape built and passed once across a boundary (a request sent and dropped,
a result returned once, a config read at start-up), defined beside the code that does
so; the workflow module importing the state model.

### A type away from its producer

Violation: a class defined in the file under review in a package that doesn't produce
it while another package does (`Invoice`, built only in `billing/`, defined in
`shipping/`; `CardDeclinedError`, raised only in `payments/`, defined in `api/`), or a
type several packages produce defined in a package that imports a sibling package.
Reported on the class.

Not a violation: a type in its one producer's package and imported by many consumers;
a type several packages produce, in a package whose modules import no sibling package.
This form doesn't place a type no package produces yet, or one produced only in tests,
or dependency and context classes and interfaces, which the next two forms place.

### A context type away from its consumer

A dependency or context class holds what a stage, service, handler or agent needs to
run: collaborators (an HTTP client, a repository, a database session, a cache),
settings, or the run's context (the current user, a tenant, a request id, a deadline):
a pydantic-ai `deps_type` dataclass, a `ServiceContext` a handler receives. Its
consumer is the stage or service whose code takes it as a parameter or field and reads
it. A module of output schemas is one whose other classes are the results, responses or
records the program produces (`schemas.py`, `results.py`, a module of response models).

Violation: a dependency or context class defined in a module of output schemas
(`ReviewDeps` beside `ReviewResult` and `Finding` in `review/schemas.py`), or in a
package other than its consumer's (`ImportContext` read only by `imports/stages.py`,
defined in `shared/context.py` or beside the command that fills it in). Reported on
the class.

Not a violation: a context class in its consumer's module, or in its own module in the
consumer's package; a class that stages in several packages read (program-wide settings
loaded once at start-up), which has no one consumer package.

### An interface away from its consumer

An interface is a class whose bases include `Protocol` (`typing.Protocol`,
`Protocol[T]`) or `ABC` (`abc.ABC`, `metaclass=ABCMeta`), with members left for others
to supply. Its consumers are code outside test files that annotates a parameter,
attribute or return value with it and uses its members.

Violation: an interface defined in the file under review whose consumers are all in
packages other than its own, whether it sits beside its implementers, in a shared
`interfaces` or `base` module, or alone (`notifications/base.py` defines
`Notifier(ABC)`, `notifications/sms.py` implements it, and only `orders/checkout.py`
takes one). Reported on the interface.

Not a violation: an interface with a consumer in its own package (`orders/ports.py`
defining a `PaymentGateway` that `orders/checkout.py` takes and `payments/stripe.py`
implements); a `Protocol` in the module of the function that takes it; an interface no
code in the repository consumes.

### A union's variants apart from its alias

A union alias is a module-level name for a union of two or more classes:
`type PaymentMethod = CardPayment | BankTransfer`,
`PaymentMethod = CardPayment | BankTransfer`, `PaymentMethod = Union[...]`, or
`PaymentMethod = Annotated[CardPayment | BankTransfer, Field(discriminator="kind")]`.
Its variants are the classes it names. A union with `None` (`Card | None`), or of plain
values (`int | str`), is not one. An inner union alias the outer alias names is itself
a variant: its own variants and alias form a run inside the outer run. The run is the
module-level code from the first variant's definition to the alias. Read the whole
module: a changed definition or statement can break the run of an unchanged union.

Violation: a union alias whose variants are not one run directly before it in its
module: a variant imported from another module, any other class, function, constant or
statement between two variants or between the last variant and the alias, or the alias
declared before its variants. Reported on the alias and on what breaks the run. This
holds alike for pydantic models, dataclasses, attrs classes, `TypedDict`s,
`NamedTuple`s and msgspec `Struct`s.

Not a violation: code before the first variant or after the alias (imports, a base
class the variants share, functions that use the union); a union written inline in an
annotation (`payment: CardPayment | BankTransfer`), which has no alias.

### Sibling packages importing each other

A package imports from another when any module in its directory, or below it, imports
any module in the other's directory or below it, in any form (`from billing import X`,
`from billing.invoice import X`, `import billing.invoice`, `from ..billing import X`).

Violation: an import in the file under review from a sibling package that, in some
module of its own, imports from the package holding the file under review (search the
sibling's files for imports of the file's package). Reported on the import.

Not a violation: `billing` importing from `shipping` with nothing in `shipping`
importing from `billing`; two packages both importing a third; a package importing its
own subpackage, or a subpackage importing its parent; an import of a library module.

### Modules split by execution phase

A phase module is a module or package named for a point in a run rather than for what
it knows: a numbered step (`step1_load.py`, `02_validate.py`, `stage3/`), a phase
(`phase_validate.py`, `pre_process.py`, `post_process.py`), or a hook moment
(`before_save.py`, `after_save.py`). A concept's knowledge is what changes when that
concept changes: its fields and their meaning, its rules, its format.

Violation: a phase module in the file under review that handles a concept whose
knowledge another phase module of the same split also handles, so a change to that one
concept edits several phase modules: `signup/step1_load.py` reading the signup's
`email` and `age` columns, `signup/step2_validate.py` checking the same email and age
rules, and `signup/step3_save.py` mapping the same fields to a row; `before_save.py`
clearing an account's verified flag when its email changes and `after_save.py` sending
the verification mail when that flag is clear. Reported on the `def` or `class` line of
the definition in the file under review that handles the shared concept.

Not a violation: a pipeline whose stages each own a distinct concept, passing on only
the result the next stage reads (`step1_fetch_rates.py` knows the rates API,
`step2_convert.py` knows the conversion arithmetic, `step3_render.py` knows the report
layout), however its modules are named or numbered.

## Violation

A definition or import in the file under review that keeps knowledge apart from the
code it changes with, in one of the forms above: a public class outside the module's
one concept, a passive shape apart from its one owner, a threaded state model outside
its own module, a type away from its producer, a context type or interface away from
its consumer, a union's variants not one run before its alias, an import from a sibling
package that imports back, or a phase module handling a concept another phase module of
the same split also handles.
