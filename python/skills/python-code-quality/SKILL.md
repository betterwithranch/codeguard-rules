---
name: python-code-quality
description: Naming, module structure, responsibility, function design, typing, and duplication rules for any Python file.
---

# Python Code Quality

These rules apply to every `.py` file, production and test code alike. A test file is not exempt from any rule here.

## Names match what the code does

State in one sentence what a symbol does, read from its body. The main verb and nouns of that sentence must appear in the name. Every word in the name must be true of the body. A mismatch in either direction is a defect.

- A misleading name is worse than a vague one. `reconcile` on code that only propagates a failure one way is wrong, not just unclear.
- Both the verb and the noun must carry domain meaning. A generic verb on a generic noun (`process_data`, `handle_items`, `manage_state`) says nothing.
- Name a symbol after what it produces, owns, or does. Do not name a type `Preparer` or `Processor` when it builds a specific output.
- Use one verb per concept across collaborating types. Do not mix `resolve`/`interpret` or `build`/`assemble` for the same operation.

Bad: `_reconcile_dependencies` whose body fails the tasks waiting on a file and wakes the jobs blocked on them.

Good: `_fail_dependent_tasks`.

## Standard type-name suffixes

- Use `Builder` only for the GoF Builder pattern, where a product is assembled step by step through a builder interface. Otherwise name the type after what it creates (`Factory`, `Composer`, or the output).
- Use `Params`, not `Request`, for an object that groups arguments to a method or constructor. Reserve `Request` for real external or API requests.
- A factory exposes `create(params) -> X`. It does not expose one method per caller or use case with overlapping arguments. Choose a variant by what the type does, not by who calls it.

## One concept per module

A module holds one cohesive concept and is named after its domain purpose or its primary type.

- No bucket modules. Do not create `utils.py`, `helpers.py`, `common.py`, `shared.py`, `_utils.py`, or `_helpers.py`. Do not create a module or package named `contracts`.
- A well-named module is still a bucket if it defines a second, unrelated public class. Judge by contents, not by filename. A second public class may stay only if it is `_`-private to the primary type, or part of one family a reader would look for under this module's name.
- "The primary type builds it" does not make a second class part of the module. A `RetryBackoffPolicy` that a `NotificationDispatcher` creates in `__init__` is its own concept and belongs in its own module, even if the dispatcher is its only caller.
- A `models.py` is acceptable only for a tight family of passive shapes with no behavior. Split it if it mixes output schemas, dependency/context classes, input builders, validators, formatters, or persistence code.
- Do not split one concept across one-symbol files. A behavior-bearing type's own parameter and result shapes, used by nothing else, live in that type's module. A `*_params.py` or `*_result.py` whose only user is one type's method signature is the defect.
- A value several peer types share is its own concept. It does not move into any one peer's module.
- All variants of a discriminated union live in one module named after the union alias.

Bad: `retry_attempt_policy.py`, `retry_attempt_params.py`, `retry_attempt.py`, each with one symbol, where the params and result exist only for the policy's one method.

Good: `retry_attempt_policy.py` holds `RetryAttemptPolicy`, `RetryAttemptParams`, and `RetryAttempt`.

## `__all__` only in `__init__.py`

Only a package `__init__.py` (or a `.pyi` stub) may define `__all__`. Flag `__all__` in any other module. Mark a private symbol with a leading underscore instead.

## Every loose function has an owner

A public module-level function needs a reason not to be a method. Place it by what it does:

- Constructs one return type: a `classmethod` or factory method on that type.
- Interprets one instance's own data: an instance method on that type.
- Coordinates several peer types: a small domain service named after the operation.
- Formats or adapts for another subsystem: a type named after the target, such as `InvoicePresenter` or `ShipmentComposer`.

Keep it module-level only when no type would be more coherent with it as a method.

## Behavior lives on the type whose data it reads

A `@staticmethod`, a method that ignores `self`, or a free function whose body reads only one parameter's own fields belongs on that parameter's type. This covers sort keys, formatted lines, derived properties, and comparisons. Where the helper currently lives does not matter.

Bad:

```python
class InvoiceSummaryComposer:
    def _sort_key(self, line: InvoiceLine) -> tuple[str, int]:
        return (line.sku.casefold(), line.position)
```

Good:

```python
@dataclass(frozen=True)
class InvoiceLine:
    sku: str
    position: int

    def __lt__(self, other: "InvoiceLine") -> bool:
        return (self.sku.casefold(), self.position) < (other.sku.casefold(), other.position)
```

