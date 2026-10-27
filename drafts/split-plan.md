# Split plan: architecture drafts

Each architecture judge draft broken into single claims, checked against codeguard's
`writing-rules` skill (0.7.0): one yes/no test per rule, the cheapest exact tool,
scoped to the change, idiomatic code never fails, each code shape on the violation side
of at most one rule. Each claim is marked with what decides it:

- **LLM**: judgment; stays a judge rule.
- **ast-grep**: a code shape; becomes a pattern rule.
- **linter**: an existing linter rule (ruff, basedpyright, import-linter) decides it.
  Out of scope here: codeguard is the layer for what a linter can't decide, not a
  linter or a wrapper for one, and linter settings belong in the app's own
  configuration. The codes are noted only so the claim isn't rebuilt as a rule.
- **LSP**: a lookup a language server answers; waits for codeguard's language-server
  tier.
- **drop**: low value next to the architecture rules, or idiomatic code it would flag.
- **moved**: kept, under another draft's table.

Every kept rule gets a why: a `## Why` section in a judge rule's skill, `metadata.why`
in a pattern rule, with an optional source. The Why column is its first draft. Each
judge rule's trigger is chosen when it is written, starting from the gates its draft's
binding lists today.

**Framework idioms.** A form a framework's own documentation shows is idiomatic, so no
rule flags it ("idiomatic code never fails a rule"). Where a claim below meets one, its
note names the exemption, and the rule gets a `valid` eval case for it.

The test drafts are planned after these.

## trust-the-boundary

| Claim | Tool | Why | Note |
|---|---|---|---|
| A check repeats a condition earlier code already guarantees (an `assert x is not None` below `if x is None: raise`, a re-check of a validator's constraint) | LLM | A re-check says the guarantee can't be trusted and hides which layer owns it | Conditions only an annotation guarantees are basedpyright's (`reportUnnecessaryIsInstance`, `reportUnnecessaryComparison`) |
| A union of pydantic models, all defined in the file, is a field without `Field(discriminator=...)` | ast-grep | Without a discriminator, pydantic tries each variant in turn: slower, and its errors name every variant | `warning` severity. Syntax can't tell an imported class is a model, so this covers only the in-file form |
| A union the parse builds has no discriminator, or a variant whose tag isn't a unique `Literal` (imported models, a `TypeAdapter` union, msgspec without `tag=`, a plain-`str` tag, two variants sharing a tag value) | LLM | As above | The forms the pattern rule can't decide. A union the program builds itself and tells apart by class is not a violation |
| A data model's validator reads state outside the model and its input (a registry, a query, settings, validation context, other instances) | LLM | A model's validity should depend only on its data, so it parses the same anywhere and its tests need no setup | Flags pydantic's documented validation `context` on purpose; the Why says so. Django's `Model.clean()` checking uniqueness by query is a framework idiom and exempt |

## domain-in-data-structures

| Claim | Tool | Why | Note |
|---|---|---|---|
| Two functions switch on the same types (`isinstance` chains, class patterns) | LLM | A new type then needs every switch found and changed; one dispatch states it once | |
| Code branches on a `Literal` value set instead of an enum | drop | | `match` on a `Literal` with basedpyright's exhaustiveness check is idiomatic; it fails "idiomatic code never fails a rule". The convention came from otter's skill with no recorded reason; it comes back if one turns up. Its gate `tag-value` goes with it |
| A project function returns a tuple or fixed-key dict whose parts answer different questions (`return user, created`) | LLM | Callers learn each part's meaning from its position or key, and nothing checks it | Decided earlier |
| A dict built from a collection keeps one item per shared key and nothing chooses which or notices | moved | | To errors-surface-at-cause: it hides lost data |
| Sibling private helpers' bodies are the same except one literal or enum member | LLM | The rule (which value goes where) is restated per helper instead of passed as data | Its own rule, not merged into copied steps: the copy test says bodies differing by a constant aren't copies. Private siblings only; public methods are exempt, since callers use their names. |
| A class stores a value that restates one field it already holds: its own (`is_shipped` beside `shipped_at`) or a stored object's (`self.email` beside `self.customer`) | LLM | Two fields that must agree drift apart when one is updated and the other isn't | Merges the derived flag and copied owner values on the drafts' narrow test. Not a violation: a value computed from several sources (`self.total = sum(...)`); a key kept without its object; an ORM foreign key beside its relationship (`customer_id` with `customer`), a framework idiom. The registration-key form and the call-site form (setting a flag and its field together where the class isn't in the file) are dropped as minor |

## knowledge-has-one-home

