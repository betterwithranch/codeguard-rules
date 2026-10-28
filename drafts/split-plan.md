# Architecture rules, by priority

The architecture rules to build, each standing on its own, in the order they are built.
Each follows codeguard's `writing-rules` skill (0.8.0): one convention stated as one
abstract declarative sentence that code keeps or breaks; examples only illustrate it;
eval cases never reuse a skill example; idiomatic code never breaks it; each code shape
breaks at most one rule. A judge skill is laid out as the convention, definitions,
`## Violation`, the forms on both sides, `## Not a violation` and `## Why`.

## Levels

codeguard is language-agnostic, and the baseline is three levels: **general**
(architecture conventions that hold in any language), **Python** and **TypeScript**
(otter uses both). A rule lives at the level its convention belongs to:

- **General**: one judge rule in the `general` ruleset. Its `SKILL.md` holds the
  convention, definitions, `## Violation`, `## Not a violation` and `## Why`, in no
  language's terms. Each language it applies in adds a supplement beside it
  (`python.md`, `typescript.md`) with that language's forms on both sides and its
  framework code that keeps the convention. The binding's `paths` name the languages by
  extension, and the one rule eval holds cases in each, which `codeguard eval` reports
  per language. A language where the rule doesn't apply is left out of its paths and
  gets no supplement, so the rule never runs there.
- **Python** or **TypeScript**: the convention itself is about that language or one of
  its libraries, in that language's ruleset. Every pattern rule is at a language level,
  since ast-grep matches one language; a general convention can have a pattern rule in
  each language for its syntactic forms.

This is codeguard 0.9's layout: codeguard gives ruleset names no meaning, so `general`
is a name, and per-language severity overrides don't exist. Only Python has change
kinds and gates so far: on a TypeScript file every trigger fires, and the judge gets
the changed lines without the code around them, so a general rule's TypeScript part is
judged with less context than its Python part until codeguard adds TypeScript gates.

## Names

A rule takes the conventional name of its principle, pattern or smell wherever one
exists: the principle's name (`dry`, `single-responsibility`), or a smell's name after
`no-` (`no-feature-envy`, `no-middle-man`). Where a canonical statement fits, the
convention uses its wording. A rule keeps a descriptive name only where no conventional
one fits: `construction-in-its-home`, `result-parts-named`,
`validator-depends-on-its-data`, `no-recheck-of-guaranteed-condition`,
`packages-under-import-contract`, `no-class-level-mutable-container`,
`union-declares-discriminator`, `no-value-with-its-source`, `threaded-state-own-module`
and `identifier-wrapper-earns-its-type`.

## How the order is set

Two measures, each high, medium or low, rated for the convention in general:

- **Accepted**: how widely the convention is accepted. High: a mainstream source states
  it and few dispute it. Medium: known, with real dissent or narrower reach. Low: a house
  convention, or one mainstream advice argues against.
- **Protects**: how much poorly designed code it keeps out. High: it stops a structural
  flaw that spreads (one change needing many edits, hidden coupling, wrong results far
  from their cause). Medium: a local design flaw. Low: readability or a local slip.

High on both is the strongest candidate. Within a tier, the rule protecting more comes
first. The Accepted column names its source; these ratings are judgment, open to change.

The **Python** and **TypeScript** columns say how the rule applies in each: "Applies"
when nothing changes, otherwise a different rating, the idioms its part must exempt, or
"Doesn't apply". **Other languages** notes the rest, for when they are added.

## The order