- Behavior that reads only the type's own fields is intrinsic. Keep it on the type.
- Behavior that queries or traverses other types is a service. Extract it to a named domain service.
- Rendering for another subsystem belongs to that subsystem's formatter, not to the data type.
- If a formatter type already owns a rendering, a second site must call it, not re-derive the same output inline. If the formatter lacks a needed variant, extend the formatter.

## Types live with their producer

A type lives in the package whose code constructs it: instantiates it, returns it, raises it, or subclasses it. The number of packages that import it does not move it.

- Group a package's passive shapes into concept-named modules (a union family in one file, an enum and its small companions in another). Do not group them by construct kind.
- A type many packages depend on lives in a low-level package that imports no sibling package.
- Dependency and context classes live beside the stage or service that consumes them, not beside output schemas.
- A validator stays on its model only for intrinsic invariants: required field combinations, normalized fields, allowed ranges. Validation that needs runtime dependencies, registries, stored data, or peer collections belongs to the service that has that context.

## Threaded state models get their own module

A type that is accumulated, reduced, merged, or checkpointed across a workflow or graph run gets its own module named after it, even with no methods. The test: does the system act on it over time (own module), or pass it once across a boundary (passive shape)?

This applies to the state model only. Place each field type by its own producer. A field type that only wraps an identity another type already owns should not exist; use the identity as a plain field.

## Package cohesion

Modules that form one pipeline or feature belong in one package. A reader should be able to guess a concept's package from its responsibility. Flag:

- One flow split across sibling packages that import sideways into each other.
- A package that only re-exports another package's symbols.
- A module (such as a registry or builder) that sits outside the package owning its concept.
- A package of unrelated single-purpose modules.

## Package public interface

- Code outside a package imports from the package root: `from billing import InvoiceTotal`, not `from billing.invoice_total import InvoiceTotal`.
- Code inside a package imports its siblings by direct submodule path (`from .invoice_total import InvoiceTotal`), never through its own package root.
- When importing through another package's root would create a cycle, import the specific leaf module instead.
- Keep `__init__.py` free of eager heavy imports.

## One responsibility per type

A type has exactly one reason to change. Two unrelated reasons is already a violation, whatever the size.

- Group the methods by what change would force each to change. One group: keep. Two or more unrelated groups: split into focused services or value objects, one per concern.
- Size is not the test. A large cohesive class is fine. A small two-method class serving two unrelated concerns is not.
- A frozen value object with no injected collaborators is not a god object. Methods that read only its own immutable fields are its behavior, even if they fall into several topics. Do not split them out.
- A very long entry method (such as a 100-line `execute()`) or repeated `isinstance` branching across sibling methods: extract an orchestrator or per-shape handlers so the entry method reads as named steps.
- A function with several responsibilities is a class. Signs: a conjunction name (`fetch_and_validate`), a long list of unrelated collaborator arguments, or sibling functions that all take the same arguments. Promote it to a type whose fields are the collaborators and whose methods are the steps.

## Types model real domain concepts

- Do not wrap a bare identity. A type that only wraps an existing key or id, with no behavior or invariant, should be replaced by the key itself.
- Do not model an `XCreate` type for the act of creating something. Group a factory's arguments in a `...Params` object beside the factory method.
- Do not store a copy of a value another object in hand already owns. Read it from the owner. This includes a strategy carrying a `kind` attribute equal to the key it is registered under.
- A stored record that crosses a queue, workflow, or graph boundary is passed by its id and re-fetched on the other side, not copied into a travelling object.
- Promote a bare `dict`/`list`/`set` to a named index type when it is queried with the same idiom at three or more sites, when two collections index the same data different ways, or when the build loop has a silent last-writer-wins or merge rule. The index owns the lookups and the collision policy, and builds itself with a `classmethod`.

## Parse boundary data once

Untyped data entering from outside (`dict[str, Any]`, `list[str | int]`, a positional tuple, a third-party error format, external JSON) is parsed once, at the seam where it enters, into a named frozen value object. Domain code uses that type, never the raw shape.

Signals of in-place interpretation:

- Index arithmetic on an untyped sequence: `loc[2:]`, `parts[0]`, `isinstance(x[-1], int)`.
- The same raw layout read in more than one method.
- `isinstance` used to decide what a raw segment means.
- A foreign primitive type passed several calls deep into domain methods.