| Claim | Tool | Why | Note |
|---|---|---|---|
| A function the change adds or edits repeats another function's steps (same steps in the same order, differing only in names, parameter order or formatting) in the file or a module it imports | LLM | Two copies of a computation change separately, so they come to disagree | Consistency kind: the search is the file's imports. Keeps the draft's copy test: bodies that differ in a step (operator, condition, constant, call) are not copies |
| Code outside a pipeline calls that pipeline's stages in its order, feeding each output into the next | LLM | The stage order is stated twice; a new stage reaches only one | Its own rule: a stage chain inside a larger function is not a function copy |
| A second type owns a job another type already owns on the same concept | LLM | Two owners of one job each get half the fixes | Consistency kind: names its search (the domain noun and verb). Building an instance is construction-has-one-home's, not a job here |
| Two passive shapes with the same fields model the same thing at the same boundary (two models of one API's response) | LLM | One outside shape described twice drifts when the outside changes | Consistency kind: the search is the boundary's module. The draft's third form, missing from the first plan |
| A function outside a type's module computes a domain answer from only that type's data | LLM | The answer belongs with the data it reads, where the type's next change will see it | Decided earlier: home is the type's module. When the type already has that method, the function is a copy and belongs to the copied-steps rule |
| A module-level collection only repeats another declared set's members | LLM | A new member must be added in two places by hand | |

## construction-has-one-home

| Claim | Tool | Why | Note |
|---|---|---|---|
| Code that is not on the type, in its module, in a factory for it or in a mapper for its source decides a new instance's field values | LLM | How a type is built changes with the type; built inline in many places, each copy needs the change | Not a violation: raising an exception; returning a result type built from values the function itself computed (`return HoldDecision(reason=r, held=h)`); a Django or SQLAlchemy model created in a view or handler (`Order.objects.create(...)`), a framework idiom. Each gets a `valid` eval case. Four homes to tell apart: watch its evals for wavering |
| Code outside a class supplies a default for one of its fields (`x or "DHL"`, a parameter default passed through, `uuid4()` for a required field) | LLM | A default declared on the class is the same for every caller; one supplied by a caller differs by caller | Owns `Invoice(currency=data.get("currency", "EUR"))`: a fallback passed to a program type's field is this rule's, not the errors fallback rule's |

## layers-earn-their-load

| Claim | Tool | Why | Note |
|---|---|---|---|
| An interface has fewer than two implementers and prevents no import cycle | LSP | | Parked. The cycle exemption is an import-graph question, so one implementer query doesn't decide it alone |
| A protocol mirrors one class's data attributes | LSP | | Parked: needs the classes that match it |
| A class only holds one collaborator and every method forwards to it unchanged | ast-grep | A layer that adds nothing is one more place to read and change | Prototype first: the collaborator must be the same in every method, which may be beyond what ast-grep metavariables can tie together. If it is, match a narrower form |
| A map wrapper has one call site | LSP | | Parked |
| A function builds an argument group only to unpack it into one call | drop | | Rare; minor. Its gate `unpacked-argument-group` goes with it |
| A class holds one identifier and has no behaviour or check | ast-grep | A wrapper with no behaviour or check adds a type to learn and protects nothing | Match a class named `...Id`, `...Key` or `...Code` with one field (including `@dataclass(frozen=True) class OrderId: value: str`), and a `str`, `int` or `UUID` subclass with an empty body. Exempt Django and SQLAlchemy models and enums. Under-matching is accepted |

## state-narrowest-scope-one-writer

| Claim | Tool | Why | Note |
|---|---|---|---|
| A shared instance (module level, class attribute, parameter default, cached factory) is of a class that stores each use's results on itself | LLM | One use's results leak into the next, and concurrent uses corrupt each other | |
| A call in a function or dataclass default, or a mutable default | linter | Evaluated once and shared by every call | ruff B008, RUF009, B006. Covers the parameter-default and dataclass-default forms of a shared instance |
| Module-level mutable state holds one call's or one instance's data | LLM | Data scoped wider than its use outlives it and is shared by accident | Split from the one-writer claim |
| Two functions write the same module-level state | LLM | With two writers, neither owns the value, and each write can undo the other | |
| A `global` statement rebinds module state | linter | | ruff PLW0603. Stricter than the claim: it also flags a lazy cache one function owns, which the drafts allow. An app may choose it |
| A class-level mutable container is mutated through `self` | ast-grep | Every instance shares the one container | A class body `$X = []`, `{}` or `set()` and a method calling `self.$X.append`, `.add`, `.update` or assigning `self.$X[...]`. Replaces RUF012, which checks the annotation, not the mutation |

## modules-own-knowledge

| Claim | Tool | Why | Note |
|---|---|---|---|
| A module holds a public class outside its one concept | LLM | Knowledge grouped by kind (`enums.py`) is found by guessing; grouped by concept, it sits where its next change will look | Framework-convention modules are exempt: Django's `models.py`, `admin.py`, `forms.py`, `serializers.py`, FastAPI's `schemas.py` |
| A state model threaded through a workflow's steps shares a module with workflow code or other public types, or is in a module named for something else | LLM | Every step depends on the state; kept apart, the steps import it without importing each other | Its own rule. The first plan merged it into one-concept, but a module of one class and functions passes that test |
| A passive shape's only user is one type in another module | LSP | | Parked |
| A type lives outside the package that produces it | LSP | | Parked |
| A context type lives outside its consumer's package | LSP | | Parked. Its in-file form (a context class in a module of output schemas) is judge-decidable, but minor; it waits with the rest |
| An interface lives outside its consumer's package | LSP | | Parked |
| A union's variants are not one run directly before its alias | drop | | Layout style. Its gate `union-alias-module` goes with it |
| Sibling packages import each other | linter | Mutual imports make the two packages one unit that can't be understood or changed apart | import-linter, with contracts each project writes for its own packages; no generic contract covers it |
| Modules split by execution phase handle the same concept | drop | | Narrow, and needs reading every phase module |

## one-responsibility

| Claim | Tool | Why | Note |
|---|---|---|---|
| A function does two or more jobs, at least one written inline | LLM | Each job changes for its own reason; together, every change risks the other | Expect wavering on short view functions; the eval cases need clear ones on both sides |
| A class's methods split into groups serving unrelated concerns | LLM | As above, for a class | |
| A loop works out each item's result through a branch and collects it | drop | | Style; the live pattern rule `no-append-in-every-branch` covers its plainest form. Its gate `accumulating-loop` goes with it |

## takes-what-it-needs

| Claim | Tool | Why | Note |
|---|---|---|---|
| A method takes a collaborator as a parameter instead of through its constructor | LLM | Every caller then has to find the collaborator; through the constructor, it's wired once | |
| A function takes a bundle (context, settings, request) to read half its fields or fewer | LLM | The function claims to need the whole bundle, so its tests must build it all | Framework-injected parameters are exempt: a framework's `request` signature, FastAPI's `Depends(...)` |
| A call passes a value together with the input it was derived from to a callee the program declares | LLM | The callee can derive it; passing both lets them disagree | |
| A stored record, or a dump of one, is passed across a task or queue boundary | LLM | The record is stale by the time the task runs; pass its id and reload it | |
| A reference is given a fresh generated id or a made-up literal | drop | | In app code, rare; the test-side form is `real-test-data`'s |
| A matched value is given a random value | drop | | Rare |

## errors-surface-at-cause

| Claim | Tool | Why | Note |
|---|---|---|---|
| A bare or blind `except`, or one whose body is `pass` or `continue` | linter | | ruff E722, BLE001, S110, S112. A cheap first pass only: S110 and S112 fire only on broad handlers by default, and BLE001 lets a handler that logs pass |
| An `except` or `contextlib.suppress` carries on without handling an error the caller needs (returns a default, passes, continues, breaks or only logs) | LLM | A swallowed error turns into a wrong result far from its cause | Covers what the linters miss: specific exception types, `break`, `suppress` (which ruff's SIM105 rewrites code into), and handlers that log and carry on |
| A fallback default stands in for data that should exist | LLM | Missing data passes as real data and is found later, if ever | A fallback passed to a program type's field is construction-has-one-home's |
| A clamp hides a state the program's rules say can't happen | LLM | The impossible state is silently made possible-looking instead of reported | |
| A dict build silently drops items sharing a key | LLM | Lost items vanish without a trace | From `domain-in-data-structures` |

## names-tell-the-truth

Decided earlier.

| Claim | Tool | Why | Note |
|---|---|---|---|
| A name is a true summary of its body (no word the body doesn't do, and a word for its main action), including a creation method named for its caller | LLM | Readers trust names; a false or vague one sends them to the body | Two questions in one; see Open |
| A method does a collaborating function's operation under a different verb | LLM | One operation under two verbs reads as two operations | Consistency kind |
| A request- or action-named type only groups an in-process call's arguments | LSP | | Parked: deciding it needs where the type is built and read across the repository, a references lookup |
| A comment or docstring the change adds states no fact from outside the code | LLM | A comment restating code goes stale with it; one giving an outside reason is the only kind the code can't replace | Commented-out code and bare TODOs are the linters', not this rule's violation side |
| A `...Builder` class has no part methods before `build()` | ast-grep | A builder that makes its product in one call is a constructor with a misleading name | |
| Commented-out code, a TODO with no tracker link | linter | | ruff ERA001, TD003. Not FIX002: it flags every TODO, and the draft allows one with a tracker link |

## Overlaps settled

Each shape is on the violation side of one rule:

- `Invoice(currency=data.get("currency", "EUR"))`: construction's default rule, not the
  errors fallback rule.
- A module function copying an existing method of the type (`is_heavy(s)` beside
  `Shipment.is_heavy`): the copied-steps rule, not the domain-answer rule.
- A service building an instance inline when a factory exists: construction's rule,
  not the second-owner-of-a-job rule.
- A dict build dropping items sharing a key: errors only; it's moved, not counted twice.
- Commented-out code and bare TODOs: ruff only.

## Gates to remove

Gates whose only binding claim is dropped: `tag-value`, `union-alias-module`,
`unpacked-argument-group`, `accumulating-loop`. Each is removed with its claim.
`literal-annotation` stays: trust-the-boundary's discriminator rule uses it for
variant tags. `reference-id` stays: the test draft `real-test-data` uses it.

## Open

- **Names claim 1** is two questions, a false name and a vague name. It was decided as
  one rule; splitting it is the skill's default.

## Count

From 11 drafts: 33 judge rules, 5 pattern rules, 5 checks a linter already decides, 8 claims
parked for the language-server tier, 7 dropped. The linter checks stay in the
app's linter configuration, not here.
