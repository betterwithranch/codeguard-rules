# Architecture rules, by priority

The architecture rules to build, each standing on its own, in the order they are built.
Each follows codeguard's `writing-rules` skill (0.8.0): one convention stated as one
abstract declarative sentence that code keeps or breaks; examples only illustrate it;
eval cases never reuse a skill example; idiomatic code never breaks it; each code shape
breaks at most one rule. A judge skill is laid out as the convention, definitions,
`## Violation`, the forms on both sides, `## Not a violation` and `## Why`.

## How the order is set

Two measures, each high, medium or low:

- **Accepted**: how widely the convention is accepted. High: a mainstream source states
  it and few dispute it. Medium: known, with real dissent or narrower reach. Low: a house
  convention, or one mainstream advice argues against.
- **Protects**: how much poorly designed code it keeps out. High: it stops a structural
  flaw that spreads (one change needing many edits, hidden coupling, wrong results far
  from their cause). Medium: a local design flaw. Low: readability or a local slip.

High on both is the strongest candidate. Within a tier, the rule protecting more comes
first. The Accepted column names its source; these ratings are judgment, open to change.

Ratings are for Python, the language this package's rules are written for. The **Other
languages** column notes where a rule doesn't apply, or is accepted or protects less (or
more), so a later package for that language re-rates it instead of copying the order.
"Universal" means no language changes it.

## The order