| # | Rule | Convention | Level | Tool | Accepted | Protects | Why | Python | TypeScript | Other languages | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `dry` | Every piece of knowledge has a single, unambiguous, authoritative representation within the system. | General | LLM | High: DRY (Hunt and Thomas, *The Pragmatic Programmer*) | High | Two copies change separately, so they come to disagree | Applies | Applies | Go: medium; "a little copying is better than a little dependency" accepts small repeats across packages | Covers repeated steps, private siblings differing only by a value, a stage sequence repeated outside its pipeline, a collection repeating another declared set's members, two passive shapes modelling one outside thing, and a module function copying a method the type already has. Consistency kind: the search is the file and the modules it imports. Not a copy: bodies differing in a step. Copies differing only in values, private or public, are copies: the convention decides, not the name. The rule is about knowledge, not alike text, which answers "duplication is cheaper than the wrong abstraction" (Metz): two alike bodies that would change for different reasons are not a violation. The widest rule: its eval keeps a case per form on both sides, and wavering on one form splits that form out |
| 2 | `domain-logic-separate-from-io` | A domain decision is made in code that does no I/O. | General | LLM | High: dependency inversion (Martin); hexagonal architecture (Cockburn); functional core, imperative shell (Bernhardt) | High | A decision tangled with I/O can only be tested by faking the I/O, and it changes whenever the infrastructure does | Applies. Exempt: an active-record model method (Django, SQLAlchemy) that only reads its own loaded fields | Applies | Haskell and other effect-typed languages enforce it through types, so a rule adds little | I/O: a database, HTTP, file, clock, random source or queue. A handler, view or task that reads, calls the decision, then writes is the shell and keeps the rule. A function deciding and doing I/O is this rule's, never `single-responsibility`'s |
| 3 | `single-responsibility` | A module, class or function has one reason to change. | General | LLM | High: single responsibility (Martin); Divergent Change (Fowler, *Refactoring*) | High | Each job changes for its own reason; together, every change risks the other | Applies | Applies. A React component that renders and also fetches is two jobs only when the fetch isn't a hook it calls | Universal | A function that only calls one helper per job does one job, orchestration. A domain decision mixed with I/O is `domain-logic-separate-from-io`'s. Expect wavering on short view functions; the eval needs clear cases on both sides |
| 4 | `no-repeated-switches` | Behaviour chosen by a value's type is chosen in one place. | General | LLM | High: Repeated Switches (Fowler, *Refactoring*); open/closed (Meyer, Martin) | High | A new type then needs every switch found and changed | Applies to class hierarchies and `isinstance` chains. A `match` on a closed union under basedpyright's exhaustiveness check: protects less, settled when the rule is written | Lower: a `switch` on a discriminated union's tag with a `never` exhaustiveness check is idiomatic, and the compiler finds every switch | Lower where the compiler checks exhaustiveness (Rust, Haskell, OCaml, Scala) | Covers open/closed's usual break |
| 5 | `no-feature-envy` | A domain answer computed from one type's data lives in that type's module. | General | LLM | High: Feature Envy (Fowler, *Refactoring*); information expert (GRASP) | High | The answer belongs with the data it reads, where the type's next change will see it | Applies | Applies as "in the type's module": types are often interfaces with functions beside them, not classes with methods | Elixir, Clojure, Haskell: as in TypeScript | When the type already has that method, the function is a copy: `dry` |
| 6 | `fail-fast` | A failure, missing data or an impossible state is reported where it's found, never turned into a normal-looking result. | General | LLM | High: fail fast (Shore); errors never pass silently (PEP 20) | High | The problem turns into a wrong result far from its cause, found later, if ever | Applies. ruff E722, BLE001, S110, S112 cover the plainest handlers | Applies. Forms include a `catch` returning `undefined` or a default, and `??` or `\|\|` standing in for data that should exist. ESLint `no-empty` and `@typescript-eslint/no-floating-promises` cover the plainest | Go: a discarded or defaulted `err`. Erlang, Elixir: "let it crash" is the same rule | Covers a handler that carries on (returns a default, passes, continues, breaks or only logs), a fallback standing in for data that should exist, a clamp hiding a state the rules say can't happen, a collection build silently dropping items. A caller-supplied default for a program type's field is `construction-in-its-home`'s |
| 7 | `no-shared-mutable-state` | Data belonging to one call or use is kept where only that call or use sees it. | General | LLM | High: shared mutable state | High | One use's data leaks into the next, and concurrent uses corrupt each other | Applies. ruff B008, RUF009, B006 cover defaults | Higher protection: one Node process serves every request concurrently, so module state leaks between users | Rust: low; the borrow checker rejects most shared mutation. Haskell: doesn't apply | Covers module-level state holding one call's data, and a shared instance (module level, class attribute or static, cached factory) storing each use's results on itself |
| 8 | `liskov-substitution` | A subclass keeps every promise its base class makes. | General | LLM | High: Liskov substitution (Liskov, Martin); Refused Bequest (Fowler, *Refactoring*) | High | A caller written against the base breaks on the subclass, far from the override that broke it | Applies | Applies to class inheritance and to a class implementing an interface | Go, Rust: no class inheritance; applies to interface and trait implementations | Breaking forms: an override that raises where the base doesn't, ignores an argument, accepts less or returns more loosely, or stubs an inherited method. The judge checks it when the base is in the file or the diff; a base elsewhere waits for the language-server tier. Owns the stub shape, so `composition-over-inheritance` doesn't flag it |
| 9 | `no-shotgun-surgery` | One type owns each job on a concept. | General | LLM | Medium: Shotgun Surgery (Fowler, *Refactoring*); information expert (GRASP) | High | Two owners of one job each get half the fixes | Applies | Applies | Universal | Consistency kind: names its search. Building an instance is `construction-in-its-home`'s |
| 10 | `construction-in-its-home` | What a new instance holds is decided by its type, its module, its factory or its source's mapper. | General | LLM | Medium: Creator (GRASP); factories (*Design Patterns*) | High | How a type is built changes with the type; built inline in many places, each copy needs the change | Applies. Exempt: a Django or SQLAlchemy model created in a view or handler | Lower: an object literal typed by an interface, built where it's used, is idiomatic; the rule covers a literal repeated for one type or one carrying defaults | Go: high; a `NewX` constructor in the type's package is the convention | Includes a caller supplying a default for a field. Not a violation: raising an exception; returning a result built from values the function computed. Each gets a `valid` eval case. Four homes to tell apart: watch its evals for wavering |
| 11 | `make-illegal-states-unrepresentable` | A type's fields can't hold a combination the domain forbids. | General | LLM | Medium: make illegal states unrepresentable (Minsky); parse, don't validate (King) | High | Every reader must re-check the combination, and the one that forgets acts on an impossible state | Medium: the fix is a union of dataclasses or pydantic models, one per state | High: discriminated unions make the fix cheap and idiomatic | Rust, Haskell, OCaml, F#: high. Go: low; without sum types the fix costs more than it buys | The usual form: optional fields whose valid combinations depend on a status or kind field. Not a violation: fields that are independently optional |
| 12 | `composition-over-inheritance` | A class inherits only from a type it is a kind of. | General | LLM | High: favour composition over inheritance (*Design Patterns*); Replace Superclass with Delegate (Fowler) | Medium | Inheriting to reuse code binds the subclass to every change in a parent it isn't a kind of | Applies. Exempt: framework base classes and documented mixins (Django `Model`, `View`, pydantic `BaseModel`, `Exception`) | Applies. Exempt: framework base classes (`Error`, NestJS and Angular bases) | Go, Rust: doesn't apply; no class inheritance | A subclass that stubs inherited methods is `liskov-substitution`'s |
| 13 | `no-middle-man` | A class does more than forward every method to one collaborator. | General, with a pattern rule per language | ast-grep | High: Middle Man (Fowler, *Refactoring*) | Medium | A layer that adds nothing is one more place to read and change | Pattern rule | Pattern rule | Go: an adapter that satisfies an interface by forwarding is idiomatic; exempt it | Prototype first: tying every method to one collaborator may be beyond ast-grep metavariables. If it is, match a narrower form |
| 14 | `single-source-of-truth` | A class doesn't store a value it can derive from one other value it holds. | General | LLM | High: single source of truth; normalization | Medium | Two values that must agree drift apart when one is updated and the other isn't | Applies. Exempt: an ORM foreign key beside its relationship | Higher acceptance: React's documentation calls derived state in `useState` an anti-pattern; the rule covers component state too | Universal | Covers its own fields and a held object's. Not a violation: a value derived from several sources; a key kept without its object |
| 15 | `single-writer` | Module-level state has one writer. | General | LLM | High: global mutable state | Medium | With two writers, neither owns the value, and each write can undo the other | Applies. ruff PLW0603 is stricter and an app may choose it | Lower: an exported `let` can only be reassigned in its own module; the rule covers mutation of an exported object | Rust (mutable statics need `unsafe`), Haskell: doesn't apply | |
| 16 | `no-disinformation` | A name claims nothing its body doesn't do. | General | LLM | High: avoid disinformation (Martin, *Clean Code*) | Medium | Readers trust names; a false one sends them wrong | Applies | Applies | Universal | |
| 17 | `claim-check` | A stored record crosses a task or queue boundary as its identity. | General | LLM | High: Celery's and Sidekiq's task guidance (pass ids, not database objects) | Medium | The record is stale by the time the task runs; pass its id and reload it | Applies (Celery, RQ) | Applies (BullMQ) | Universal where jobs are queued | |
| 18 | `constructor-injection` | A method's collaborators come through its object's constructor. | General | LLM | Medium: dependency injection (Fowler; Seemann); practice varies by language | Medium | Every caller then has to find the collaborator; through the constructor, it's wired once | Medium: module imports patched in tests are common, DI containers rare | Angular, NestJS: high, built in. Node and React without them: medium; modules imported directly are common | Java, C#, Kotlin: high (Spring, .NET). Go: high, without containers. Ruby: low. Functional languages: doesn't apply as written | |
| 19 | `result-parts-named` | A function's result names what each of its parts means. | General | LLM | Medium: named tuples and records over bare tuples (Effective Python) | Medium | Nothing checks a part's meaning, so a caller that reads it wrong passes | Applies | Lower: a tuple returned from a React hook (`[value, setValue]`) is idiomatic and exempt | Go: a `(value, err)` pair is idiomatic and exempt | A pair whose meaning is the type's own (a coordinate) is not a violation |
| 20 | `validator-depends-on-its-data` | A data model's validator depends only on the model and its input. | General | LLM | Medium: pydantic documents validation `context`, against it | Medium | A model's validity should depend only on its data, so it parses the same anywhere and its tests need no setup | Applies (pydantic validators and `context`). Exempt: Django's `Model.clean()` checking uniqueness by query | Applies (zod `refine` and `superRefine`, class-validator) | Universal where a validation library is used | Flags pydantic's validation `context` on purpose; the Why says so |
| 21 | `no-recheck-of-guaranteed-condition` | A check doesn't re-test a condition earlier code already guarantees. | General | LLM | Medium: parse, don't validate (King) | Medium | A re-check says the guarantee can't be trusted and hides which layer owns it | Applies. A condition only an annotation guarantees is basedpyright's | Lower: `@typescript-eslint/no-unnecessary-condition` covers what the types guarantee; the rule covers guarantees from earlier code and validators | Rust: lower, as TypeScript | Covers an earlier raise or return, and a validator's constraint |
| 22 | `discriminated-unions` | A parsed union's parser picks each variant from one unique tag. | General | LLM | Medium: pydantic's and zod's discriminated union documentation | Medium | Without a tag the parser tries each variant in turn: slower, and its errors name every variant | Applies (pydantic) | Applies (zod's `discriminatedUnion`) | Rust: serde's tagged enums | A union the program builds itself and tells apart by type is not a violation |
| 23 | `no-stamp-coupling` | A function takes the values it reads, not a bundle it mostly ignores. | General | LLM | Medium: Law of Demeter; tramp data; interface segregation at the function level | Medium | The function claims to need the whole bundle, so its tests must build it all | Applies. Exempt: framework-injected parameters | Applies. Exempt: framework-injected parameters (a handler's request, a component's props from its framework) | Universal | Owns a parameter the function mostly ignores; reaching through a value the function does use is `law-of-demeter`'s |
| 24 | `high-cohesion` | A module's public classes belong to its one concept. | General | LLM | Medium: package by feature; cohesion | Medium | Knowledge grouped by kind is found by guessing; grouped by concept, it sits where its next change will look | Applies. Exempt: Django's `models.py`, `admin.py`, `forms.py`, `serializers.py`, FastAPI's `schemas.py` | Applies. Exempt: barrel `index.ts` files and framework route files (Next.js `page.tsx`, `route.ts`) | Java: doesn't apply to files, where one public class per file is enforced; applies to packages | |
| 25 | `packages-under-import-contract` | A package the change adds is under the project's import-boundary configuration, which keeps its siblings from importing each other. | General | LLM | Medium: layered architecture; independence contracts | Medium | Mutual imports make two packages one unit; the boundary tool enforces the contract, so this rule only checks a new package is under one | import-linter | dependency-cruiser or `eslint-plugin-boundaries` | Java: ArchUnit. Go: depguard | Checks the boundary tool's configuration, never the imports themselves. Applies only where the project configures one |
| 26 | `command-query-separation` | A function either changes state or returns an answer, not both. | General | LLM | Medium: command–query separation (Meyer). Common idioms break it | Medium | A caller can't ask without changing something, so reading becomes risky | Applies. Exempt: `pop`, `setdefault` | Applies. Exempt: `push`, `shift`, `Map.set` chaining | Eiffel: high. Go: a command returning only `err` keeps it | Not a violation: a create returning the new identity. A command returning its object for chaining is a builder |
| 27 | `law-of-demeter` | A function doesn't reach through one object into another's parts. | General | LLM | Medium: Law of Demeter; Message Chains (Fowler). Its strict "one dot" form is widely disputed | Medium | The function depends on how every object along the chain is built, so changing any one of them breaks it | Applies. Exempt: pandas and query-builder chains | Applies. Exempt: optional-chained reads of plain data (`a?.b?.c`), array and promise chains | Fluent and pipeline APIs exempt everywhere: Rust iterators, LINQ | Reaching into a value object's own data, and into a framework's request or settings object, is not a violation |
| 28 | `intention-revealing-names` | A name says what its body mainly does. | General | LLM | High: intention-revealing names (Martin, *Clean Code*) | Low | A vague name sends readers to the body | Applies | Applies | Universal | Covers a creation method named for its caller |
| 29 | `one-word-per-concept` | One operation goes by one verb. | General | LLM | High: one word per concept (Martin, *Clean Code*) | Low | One operation under two verbs reads as two operations | Applies | Applies | Universal | Consistency kind |
| 30 | `no-class-level-mutable-container` | A class-level mutable container isn't mutated through `self`. | Python | ast-grep | High: a known Python pitfall | Low | Every instance shares the one container | Pattern rule | Doesn't apply: a shared field must be declared `static` | Ruby: class variables have the same pitfall | A class body binding a list, dict or set, and a method mutating it through `self`. A syntactic form of `no-shared-mutable-state`; `warning` severity so the judge rule still runs. Replaces RUF012, which checks the annotation, not the mutation |
| 31 | `comments-explain-why` | A comment or docstring states a fact from outside the code. | General | LLM | Medium: comments explain why (Martin, *Clean Code*); docstring conventions disagree | Low | A comment restating code goes stale with it; one giving an outside reason is the only kind the code can't replace | Applies. ruff ERA001, TD003 cover commented-out code and bare TODOs | Applies; TSDoc on exported items is a convention projects may keep, then the rule covers inline comments only | Go, Java: lower, doc comments on every exported item are expected | |
| 32 | `union-declares-discriminator` | A union of schema models defined in the file declares its discriminator. | Python, TypeScript (one pattern rule each) | ast-grep | Medium: pydantic's and zod's discriminated union documentation | Low | As `discriminated-unions` | Pattern rule: a field typed as a union of pydantic models | Pattern rule: `z.union` of `z.object`s sharing a literal field | Per schema library | The syntactic form of `discriminated-unions`; `warning` severity so the judge rule still runs |
| 33 | `no-value-with-its-source` | A call doesn't pass a value together with the input it was derived from. | General | LLM | Low: no mainstream source names it | Medium | The callee can derive it; passing both lets them disagree | Applies | Applies | Universal | |
| 34 | `threaded-state-own-module` | A workflow's threaded state has a module of its own. | General | LLM | Low: house convention | Low | Every step depends on the state; kept apart, the steps import it without importing each other | Applies | Applies | Universal | A module of one type and functions passes `high-cohesion` |
| 35 | `builder-pattern` | A `...Builder` class has part methods before `build()`. | General, with a pattern rule per language | ast-grep | Low: Builder pattern (*Design Patterns*), but naming is loose in practice | Low | A builder that makes its product in one call is a constructor with a misleading name | Pattern rule | Pattern rule | Java, Rust: medium; builders are common and the name is used strictly | |
| 36 | `identifier-wrapper-earns-its-type` | A class that holds one identifier adds behaviour or a check. | Python | ast-grep | Low: Primitive Obsession (Fowler) advises the opposite | Low | A wrapper with no behaviour or check adds a type to learn and protects nothing | Pattern rule. `NewType` gets the same check from basedpyright | Doesn't apply: branded types are idiomatic, and the type checker stops one id passing for another | Rust, Haskell (newtypes), F#: doesn't apply | Matches a class named `...Id`, `...Key` or `...Code` with one field, and a `str`, `int` or `UUID` subclass with an empty body. Exempt Django and SQLAlchemy models and enums. Candidate to drop: low in Python, and doesn't apply in TypeScript |