## Map between models field by field

When converting one typed model into another, assign each field explicitly. Do not round-trip through a dict: `Target(**dataclasses.asdict(source))`, `Target.from_dict(source.to_dict())`, or a list of dumped dicts fed into another model's field. Serializing to a dict is fine only when the dict is the destination (JSON, a database column, a wire payload).

When one source type is mapped into more than one target, give it one dedicated mapper class that does the explicit field mapping, and have every target delegate to it. A single-target mapping stays inline.

## No dead code

Every production symbol must have a production reference. Search the whole repository before reporting. Orphan shapes:

- Referenced only by its own definition.
- Referenced only by tests. Either delete it with its tests or wire it into production.
- Referenced only by an `__init__.py` re-export.
- An unused method on a live type, such as a stale `with_*` copy helper or factory.
- A package directory whose only file is a code-less `__init__.py`. An empty `__init__.py` beside real modules is correct.

A symbol is live if reached dynamically: decorator registration, route or handler registries, string-keyed dispatch, framework configuration, entry points, or use within its own module.

## No duplicate logic

Two function or method bodies that are near-identical copies are one concept. Keep one implementation with one parameter order and point both callers at it. Copies with different signatures (for example, the first two parameters swapped) are the worst case.

## No overlapping responsibility

Two differently named types must not both own the same concept, such as a `Service` and a `Factory` with the same `create_*` surface, or two views computing the same projection. The bodies need not match. Search for sibling types with the same role and domain noun.

Two passive shapes with identical fields are not overlap when they sit at different boundaries, are mapped explicitly at a seam, and change for independent reasons. Flag only when they share one reason to change.

## Do not re-implement orchestration

When a component already runs a multi-step pipeline (a graph you invoke, a resolver that chains stages, a service with one `run()`), callers invoke it as a unit. A method body that calls two or more pipeline stages in sequence, passing one's output into the next (`capture` then `resolve`, `plan` then `apply`, `extract` then `validate`), is the sign. Search for any component that already calls those collaborators in that order. If the owner lacks the entry point a caller needs, add a narrow one to the owner; do not copy its steps.

## One responsibility per function

- If a method's description needs "and" (fetches and decides, parses and looks up), split it. This holds for short, simple methods too.
- Replace branching that maps inputs to outputs, or repeats one pattern with different values, with data-driven dispatch (a dict lookup, an ordered tuple, iteration over metadata).
- Do not extract a helper that is an arbitrary chunk of the original with no conceptual identity.
- Do not use `**kwargs` to reduce a parameter count.
- Do not write a wrapper that forwards all its parameters to another API.
- Group parameters into a dataclass only when the group is a concept you would store, pass on, or test as a unit. A parameter object built at the call site and unpacked at once is indirection.

## Constructor state over repeated arguments

Arguments that every caller passes with the same values (providers, strategies, registries, formatters) are the object's dependencies. Take them in `__init__`; method signatures hold only per-call data.

## Pass only what a collaborator needs

Do not hand a wide context object to a collaborator that reads a few of its fields. Build a narrow `...Params` at the call site. Do not add a `build_params()` method to the context object for each consumer.

## No anonymous tuples or dicts for concepts

- A method returning a `tuple` of answers to different questions does too much. Return a named type, or return the fetched data and let callers ask each question separately.
- A helper whose whole body is `return {...}` or `return (...)` packing its own arguments under the same names is not an abstraction. Inline the literal, or define a named type if the shape recurs and means something.
- A single-call-site function whose whole body is `[f(x) for x in xs]` over an already-named `f` should be inlined. Keep it if it filters, sorts, deduplicates, handles errors, or is used at many sites.

Bad:

```python
def _evaluate_order(self, order_id: str) -> tuple[str | None, bool]:
    order = self._fetch(order_id)
    return self._rejection_reason(order), bool(order.holds)
```

Good:

```python
@dataclass(frozen=True)
class OrderReview:
    rejection_reason: str | None
    is_on_hold: bool
```

## No branch-and-accumulate loops

A loop that branches to compute a per-item result and append it to a shared list mixes mapping one item with iterating. Extract the body to a function that returns one result (each `continue` becomes `return`) and use a comprehension. An `if`/`elif`/`else` that appends in every branch is the same defect.

Not a violation: a single filtering guard, or a loop with real cross-item state (running totals, dedup sets).

## One way to specify each input

A function accepts one form for each input.

