# Split plan: architecture drafts

Each architecture judge draft broken into rules, checked against codeguard's
`writing-rules` skill (0.8.0). The standard:

- **A rule is one convention**: one abstract declarative sentence, at the level of
  intent, that each piece of code either keeps or breaks. codeguard's judge prompt
  (`review/judge.md`) reviews the change against that convention and reports where a
  changed line breaks it, so the rule is a statement, not a question. A rule that states
  several conventions splits; forms that break the same convention are one rule. An
  intent (a draft below) groups rules and is not itself a rule.
- **A judge skill's structure**: the convention sentence first; definitions of its
  terms; a Violation section stating what breaks it and the line it's reported on (the
  line a fix would change); the forms on both sides as illustrations; what is not a
  violation; `## Why`. No fix, and nothing on how to answer: the judge prompt sets that.
- **Examples only illustrate.** Code no example shows is still decided by the
  convention. No example goes in a rule's one-line description.
- **Evals never reuse a skill example**, even renamed or with changed literals. The
  judge prompt's top confidence is for code that matches an example the convention
  describes, so a reused example tests that match, not the convention. Each case uses
  different code, a different domain and different names. A failing case restates the
  convention; its code never becomes a skill example. Pattern rule tests are exempt:
  they check syntax.
- The cheapest exact tool, scoped to the change; idiomatic code never fails a rule; each
  code shape is on the violation side of at most one rule.

Each convention is marked with what decides it:

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

The Note column says what the convention covers and exempts, sometimes with a code form
for this plan's reader. Those forms are planning shorthand: the skill's examples and
the eval cases are written fresh, from different domains, when each rule is written.

**Framework idioms.** A form a framework's own documentation shows is idiomatic, so no
rule flags it. Where a convention below meets one, its note names the exemption, and the
rule gets a `valid` eval case for it.

The test drafts are planned after these.

## trust-the-boundary

| Convention | Tool | Why | Note |
|---|---|---|---|
| A check doesn't re-test a condition earlier code already guarantees. | LLM | A re-check says the guarantee can't be trusted and hides which layer owns it | Covers an earlier raise or return, and a validator's constraint. A condition only an annotation guarantees is basedpyright's (`reportUnnecessaryIsInstance`, `reportUnnecessaryComparison`) |
| A field typed as a union of pydantic models defined in the file declares a discriminator. | ast-grep | Without a discriminator, pydantic tries each variant in turn: slower, and its errors name every variant | `warning` severity, so the judge rule below still runs on the file. Syntax can't tell an imported class is a model, so this covers only the in-file form |
| A parsed union's parser picks each variant from one unique tag. | LLM | As above | Covers a missing discriminator, a tag that isn't a unique literal, and every parsing library. A union the program builds itself and tells apart by class is not a violation |
| A data model's validator depends only on the model and its input. | LLM | A model's validity should depend only on its data, so it parses the same anywhere and its tests need no setup | Flags pydantic's documented validation `context` on purpose; the Why says so. Django's `Model.clean()` checking uniqueness by query is a framework idiom and exempt |

## domain-in-data-structures

| Convention | Tool | Why | Note |
|---|---|---|---|
| Behaviour chosen by a value's type is chosen in one place. | LLM | A new type then needs every switch found and changed; one dispatch states it once | |
| A function's result names what each of its parts means. | LLM | Nothing checks a part's meaning, so a caller that reads it wrong passes | Decided earlier. A pair whose meaning is the type's own (a coordinate) is not a violation |
| A class doesn't store a value it can derive from one other value it holds. | LLM | Two values that must agree drift apart when one is updated and the other isn't | Covers its own fields and a held object's. Not a violation: a value derived from several sources; a key kept without its object; an ORM foreign key beside its relationship, a framework idiom |
| Code branches on a `Literal` value set instead of an enum | drop | | `match` on a `Literal` with basedpyright's exhaustiveness check is idiomatic. The convention came from otter's skill with no recorded reason; it comes back if one turns up. Its gate `tag-value` goes with it |

## knowledge-has-one-home

