# Split plan: architecture drafts

Each architecture judge draft broken into single claims, checked against codeguard's
`writing-rules` skill (0.7.0): one yes/no test per rule, the cheapest exact tool,
scoped to the change, idiomatic code never fails, each code shape on the violation side
of at most one rule. Each claim is marked with what decides it:

- **LLM**: judgment; stays a judge rule.
- **ast-grep**: a code shape; becomes a pattern rule.
- **linter**: a ruff or basedpyright rule, or import-linter, already covers it; the
  README recommends it instead.
- **LSP**: a lookup a language server answers; waits for codeguard's language-server
  tier.
- **drop**: low value next to the architecture rules, or idiomatic code it would flag.
- **merge**: the same test as another claim; folded into it.

The test drafts are planned after these.

## trust-the-boundary

| Claim | Tool | Note |
|---|---|---|
| A check repeats a condition earlier code already guarantees (an `assert x is not None` below `if x is None: raise`, a re-check of a validator's constraint) | LLM | Conditions only an annotation guarantees are basedpyright's (`reportUnnecessaryIsInstance`, `reportUnnecessaryComparison`) |
| A union of pydantic models the parse builds names its discriminator | ast-grep | A union alias of models used as a field without `Field(discriminator=...)` |
| A data model's validator reads state outside the model (a registry, a query, settings, validation context) | LLM | |

## domain-in-data-structures

| Claim | Tool | Note |
|---|---|---|
| Two functions switch on the same types (`isinstance` chains, class patterns) | LLM | |
| Code branches on a `Literal` value set instead of an enum | drop | `match` on a `Literal` with basedpyright's exhaustiveness check is idiomatic; it fails "idiomatic code never fails a rule". The convention came from otter's skill with no recorded reason; it comes back if one turns up |
| A project function returns a tuple or fixed-key dict whose parts answer different questions (`return user, created`) | LLM | Decided earlier |
| A dict built from a collection keeps one item per shared key and nothing chooses which or notices | LLM | Hides lost data, so it moves to the errors group |
| Sibling private helpers differ only by one value | merge | Into "a function repeats another's steps" |
| A boolean field restates another field of the class (`is_shipped` beside `shipped_at`) | merge | With "copied owner values" into "a class stores a value it can derive from what it already holds" |

## knowledge-has-one-home

| Claim | Tool | Note |
|---|---|---|
| A function the change adds or edits repeats the steps of another function in the file or a module it imports | LLM | Consistency kind: the search is the file's imports. Takes in the one-value helpers and re-implemented orchestration (a pipeline's stage calls chained outside it is a copy of its steps) |
| A second type owns a job another type already owns on the same concept | LLM | Consistency kind: names its search (the domain noun and verb) |
| A function outside a type's module computes a domain answer from only that type's data | LLM | Decided earlier: home is the type's module |
| A class stores a value it can derive from another field or object it holds | LLM | Merged from the derived flag and copied owner values. The "class attribute equal to its registration key" form is dropped as minor |
| A module-level collection only repeats another declared set's members | LLM | |

## construction-has-one-home

| Claim | Tool | Note |
|---|---|---|
| Code that is not on the type, in its module, in a factory for it or in a mapper for its source decides a new instance's field values | LLM | |
| Code outside a class supplies a default for one of its fields (`x or "DHL"`, a parameter default passed through, `uuid4()` for a required field) | LLM | Not a contradiction with `takes-what-it-needs`: that rule allows `id=uuid4()` for its own claim and doesn't require it |

## layers-earn-their-load

| Claim | Tool | Note |
|---|---|---|
| An interface has fewer than two implementers and prevents no import cycle | LSP | Parked |
| A protocol mirrors one class's data attributes | LSP | Parked: needs the classes that match it |
| A class only holds one collaborator and every method forwards to it unchanged | ast-grep | The same shape `no-forwarding-wrappers` matches for functions |
| A map wrapper has one call site | LSP | Parked |
| A function builds an argument group only to unpack it into one call | drop | Rare; minor |
| A class holds one identifier and has no behaviour or check | ast-grep | A one-field class whose field name is an identifier (`*_id`, `key`, `code`, `sku`, `slug`) with no methods or validators |

## state-narrowest-scope-one-writer

| Claim | Tool | Note |
|---|---|---|
| A shared instance (module level, class attribute, parameter default, cached factory) is of a class that stores each use's results on itself | LLM | |
| Module-level mutable state holds one call's or one instance's data, or two functions write it | LLM | |
| A `global` statement rebinds module state | linter | ruff PLW0603 |
| A class-level container is shared by every instance | linter | ruff RUF012 |

## modules-own-knowledge

| Claim | Tool | Note |
|---|---|---|
| A module holds a public class outside its one concept | LLM | Takes in "threaded state outside its own module": a state model beside workflow code is a second concept |
| A passive shape's only user is one type in another module | LSP | Parked |
| A type lives outside the package that produces it | LSP | Parked |
| A context type lives outside its consumer's package | LSP | Parked |
| An interface lives outside its consumer's package | LSP | Parked |
| A union's variants are not one run directly before its alias | drop | Layout style |
| Sibling packages import each other | linter | import-linter |
| Modules split by execution phase handle the same concept | drop | Narrow, and needs reading every phase module |

## one-responsibility

| Claim | Tool | Note |
|---|---|---|
| A function does two or more jobs, at least one written inline | LLM | |
| A class's methods split into groups serving unrelated concerns | LLM | |
| A loop works out each item's result through a branch and collects it | drop | Style; the live pattern rule `no-append-in-every-branch` covers its plainest form |

## takes-what-it-needs

| Claim | Tool | Note |
|---|---|---|
| A method takes a collaborator as a parameter instead of through its constructor | LLM | |
| A function takes a bundle (context, settings, request) to read half its fields or fewer | LLM | |
| A call passes a value together with the input it was derived from to a callee the program declares | LLM | |
| A stored record, or a dump of one, is passed across a task or queue boundary | LLM | |
| A reference is given a fresh generated id or a made-up literal | drop | In app code, rare; the test-side form is `real-test-data`'s |
| A matched value is given a random value | drop | Rare |

## errors-surface-at-cause

| Claim | Tool | Note |
|---|---|---|
| A bare or blind `except`, or one whose body is `pass` or `continue` | linter | ruff E722, BLE001, S110, S112 |
| An `except` returns a default or only logs and carries on, for an error the caller needs | LLM | |
| A fallback default stands in for data that should exist | LLM | |
| A clamp hides a state the program's rules say can't happen | LLM | |
| A dict build silently drops items sharing a key | LLM | From `domain-in-data-structures` |

## names-tell-the-truth

Decided earlier.

| Claim | Tool | Note |
|---|---|---|
| A name is a true summary of its body (no word the body doesn't do, and a word for its main action), including a creation method named for its caller | LLM | |
| A method does a collaborating function's operation under a different verb | LLM | Consistency kind |
| A request- or action-named type only groups an in-process call's arguments | LLM | |
| A comment or docstring says nothing the code doesn't | LLM | |
| A `...Builder` class has no part methods before `build()` | ast-grep | |
| Commented-out code, bare TODOs | linter | ruff ERA001, TD003, FIX002 |

## Count

From 11 drafts: 28 judge rules, 4 pattern rules, 5 checks moved to linters, 7 claims
parked for the language-server tier, 7 dropped.