- No two mutually exclusive parameters for the same value reconciled by a guard (`if a is None and b: a = derive(b)`).
- No deriving one input from another inside the function.
- A single default (`x or default`) and `**overrides` passed untouched to one typed target are fine.

Take the already-derived value and move the derivation to the call site. A separate derivation helper is allowed only if it reads a value the source already holds (`catalog.price_index`). It must not run a construction backwards: if production builds `Shipment(parcels=[...])`, a helper that builds shipments from a registry of parcel keys is the defect.

## No pre-derived arguments

A call must not pass both a value and the input it was derived from: `quote(lines=select_lines(cart, ctx), context=ctx)`. Move the derivation into the callee, which takes `ctx` and computes `lines` itself.

## Comments and docstrings

- Treat a comment as a sign the code is unclear. Fix the name or structure instead. Keep a comment only for a reason no structure can hold, such as a hidden external constraint.
- Apply the same test to docstrings. Delete a docstring that restates the body or props up a vague name, and rename instead.
- Do not narrate logic with inline comments; extract a well-named helper.
- Do not put comments in test files.
- Do not document what the code does not do or used to do.

## `Any`

Do not use `Any` unless the type cannot be determined or the code interfaces with untyped third-party code.

## `StrEnum` vs `Literal`

- `StrEnum` when code branches on the value or uses it as a dict or registry key.
- `Literal["x"] = "x"` as the fixed tag on one variant of a discriminated union.
- `Literal["a", "b"]` for a constrained field nothing branches on.

## Discriminated unions are explicit

- Tag every variant with a `kind: Literal[...]` field and declare the union as discriminated on that tag. Never rely on inferring the variant from field shape.
- Define a union's variant classes together, next to the alias, with no unrelated types between them. For nested unions, define the inner union first.

## Typed registries for dispatch

When a class takes a `dict[str, Callable]` for dispatch, wrap it in a named registry class with a `resolve` method and take the registry instead.

## Trust established invariants

Do not re-check a fact already guaranteed upstream. Such a guard can never fire. The guarantee may come from:

- Dispatch routing: a registry already chose this handler by the value's tag.
- An enclosing branch: an outer check already narrowed the value.
- A collaborator's return contract: a result that is non-empty only for one variant.

Narrow at the contract instead. Make the handler generic over its variant so its type carries the guarantee, or move the dependent branch inside the check that establishes it. Put the one `Any` at the registry dict, not in handler bodies.

Bad:

```python
class RefundHandler:
    def handle(self, request: PaymentRequest) -> PaymentResult:
        if not isinstance(request.payload, RefundPayload):
            raise TypeError("RefundHandler requires a refund payload")
        ...
```

Good:

```python
class RefundHandler:
    def handle(self, request: PaymentRequest[RefundPayload]) -> PaymentResult:
        ...
```

Validation of input the code received (an unknown key or id) is not covered by this rule.

## Enum usage

- Do not call `.value` on a `StrEnum` or `IntEnum` member.
- Where a parameter, field, dict key, or argument is typed as an enum, pass the member (`OrderStatus.CANCELLED`), never a bare literal (`"cancelled"`). This holds in tests too.

## One home for defaults

A field's default is declared once, on the owning type. Callers omit it rather than supply it. A fallback in a consumer (`x or uuid4()`, `x if x is not None else default`) that duplicates a default the type could declare is a default in the wrong place. A type that defaults one field but leaves a sibling required, while a consumer fills in that sibling, is the clearest case.

## A supplied value's form matches its role

- Omit a value that is irrelevant to the case.
- Use a fixed literal when the code asserts or branches on that exact value.
- Use a real created record's id when the code reads, joins, or correlates on that id. Never pass a fresh `uuid4()` there.

## Interfaces must earn their existence

A `Protocol` or `ABC` is justified when it inverts a real dependency, or when two or more implementers exist today. Either alone is enough.

- A lower-level package that defines a narrow `Protocol` for what it needs, instead of importing a higher-level concrete type, is correct even with one implementer.
- Test: would retyping the consumers against the concrete type create an import cycle? Yes: keep. No: delete the interface.
- A planned second implementer does not justify an interface.
- An interface belongs in the package that depends on it.
- A `Protocol` must be designed from the consumer's needs. Do not write a `Protocol` whose members are just the attributes the consumer happens to read off one wide object. Sign: its members match a slice of one concrete class one-for-one and no other type was built to satisfy it. Pass a parameter object with exactly what the consumer needs instead.