| Convention | Tool | Why | Note |
|---|---|---|---|
| Each piece of knowledge is stated once in the code. | LLM | Two copies change separately, so they come to disagree | Merges five claims that were one convention: a function repeating another's steps, private siblings differing only by a value, a stage sequence repeated outside its pipeline, a collection repeating another declared set's members, two passive shapes modelling one outside thing. Consistency kind: the search is the file and the modules it imports. Not a copy: bodies differing in a step; public methods with distinct names. The widest rule in the plan: its eval keeps a case per form on both sides, and wavering on one form splits that form out |
| One type owns each job on a concept. | LLM | Two owners of one job each get half the fixes | Consistency kind: names its search. Building an instance is construction's |
| A domain answer computed from one type's data lives in that type's module. | LLM | The answer belongs with the data it reads, where the type's next change will see it | Decided earlier. When the type already has that method, the function is a copy: the restated-knowledge rule's |

## construction-has-one-home

| Convention | Tool | Why | Note |
|---|---|---|---|
| What a new instance holds is decided by its type, its module, its factory or its source's mapper. | LLM | How a type is built changes with the type; built inline in many places, each copy needs the change | Merges the default claim: a caller supplying a default for a field is deciding what the instance holds. Not a violation: raising an exception; returning a result built from values the function computed; a Django or SQLAlchemy model created in a view or handler, a framework idiom. Each gets a `valid` eval case. Four homes to tell apart: watch its evals for wavering |

## layers-earn-their-load

| Convention | Tool | Why | Note |
|---|---|---|---|
| An interface has two implementers or breaks an import cycle. | LSP | | Parked. The cycle exemption is an import-graph lookup |
| A protocol does more than mirror one class's data attributes. | LSP | | Parked: needs the classes that match it |
| A class does more than forward every method to one collaborator. | ast-grep | A layer that adds nothing is one more place to read and change | Prototype first: tying every method to one collaborator may be beyond ast-grep metavariables. If it is, match a narrower form |
| A map wrapper has more than one call site. | LSP | | Parked |
| A class that holds one identifier adds behaviour or a check. | ast-grep | A wrapper with no behaviour or check adds a type to learn and protects nothing | Matches a class named `...Id`, `...Key` or `...Code` with one field, and a `str`, `int` or `UUID` subclass with an empty body. Exempt Django and SQLAlchemy models and enums. Under-matching is accepted |
| A function builds an argument group only to unpack it into one call | drop | | Rare; minor. Its gate `unpacked-argument-group` goes with it |

## state-narrowest-scope-one-writer

| Convention | Tool | Why | Note |
|---|---|---|---|
| Data belonging to one call or use is kept where only that call or use sees it. | LLM | One use's data leaks into the next, and concurrent uses corrupt each other | Merges two claims that were one convention: module-level state holding one call's data, and a shared instance (module level, class attribute, cached factory) storing each use's results on itself |
| Module-level state has one writer. | LLM | With two writers, neither owns the value, and each write can undo the other | |
| A class-level mutable container isn't mutated through `self`. | ast-grep | Every instance shares the one container | A class body binding a list, dict or set, and a method mutating it through `self`. Replaces RUF012, which checks the annotation, not the mutation. A syntactic form of the shared-data convention; `warning` severity so the judge rule still runs |
| A call in a function or dataclass default, or a mutable default | linter | | ruff B008, RUF009, B006 |
| A `global` statement rebinds module state | linter | | ruff PLW0603. Stricter than the drafts, which allow a lazy cache one function owns. An app may choose it |

## modules-own-knowledge

| Convention | Tool | Why | Note |
|---|---|---|---|
| A module's public classes belong to its one concept. | LLM | Knowledge grouped by kind is found by guessing; grouped by concept, it sits where its next change will look | Framework-convention modules are exempt: Django's `models.py`, `admin.py`, `forms.py`, `serializers.py`, FastAPI's `schemas.py` |
| A workflow's threaded state has a module of its own. | LLM | Every step depends on the state; kept apart, the steps import it without importing each other | Also a module named for something else. Its own convention: a module of one class and functions passes the one-concept test |
| A package the change adds is in an import-linter contract that keeps its siblings from importing each other. | LLM | Mutual imports make two packages one unit that can't be understood or changed apart; import-linter enforces the contract, so this rule only checks a new package is under one | Checks the project's import-linter configuration, never the imports themselves. Consistency kind: names its search. Applies only where the project configures import-linter |
| A passive shape used by one type lives with that type. | LSP | | Parked |
| A type lives in the package that produces it. | LSP | | Parked |
| A context type lives in its consumer's package. | LSP | | Parked |
| An interface lives in its consumer's package. | LSP | | Parked |
| A union's variants are not one run directly before its alias | drop | | Layout style. Its gate `union-alias-module` goes with it |
| Modules split by execution phase handle the same concept | drop | | Narrow, and needs reading every phase module |