The first rule to build is `dry`.

## Waiting for the language-server tier

Each needs a lookup across the repository that a language server answers (basedpyright
for Python, tsserver for TypeScript). Ranked when codeguard can run them. All are
general.

| Convention | Note |
|---|---|
| A protocol, interface or abstract base asks for only what each of its users needs. | Interface segregation (Martin). Needs every user and implementer |
| An interface has two implementers or breaks an import cycle. | The cycle exemption is an import-graph lookup |
| A protocol or interface does more than mirror one class's data attributes. | Needs the classes that match it |
| A map wrapper has more than one call site. | |
| A passive shape used by one type lives with that type. | |
| A type lives in the package that produces it. | |
| A context type lives in its consumer's package. | |
| An interface lives in its consumer's package. | |
| A request- or action-named type does more than group an in-process call's arguments. | Needs where the type is built and read |

`liskov-substitution` also gains its cross-module form here: an override whose
base class is in another module.

## Left to a linter

Out of scope: codeguard is the layer for what a linter can't decide, and linter
settings belong in the app's own configuration. Noted so the claims aren't rebuilt.

| Claim | Python | TypeScript |
|---|---|---|
| A call in a default, or a mutable default | ruff B008, RUF009, B006 | Doesn't apply: defaults are evaluated per call |
| A `global` statement rebinds module state | ruff PLW0603 | Doesn't apply: only the declaring module can reassign |
| A bare, blind or empty error handler | ruff E722, BLE001, S110, S112 | ESLint `no-empty`; `@typescript-eslint/no-floating-promises` for an unhandled promise |
| Commented-out code, a TODO with no tracker link | ruff ERA001, TD003 (not FIX002: it flags every TODO) | ESLint `no-warning-comments` with a pattern allowing tracker links |
| Packages import each other in a cycle (acyclic dependencies, Martin) | import-linter; pylint `cyclic-import` | `import/no-cycle`; dependency-cruiser |
| Code reads another object's private attributes (information hiding, Parnas) | ruff SLF001 | The compiler, for `private` and `#` fields |
| A boolean flag argument selects behaviour (Fowler, Remove Flag Argument) | ruff FBT001–FBT003 | No standard rule; a candidate pattern rule if it matters |
| A function takes too many parameters (Long Parameter List, Fowler) | ruff PLR0913 | ESLint `max-params` |
| A condition the types already guarantee | basedpyright `reportUnnecessaryComparison` | `@typescript-eslint/no-unnecessary-condition` |