| # | Rule | Convention | Tool | Accepted | Protects | Why | Other languages | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | `knowledge-stated-once` | Each piece of knowledge is stated once in the code. | LLM | High: DRY (Hunt and Thomas, *The Pragmatic Programmer*) | High | Two copies change separately, so they come to disagree | Go: medium; its proverb "a little copying is better than a little dependency" accepts small repeats across packages | Covers repeated steps, private siblings differing only by a value, a stage sequence repeated outside its pipeline, a collection repeating another declared set's members, two passive shapes modelling one outside thing, and a module function copying a method the type already has. Consistency kind: the search is the file and the modules it imports. Not a copy: bodies differing in a step; public methods with distinct names. The rule is about knowledge, not alike text, which answers "duplication is cheaper than the wrong abstraction" (Metz): two alike bodies that would change for different reasons are not a violation. The widest rule: its eval keeps a case per form on both sides, and wavering on one form splits that form out |
| 2 | `domain-decision-without-io` | A domain decision is made in code that does no I/O. | LLM | High: dependency inversion (Martin); hexagonal architecture (Cockburn); functional core, imperative shell (Bernhardt) | High | A decision tangled with I/O can only be tested by faking the I/O, and it changes whenever the infrastructure does | Universal. Haskell and other effect-typed languages enforce it through types, so a rule adds little there | I/O: a database, HTTP, file, clock, random source or queue. A handler, view or task that reads, calls the decision, then writes is the shell and keeps the rule. A function deciding and doing I/O is this rule's, never `one-job`'s. An active-record model method (Django, SQLAlchemy) that only reads its own loaded fields does no I/O |
| 3 | `one-job` | A function or class does one job. | LLM | High: single responsibility (Martin); Divergent Change (Fowler, *Refactoring*) | High | Each job changes for its own reason; together, every change risks the other | Universal | A function that only calls one helper per job does one job, orchestration. A domain decision mixed with I/O is `domain-decision-without-io`'s. Expect wavering on short view functions; the eval needs clear cases on both sides |
| 4 | `type-dispatch-in-one-place` | Behaviour chosen by a value's type is chosen in one place. | LLM | High: Repeated Switches (Fowler, *Refactoring*); open/closed (Meyer, Martin) | High | A new type then needs every switch found and changed | Lower protection where the compiler checks a match on a closed union for exhaustiveness (Rust, Haskell, OCaml, Scala, TypeScript with a `never` check): a new variant breaks the build at every switch. Repeated matches are idiomatic there | Covers open/closed's usual break. In Python the same exhaustiveness exists for a `match` on a closed union under basedpyright's check; whether that is a violation is settled when the rule is written |
| 5 | `domain-answer-with-its-data` | A domain answer computed from one type's data lives in that type's module. | LLM | High: Feature Envy (Fowler, *Refactoring*); information expert (GRASP) | High | The answer belongs with the data it reads, where the type's next change will see it | Functional languages (Elixir, Clojure, Haskell) keep data and functions apart by design; the rule holds there only as "in the type's module", never "a method on the type" | When the type already has that method, the function is a copy: `knowledge-stated-once` |
| 6 | `failures-reported` | A failure, missing data or an impossible state is reported where it's found, never turned into a normal-looking result. | LLM | High: fail fast (Shore); errors never pass silently (PEP 20) | High | The problem turns into a wrong result far from its cause, found later, if ever | Universal. In Go the form is a discarded or defaulted `err`; in Erlang and Elixir "let it crash" is the same rule | Covers a handler that carries on (returns a default, passes, continues, breaks or only logs), a fallback standing in for data that should exist, a clamp hiding a state the rules say can't happen, a collection build silently dropping items. A caller-supplied default for a program type's field is `construction-in-its-home`'s. ruff E722, BLE001, S110 and S112 cover the plainest handlers in the app's linter |
| 7 | `per-use-data-not-shared` | Data belonging to one call or use is kept where only that call or use sees it. | LLM | High: shared mutable state (Python's thread-safety guidance; Effective Python) | High | One use's data leaks into the next, and concurrent uses corrupt each other | Rust: low protection; the borrow checker rejects most shared mutation. Haskell: doesn't apply | Covers module-level state holding one call's data, and a shared instance (module level, class attribute, cached factory) storing each use's results on itself. ruff B008, RUF009 and B006 cover defaults in the app's linter |
| 8 | `subclass-keeps-base-promises` | A subclass keeps every promise its base class makes. | LLM | High: Liskov substitution (Liskov, Martin); Refused Bequest (Fowler, *Refactoring*) | High | A caller written against the base breaks on the subclass, far from the override that broke it | Go and Rust have no class inheritance; there it applies only to interface and trait implementations | Breaking forms: an override that raises where the base doesn't, ignores an argument, accepts less or returns more loosely, or stubs an inherited method. The judge checks it when the base is in the file or the diff; a base elsewhere waits for the language-server tier. Owns the stub shape, so `inherit-only-from-a-kind` doesn't flag it |
| 9 | `one-owner-per-job` | One type owns each job on a concept. | LLM | Medium: Shotgun Surgery (Fowler, *Refactoring*); information expert (GRASP) | High | Two owners of one job each get half the fixes | Universal | Consistency kind: names its search. Building an instance is `construction-in-its-home`'s |
| 10 | `construction-in-its-home` | What a new instance holds is decided by its type, its module, its factory or its source's mapper. | LLM | Medium: Creator (GRASP); factories (*Design Patterns*) | High | How a type is built changes with the type; built inline in many places, each copy needs the change | Go: high; a `NewX` constructor in the type's package is the convention | Includes a caller supplying a default for a field. Not a violation: raising an exception; returning a result built from values the function computed; a Django or SQLAlchemy model created in a view or handler, a framework idiom. Each gets a `valid` eval case. Four homes to tell apart: watch its evals for wavering |
| 11 | `no-forbidden-field-combinations` | A type's fields can't hold a combination the domain forbids. | LLM | Medium: make illegal states unrepresentable (Minsky); parse, don't validate (King) | High | Every reader must re-check the combination, and the one that forgets acts on an impossible state | High acceptance where sum types are cheap (Rust, Haskell, OCaml, F#, TypeScript). Go: low; without sum types the fix costs more than it buys | The usual form: optional fields whose valid combinations depend on a status or kind field. Python's fix is a union of shapes, one per state. Not a violation: fields that are independently optional |
| 12 | `inherit-only-from-a-kind` | A class inherits only from a type it is a kind of. | LLM | High: favour composition over inheritance (*Design Patterns*); Replace Superclass with Delegate (Fowler) | Medium | Inheriting to reuse code binds the subclass to every change in a parent it isn't a kind of | Doesn't apply to Go or Rust, which have no class inheritance | Framework base classes (Django `Model`, `View`, pydantic `BaseModel`, `Exception`) and mixins a framework documents are kinds. A subclass that stubs inherited methods is `subclass-keeps-base-promises`'s |
| 13 | `no-forwarding-class` | A class does more than forward every method to one collaborator. | ast-grep | High: Middle Man (Fowler, *Refactoring*) | Medium | A layer that adds nothing is one more place to read and change | Go: an adapter that satisfies an interface by forwarding is idiomatic; exempt it there | Prototype first: tying every method to one collaborator may be beyond ast-grep metavariables. If it is, match a narrower form |
| 14 | `no-derivable-stored-value` | A class doesn't store a value it can derive from one other value it holds. | LLM | High: single source of truth; normalization | Medium | Two values that must agree drift apart when one is updated and the other isn't | Universal | Covers its own fields and a held object's. Not a violation: a value derived from several sources; a key kept without its object; an ORM foreign key beside its relationship, a framework idiom |
| 15 | `one-writer-per-module-state` | Module-level state has one writer. | LLM | High: global mutable state | Medium | With two writers, neither owns the value, and each write can undo the other | Rust (mutable statics need `unsafe`) and Haskell: doesn't apply | ruff PLW0603 is stricter (it also flags a lazy cache one function owns) and an app may choose it |
| 16 | `names-claim-only-what-body-does` | A name claims nothing its body doesn't do. | LLM | High: avoid disinformation (Martin, *Clean Code*) | Medium | Readers trust names; a false one sends them wrong | Universal | |
| 17 | `records-cross-queues-as-ids` | A stored record crosses a task or queue boundary as its identity. | LLM | High: Celery's task guidance (pass ids, not database objects) | Medium | The record is stale by the time the task runs; pass its id and reload it | Universal where jobs are queued; Ruby's Sidekiq documents the same | |
| 18 | `collaborators-through-constructor` | A method's collaborators come through its object's constructor. | LLM | Medium: dependency injection (Fowler; Seemann). Python practice often prefers module imports patched in tests, and DI containers are rare | Medium | Every caller then has to find the collaborator; through the constructor, it's wired once | Java, C#, Kotlin, TypeScript (Angular, NestJS): high, built into Spring, .NET and those frameworks. Go: high for explicit constructor injection, without containers. Ruby: low; Rails culture rejects it. Functional languages: doesn't apply as written; collaborators are function arguments | |
| 19 | `result-parts-named` | A function's result names what each of its parts means. | LLM | Medium: named tuples and dataclasses over bare tuples (Effective Python) | Medium | Nothing checks a part's meaning, so a caller that reads it wrong passes | Go: a `(value, err)` pair is idiomatic and never a violation | A pair whose meaning is the type's own (a coordinate) is not a violation |
| 20 | `validator-depends-on-its-data` | A data model's validator depends only on the model and its input. | LLM | Medium: pydantic documents validation `context`, against it | Medium | A model's validity should depend only on its data, so it parses the same anywhere and its tests need no setup | Written for pydantic; other languages' validation libraries need their own wording | Flags pydantic's validation `context` on purpose; the Why says so. Django's `Model.clean()` checking uniqueness by query is a framework idiom and exempt |
| 21 | `no-recheck-of-guaranteed-condition` | A check doesn't re-test a condition earlier code already guarantees. | LLM | Medium: parse, don't validate (King) | Medium | A re-check says the guarantee can't be trusted and hides which layer owns it | Lower protection where the type system already narrows (Rust, TypeScript): fewer re-checks get written | Covers an earlier raise or return, and a validator's constraint. A condition only an annotation guarantees is basedpyright's |
| 22 | `unions-parsed-by-tag` | A parsed union's parser picks each variant from one unique tag. | LLM | Medium: pydantic's discriminated unions documentation | Medium | Without a tag the parser tries each variant in turn: slower, and its errors name every variant | TypeScript (zod's `discriminatedUnion`) and Rust (serde's tagged enums): same | Covers every parsing library. A union the program builds itself and tells apart by class is not a violation |
| 23 | `take-what-you-read` | A function takes the values it reads, not a bundle it mostly ignores. | LLM | Medium: Law of Demeter; tramp data; interface segregation at the function level | Medium | The function claims to need the whole bundle, so its tests must build it all | Universal | Framework-injected parameters are exempt. Owns a parameter the function mostly ignores; reaching through a value the function does use is `no-reach-through`'s |
| 24 | `module-holds-one-concept` | A module's public classes belong to its one concept. | LLM | Medium: package by feature; cohesion | Medium | Knowledge grouped by kind is found by guessing; grouped by concept, it sits where its next change will look | Java: doesn't apply at the file level, where one public class per file is enforced; it applies to packages | Framework-convention modules are exempt: Django's `models.py`, `admin.py`, `forms.py`, `serializers.py`, FastAPI's `schemas.py` |
| 25 | `packages-under-import-contract` | A package the change adds is in an import-linter contract that keeps its siblings from importing each other. | LLM | Medium: layered architecture; import-linter's independence contracts | Medium | Mutual imports make two packages one unit; import-linter enforces the contract, so this rule only checks a new package is under one | import-linter is Python's. The convention carries over with that language's tool: ArchUnit (Java), dependency-cruiser (TypeScript), depguard (Go) | Checks the project's import-linter configuration, never the imports themselves. Applies only where the project configures import-linter |
| 26 | `command-or-query` | A function either changes state or returns an answer, not both. | LLM | Medium: command–query separation (Meyer). Common idioms break it | Medium | A caller can't ask without changing something, so reading becomes risky | Eiffel: high. Go: a command returning only `err` keeps it | Not a violation: `pop`, `setdefault`, and a create returning the new identity, idioms. A command returning its result for chaining is a builder |
| 27 | `no-reach-through` | A function doesn't reach through one object into another's parts. | LLM | Medium: Law of Demeter; Message Chains (Fowler). Its strict "one dot" form is widely disputed | Medium | The function depends on how every object along the chain is built, so changing any one of them breaks it | Fluent and pipeline APIs are exempt everywhere: Rust iterators, LINQ, pandas, query builders | Reaching into a value object's own data, and into a framework's request or settings object, is not a violation |
| 28 | `names-say-main-action` | A name says what its body mainly does. | LLM | High: intention-revealing names (Martin, *Clean Code*) | Low | A vague name sends readers to the body | Universal | Covers a creation method named for its caller |
| 29 | `one-verb-per-operation` | One operation goes by one verb. | LLM | High: one word per concept (Martin, *Clean Code*) | Low | One operation under two verbs reads as two operations | Universal | Consistency kind |
| 30 | `no-class-level-mutable-container` | A class-level mutable container isn't mutated through `self`. | ast-grep | High: a known Python pitfall | Low | Every instance shares the one container | Python's. Ruby's class variables have the same pitfall | A class body binding a list, dict or set, and a method mutating it through `self`. A syntactic form of `per-use-data-not-shared`; `warning` severity so the judge rule still runs. Replaces RUF012, which checks the annotation, not the mutation |
| 31 | `comments-state-outside-facts` | A comment or docstring states a fact from outside the code. | LLM | Medium: comments explain why (Martin, *Clean Code*); docstring conventions disagree | Low | A comment restating code goes stale with it; one giving an outside reason is the only kind the code can't replace | Lower where every exported item needs a doc comment: Go's linters and Java's Javadoc convention; the rule then covers inline comments only | Commented-out code and bare TODOs are ruff's (ERA001, TD003) |
| 32 | `in-file-union-discriminator` | A field typed as a union of pydantic models defined in the file declares a discriminator. | ast-grep | Medium: pydantic's discriminated unions documentation | Low | As `unions-parsed-by-tag` | pydantic only | The syntactic form of `unions-parsed-by-tag`; `warning` severity so the judge rule still runs |
| 33 | `no-value-with-its-source` | A call doesn't pass a value together with the input it was derived from. | LLM | Low: no mainstream source names it | Medium | The callee can derive it; passing both lets them disagree | Universal | |
| 34 | `threaded-state-own-module` | A workflow's threaded state has a module of its own. | LLM | Low: house convention | Low | Every step depends on the state; kept apart, the steps import it without importing each other | Universal | A module of one class and functions passes `module-holds-one-concept` |
| 35 | `builder-has-parts` | A `...Builder` class has part methods before `build()`. | ast-grep | Low: Builder pattern (*Design Patterns*), but naming is loose in practice | Low | A builder that makes its product in one call is a constructor with a misleading name | Java and Rust: medium; builders are common there and the name is used strictly | |
| 36 | `identifier-wrapper-earns-its-type` | A class that holds one identifier adds behaviour or a check. | ast-grep | Low: Primitive Obsession (Fowler) advises the opposite | Low | A wrapper with no behaviour or check adds a type to learn and protects nothing | Rust, Haskell (newtypes), TypeScript (branded types) and F#: doesn't apply. There a bare wrapper is idiomatic, because the type checker stops one id passing for another | Matches a class named `...Id`, `...Key` or `...Code` with one field, and a `str`, `int` or `UUID` subclass with an empty body. Exempt Django and SQLAlchemy models and enums. Candidate to drop: mainstream advice favours such wrappers, and Python's `NewType` gets the same check from basedpyright |

The first rule to build is `knowledge-stated-once`.

## Waiting for the language-server tier

Each needs a lookup across the repository that a language server answers. Ranked when
codeguard can run them.

| Convention | Note |
|---|---|
| A protocol or abstract base asks for only what each of its users needs. | Interface segregation (Martin). Needs every user and implementer |
| An interface has two implementers or breaks an import cycle. | The cycle exemption is an import-graph lookup |
| A protocol does more than mirror one class's data attributes. | Needs the classes that match it |
| A map wrapper has more than one call site. | |
| A passive shape used by one type lives with that type. | |
| A type lives in the package that produces it. | |
| A context type lives in its consumer's package. | |
| An interface lives in its consumer's package. | |
| A request- or action-named type does more than group an in-process call's arguments. | Needs where the type is built and read |

`subclass-keeps-base-promises` also gains its cross-module form here: an override whose
base class is in another module.

## Left to a linter

Out of scope: codeguard is the layer for what a linter can't decide, and linter
settings belong in the app's own configuration. Noted so the claims aren't rebuilt.

| Claim | Linter |
|---|---|
| A call in a function or dataclass default, or a mutable default | ruff B008, RUF009, B006 |
| A `global` statement rebinds module state | ruff PLW0603 |
| A bare or blind `except`, or one whose body is `pass` or `continue` | ruff E722, BLE001, S110, S112 |
| Commented-out code, a TODO with no tracker link | ruff ERA001, TD003 (not FIX002: it flags every TODO) |
| Packages import each other in a cycle (acyclic dependencies, Martin) | import-linter contracts; pylint `cyclic-import` |
| Code reads another object's `_private` attributes (information hiding, Parnas) | ruff SLF001 |
| A boolean flag argument selects behaviour (Fowler, Remove Flag Argument) | ruff FBT001–FBT003 |
| A function takes too many parameters (Long Parameter List, Fowler) | ruff PLR0913 |

## Dropped

| Claim | Reason |
|---|---|
| Code branches on a `Literal` value set instead of an enum | `match` on a `Literal` with basedpyright's exhaustiveness check is idiomatic. It came from otter's skill with no recorded reason; it comes back if one turns up |
| A function builds an argument group only to unpack it into one call | Rare; minor |
| A union's variants are not one run directly before its alias | Layout style |
| Modules split by execution phase handle the same concept | Narrow, and needs reading every phase module |
| A loop works out each item's result through a branch and collects it | Style; the live pattern rule `no-append-in-every-branch` covers its plainest form |
| A reference is given a fresh generated id or a made-up literal | Rare in app code; the test-side form is `real-test-data`'s |
| A matched value is given a random value | Rare |

## Gates

The gates `tag-value`, `union-alias-module`, `unpacked-argument-group` and
`accumulating-loop` served only dropped claims and are removed with them.
`literal-annotation` stays for `unions-parsed-by-tag`; `reference-id` stays for the test
draft `real-test-data`. Each rule's trigger is chosen when it is written, starting from
the gates in `python/drafts/bindings/`.

## Count

36 rules to build (31 judge, 5 pattern), 9 waiting for the language-server tier, 8 left
to a linter, 7 dropped. The test drafts are planned after these.
