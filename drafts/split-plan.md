# Split plan: architecture drafts

Each architecture judge draft broken into rules, checked against codeguard's
`writing-rules` skill (0.8.0). The standard:

- **A rule is one abstract yes/no question**, stated at the level of intent in a
  reviewer's words: never a list of code shapes, values or names. A rule that asks
  several questions splits; forms that answer the same question are one rule. An
  intent (a draft below) groups rules and is not itself a rule.
- **Examples only illustrate.** A judge rule's skill shows the question on both sides
  with examples; code no example shows is still decided by the question. No example goes
  in a rule's one-line description.
- **Evals never reuse a skill example**, even renamed or with changed literals. Each
  case uses different code, a different domain and different names that exercise the
  same question. A failing case restates the question; its code never becomes a skill
  example. Pattern rule tests are exempt: they check syntax.
- The cheapest exact tool, scoped to the change; idiomatic code never fails a rule; each
  code shape is on the violation side of at most one rule.

Each question is marked with what decides it:

- **LLM**: judgment; a judge rule.
- **ast-grep**: a code shape; a pattern rule.
- **linter**: an existing linter rule (ruff, basedpyright, import-linter) decides it.
  Out of scope here: codeguard is the layer for what a linter can't decide, not a
  linter or a wrapper for one, and linter settings belong in the app's own
  configuration. The codes are noted only so the claim isn't rebuilt as a rule.
- **LSP**: a lookup a language server answers; waits for codeguard's language-server
  tier.
- **drop**: low value next to the architecture rules, or idiomatic code it would flag.

Every kept rule gets a why: a `## Why` section in a judge rule's skill, `metadata.why`
in a pattern rule, with an optional source. The Why column is its first draft. Each
judge rule's trigger is chosen when it is written, starting from the gates its draft's
binding lists today.

The Note column says what the question covers and exempts, sometimes with a code form
for this plan's reader. Those forms are planning shorthand: the skill's examples and
the eval cases are written fresh, from different domains, when each rule is written.

**Framework idioms.** A form a framework's own documentation shows is idiomatic, so no
rule flags it. Where a question below meets one, its note names the exemption, and the
rule gets a `valid` eval case for it.

The test drafts are planned after these.

## trust-the-boundary

| Question | Tool | Why | Note |
|---|---|---|---|
| Does a check re-test a condition that earlier code already guarantees? | LLM | A re-check says the guarantee can't be trusted and hides which layer owns it | Covers an earlier raise or return, and a validator's constraint. A condition only an annotation guarantees is basedpyright's (`reportUnnecessaryIsInstance`, `reportUnnecessaryComparison`) |
| Is a field typed as a union of pydantic models, all defined in the file, without a discriminator? | ast-grep | Without a discriminator, pydantic tries each variant in turn: slower, and its errors name every variant | `warning` severity, so the judge rule below still runs on the file. Syntax can't tell an imported class is a model, so this covers only the in-file form |
| Can the parser of a union it builds fail to pick the variant from one unique tag? | LLM | As above | Covers a missing discriminator, a tag that isn't a unique literal, and every parsing library. A union the program builds itself and tells apart by class is not a violation |
| Does a data model's validator depend on anything besides the model and its input? | LLM | A model's validity should depend only on its data, so it parses the same anywhere and its tests need no setup | Flags pydantic's documented validation `context` on purpose; the Why says so. Django's `Model.clean()` checking uniqueness by query is a framework idiom and exempt |

## domain-in-data-structures

| Question | Tool | Why | Note |
|---|---|---|---|
| Do two functions each decide behaviour by testing which of the same types a value is? | LLM | A new type then needs every switch found and changed; one dispatch states it once | |
| Does a function return several values whose meanings callers learn only from position or key? | LLM | Nothing checks a part's meaning, so a caller that reads it wrong passes | Decided earlier. A pair whose meaning is the type's own (a coordinate) is not a violation |
| Does a class store a value it could derive from one other value it already holds? | LLM | Two values that must agree drift apart when one is updated and the other isn't | Covers its own fields and a held object's. Not a violation: a value derived from several sources; a key kept without its object; an ORM foreign key beside its relationship, a framework idiom |
| Code branches on a `Literal` value set instead of an enum | drop | | `match` on a `Literal` with basedpyright's exhaustiveness check is idiomatic. The convention came from otter's skill with no recorded reason; it comes back if one turns up. Its gate `tag-value` goes with it |

## knowledge-has-one-home