## Dropped

| Claim | Reason |
|---|---|
| Code branches on a `Literal` value set instead of an enum | `match` on a `Literal` with basedpyright's exhaustiveness check is idiomatic, as a string-literal union is in TypeScript. It came from otter's skill with no recorded reason; it comes back if one turns up |
| A function builds an argument group only to unpack it into one call | Rare; minor |
| A union's variants are not one run directly before its alias | Layout style |
| Modules split by execution phase handle the same concept | Narrow, and needs reading every phase module |
| A loop works out each item's result through a branch and collects it | Style; the live pattern rule `no-append-in-every-branch` covers its plainest Python form |
| A reference is given a fresh generated id or a made-up literal | Rare in app code; the test-side form is `real-test-data`'s |
| A matched value is given a random value | Rare |

## Gates

The Python gates `tag-value`, `union-alias-module`, `unpacked-argument-group` and
`accumulating-loop` served only dropped claims and are removed with them.
`literal-annotation` stays for `discriminated-unions`; `reference-id` stays for the test
draft `real-test-data`. Each rule's triggers are chosen per language when its language
part is written, starting from the gates in `python/drafts/bindings/`.

## Count

36 rules to build: 31 general judge rules, 2 general rules built as a pattern rule per
language (`no-middle-man`, `builder-pattern`), 1 pattern rule in each of Python
and TypeScript (`union-declares-discriminator`), and 2 Python-only pattern rules. 9 wait
for the language-server tier, 9 are left to a linter, 7 are dropped. The test drafts are
planned after these.

## Last tasks

Two checks run after each rule ships and don't hold up the next rule; the README's rule
table tracks them. The plan is done when every rule has passed both:

- **Gemini**: every judge rule's eval cases pass CI's `gemini` leg (3 runs with
  `--provider gemini`).
- **Validation**: every rule's findings on real changes, from codeguard's Logfire data,
  show it flags what it should and nothing else. A validated rule's binding moves from
  `warning` to `error`.