## one-responsibility

| Convention | Tool | Why | Note |
|---|---|---|---|
| A function or class does one job. | LLM | Each job changes for its own reason; together, every change risks the other | Merges the function and class claims, one convention at two scopes. A function that only calls one helper per job does one job, orchestration. Expect wavering on short view functions; the eval needs clear cases on both sides |
| A loop works out each item's result through a branch and collects it | drop | | Style; the live pattern rule `no-append-in-every-branch` covers its plainest form. Its gate `accumulating-loop` goes with it |

## takes-what-it-needs

| Convention | Tool | Why | Note |
|---|---|---|---|
| A method's collaborators come through its object's constructor. | LLM | Every caller then has to find the collaborator; through the constructor, it's wired once | |
| A function takes the values it reads, not a bundle it mostly ignores. | LLM | The function claims to need the whole bundle, so its tests must build it all | Framework-injected parameters are exempt |
| A call doesn't pass a value together with the input it was derived from. | LLM | The callee can derive it; passing both lets them disagree | |
| A stored record crosses a task or queue boundary as its identity. | LLM | The record is stale by the time the task runs; pass its id and reload it | |
| A reference is given a fresh generated id or a made-up literal | drop | | In app code, rare; the test-side form is `real-test-data`'s |
| A matched value is given a random value | drop | | Rare |

## errors-surface-at-cause

| Convention | Tool | Why | Note |
|---|---|---|---|
| A failure, missing data or an impossible state is reported where it's found, never turned into a normal-looking result. | LLM | The problem turns into a wrong result far from its cause, found later, if ever | Merges four claims that were one convention: a handler that carries on, a fallback standing in for data that should exist, a clamp hiding a state the rules say can't happen, and a collection build silently dropping items. A caller-supplied default for a program type's field is construction's |
| A bare or blind `except`, or one whose body is `pass` or `continue` | linter | | ruff E722, BLE001, S110, S112. A cheap first pass; the judge rule covers specific exception types, `contextlib.suppress`, `break` and log-only handlers |

## names-tell-the-truth

| Convention | Tool | Why | Note |
|---|---|---|---|
| A name claims nothing its body doesn't do. | LLM | Readers trust names; a false one sends them wrong | Split from the decided names rule, which stated two conventions |
| A name says what its body mainly does. | LLM | A vague name sends readers to the body | Covers a creation method named for its caller |
| One operation goes by one verb. | LLM | One operation under two verbs reads as two operations | Consistency kind |
| A comment or docstring states a fact from outside the code. | LLM | A comment restating code goes stale with it; one giving an outside reason is the only kind the code can't replace | Commented-out code and bare TODOs are the linters' |
| A `...Builder` class has part methods before `build()`. | ast-grep | A builder that makes its product in one call is a constructor with a misleading name | |
| A request- or action-named type does more than group an in-process call's arguments. | LSP | | Parked: needs where the type is built and read, a references lookup |
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

Rechecked against the 2026-10-27 standard (a rule is one abstract convention; evals never
reuse its examples):

- Every claim restated as an abstract convention, a statement the judge checks code
  against, with its examples moved out of it.
- Merged, as one convention each: restated knowledge (five claims), errors surfacing
  (four), shared data (two), one responsibility (two), construction (two).
- Split: the names truth rule into a false name and a vague name, closing the open item.

## Count

From 11 drafts: 25 judge rules, 5 pattern rules, 4 checks a linter already decides, 8
conventions parked for the language-server tier, 7 dropped. The linter checks stay in the
app's linter configuration, not here.