| Question | Tool | Why | Note |
|---|---|---|---|
| Does the change state again knowledge the code already states, so that the two must change together? | LLM | Two copies change separately, so they come to disagree | Merges five claims that were one question: a function repeating another's steps, private siblings differing only by a value, a stage sequence repeated outside its pipeline, a collection repeating another declared set's members, two passive shapes modelling one outside thing. Consistency kind: the search is the file and the modules it imports. Not a copy: bodies differing in a step; public methods with distinct names. The widest rule in the plan: its eval keeps a case per form on both sides, and wavering on one form splits that form out |
| Does a second type take on a job another type already owns for the same concept? | LLM | Two owners of one job each get half the fixes | Consistency kind: names its search. Building an instance is construction's |
| Does code outside a type's module compute a domain answer from only that type's data? | LLM | The answer belongs with the data it reads, where the type's next change will see it | Decided earlier. When the type already has that method, the function is a copy: the restated-knowledge rule's |

## construction-has-one-home

| Question | Tool | Why | Note |
|---|---|---|---|
| Does code other than the type, its module, its factory or its source's mapper decide what a new instance holds? | LLM | How a type is built changes with the type; built inline in many places, each copy needs the change | Merges the default claim: a caller supplying a default for a field is deciding what the instance holds. Not a violation: raising an exception; returning a result built from values the function computed; a Django or SQLAlchemy model created in a view or handler, a framework idiom. Each gets a `valid` eval case. Four homes to tell apart: watch its evals for wavering |

## layers-earn-their-load

| Question | Tool | Why | Note |
|---|---|---|---|
| Does an interface have fewer than two implementers while preventing no import cycle? | LSP | | Parked. The cycle exemption is an import-graph question |
| Does a protocol only mirror one class's data attributes? | LSP | | Parked: needs the classes that match it |
| Does a class only hold one collaborator and forward every method to it unchanged? | ast-grep | A layer that adds nothing is one more place to read and change | Prototype first: tying every method to one collaborator may be beyond ast-grep metavariables. If it is, match a narrower form |
| Does a map wrapper have one call site? | LSP | | Parked |
| Does a class hold one identifier with no behaviour or check? | ast-grep | A wrapper with no behaviour or check adds a type to learn and protects nothing | Matches a class named `...Id`, `...Key` or `...Code` with one field, and a `str`, `int` or `UUID` subclass with an empty body. Exempt Django and SQLAlchemy models and enums. Under-matching is accepted |
| A function builds an argument group only to unpack it into one call | drop | | Rare; minor. Its gate `unpacked-argument-group` goes with it |

## state-narrowest-scope-one-writer

| Question | Tool | Why | Note |
|---|---|---|---|
| Is data belonging to one call or one use kept where other calls or uses share it? | LLM | One use's data leaks into the next, and concurrent uses corrupt each other | Merges two claims that were one question: module-level state holding one call's data, and a shared instance (module level, class attribute, cached factory) storing each use's results on itself |
| Do two functions write the same module-level state? | LLM | With two writers, neither owns the value, and each write can undo the other | |
| Is a class-level mutable container mutated through `self`? | ast-grep | Every instance shares the one container | A class body binding a list, dict or set, and a method mutating it through `self`. Replaces RUF012, which checks the annotation, not the mutation. A syntactic form of the shared-data question; `warning` severity so the judge rule still runs |
| A call in a function or dataclass default, or a mutable default | linter | | ruff B008, RUF009, B006 |
| A `global` statement rebinds module state | linter | | ruff PLW0603. Stricter than the drafts, which allow a lazy cache one function owns. An app may choose it |

## modules-own-knowledge

| Question | Tool | Why | Note |
|---|---|---|---|
| Does a module hold a public class outside its one concept? | LLM | Knowledge grouped by kind is found by guessing; grouped by concept, it sits where its next change will look | Framework-convention modules are exempt: Django's `models.py`, `admin.py`, `forms.py`, `serializers.py`, FastAPI's `schemas.py` |
| Does a workflow's threaded state share a module with workflow code or other public types? | LLM | Every step depends on the state; kept apart, the steps import it without importing each other | Also a module named for something else. Its own question: a module of one class and functions passes the one-concept test |
| Is a package the change adds outside every import-linter contract that keeps its siblings from importing each other? | LLM | Mutual imports make two packages one unit that can't be understood or changed apart; import-linter enforces the contract, so this rule only checks a new package is under one | Checks the project's import-linter configuration, never the imports themselves. Consistency kind: names its search. Applies only where the project configures import-linter |
| Is a passive shape's only user one type in another module? | LSP | | Parked |
| Does a type live outside the package that produces it? | LSP | | Parked |
| Does a context type live outside its consumer's package? | LSP | | Parked |
| Does an interface live outside its consumer's package? | LSP | | Parked |
| A union's variants are not one run directly before its alias | drop | | Layout style. Its gate `union-alias-module` goes with it |
| Modules split by execution phase handle the same concept | drop | | Narrow, and needs reading every phase module |

## one-responsibility

| Question | Tool | Why | Note |
|---|---|---|---|
| Does one function or class do jobs that change for unrelated reasons? | LLM | Each job changes for its own reason; together, every change risks the other | Merges the function and class claims, one question at two scopes. A function that only calls one helper per job does one job, orchestration. Expect wavering on short view functions; the eval needs clear cases on both sides |
| A loop works out each item's result through a branch and collects it | drop | | Style; the live pattern rule `no-append-in-every-branch` covers its plainest form. Its gate `accumulating-loop` goes with it |

## takes-what-it-needs

| Question | Tool | Why | Note |
|---|---|---|---|
| Does a method receive a collaborator per call instead of when its object is built? | LLM | Every caller then has to find the collaborator; through the constructor, it's wired once | |
| Does a function take a bundle of values it reads half or fewer of? | LLM | The function claims to need the whole bundle, so its tests must build it all | Framework-injected parameters are exempt |
| Does a call pass a value together with the input it was derived from to a callee the program declares? | LLM | The callee can derive it; passing both lets them disagree | |
| Is a stored record, rather than its identity, sent across a task or queue boundary? | LLM | The record is stale by the time the task runs; pass its id and reload it | |
| A reference is given a fresh generated id or a made-up literal | drop | | In app code, rare; the test-side form is `real-test-data`'s |
| A matched value is given a random value | drop | | Rare |

## errors-surface-at-cause

| Question | Tool | Why | Note |
|---|---|---|---|
| Does the code turn a failure, missing data or an impossible state into a normal-looking result instead of reporting it? | LLM | The problem turns into a wrong result far from its cause, found later, if ever | Merges four claims that were one question: a handler that carries on, a fallback standing in for data that should exist, a clamp hiding a state the rules say can't happen, and a collection build silently dropping items. A caller-supplied default for a program type's field is construction's |
| A bare or blind `except`, or one whose body is `pass` or `continue` | linter | | ruff E722, BLE001, S110, S112. A cheap first pass; the judge rule covers specific exception types, `contextlib.suppress`, `break` and log-only handlers |

## names-tell-the-truth

| Question | Tool | Why | Note |
|---|---|---|---|
| Does a name claim something its body doesn't do? | LLM | Readers trust names; a false one sends them wrong | Split from the decided names rule, which asked two questions |
| Does a name leave out what its body mainly does? | LLM | A vague name sends readers to the body | Covers a creation method named for its caller |
| Does a method do a collaborator's operation under a different verb? | LLM | One operation under two verbs reads as two operations | Consistency kind |
| Does a comment or docstring the change adds state no fact from outside the code? | LLM | A comment restating code goes stale with it; one giving an outside reason is the only kind the code can't replace | Commented-out code and bare TODOs are the linters' |
| Does a `...Builder` class make its product without part methods before `build()`? | ast-grep | A builder that makes its product in one call is a constructor with a misleading name | |
| Does a request- or action-named type only group an in-process call's arguments? | LSP | | Parked: needs where the type is built and read, a references lookup |
| Commented-out code, a TODO with no tracker link | linter | | ruff ERA001, TD003. Not FIX002: it flags every TODO, and the draft allows one with a tracker link |

## Overlaps settled

Each shape is on the violation side of one rule:

- A caller-supplied default for a program type's field: construction, not errors.
- A module function copying a method the type already has: the restated-knowledge
  rule, not the domain-answer rule.
- Building an instance inline when a factory exists: construction, not the
  second-owner rule.
- Commented-out code and bare TODOs: ruff only.
- A class-level container mutated through `self`: the pattern rule and the
  shared-data judge rule both see it; the pattern rule is a `warning` so both report.

## Gates to remove

Gates whose only binding claim is dropped: `tag-value`, `union-alias-module`,
`unpacked-argument-group`, `accumulating-loop`. Each is removed with its claim.
`literal-annotation` stays: the discriminator rule uses it for variant tags.
`reference-id` stays: the test draft `real-test-data` uses it.

## Changes from the previous plan

Rechecked against the 2026-10-27 standard (a rule is one abstract question; evals never
reuse its examples):

- Every claim restated as an abstract question, with its examples moved out of it.
- Merged, as one question each: restated knowledge (five claims), errors surfacing
  (four), shared data (two), one responsibility (two), construction (two).
- Split: the names truth rule into a false name and a vague name, closing the open item.

## Count

From 11 drafts: 25 judge rules, 5 pattern rules, 4 checks a linter already decides, 8
questions parked for the language-server tier, 7 dropped. The linter checks stay in the
app's linter configuration, not here.
