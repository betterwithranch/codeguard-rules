# Draft rules

Judge rules and pattern rules that codeguard doesn't load. codeguard validates only the
ruleset directories named in `codeguard-package.yaml`, so nothing here runs. The gates
the drafts' bindings name are in `python/gates/`, where `codeguard test` tests them.

Each draft keeps its `python/` layout and its binding's `skill:` path, so adding a rule
back is `git mv` of its files into `python/`, in a commit whose CI passes. A judge rule
moves its skill, binding and eval, once:

- every `invalid` and `valid` eval case passes 20 of 20 runs (`codeguard eval --repeat 20`)
  on its binding's model, checked before the commit; CI then repeats 3 runs;
- a judged review of codeguard with the rule loaded reports no false positive, and every
  real violation it finds is fixed in codeguard.

A pattern rule moves its rule, binding, test and snapshot, once
`codeguard review --all --dry-run` over codeguard flags nothing it shouldn't.

Rules are added back highest value first: rules about architecture and design before
rules about style.

Judge rules on every `.py` file except test files (Claude reads each changed file
against the rule's skill). `no-foreign-reexports` runs on `__init__.py` files only.

| Rule | Checks |
|---|---|
| `argument-group-names` | No `...Request`/`...Create` name on an in-process argument group |
| `behavior-on-data-owner` | A function that reads only one value's own data is a method of that value's type |
| `builder-names-step-builders` | `...Builder` only for step-by-step builders |
| `comments-state-reasons` | A comment states a reason the code can't hold, never what it does, did or doesn't do |
| `constructor-dependencies` | Methods don't take collaborators as parameters; the class gets them at construction |
| `context-types-live-with-consumer` | Dependency and context classes live with the stage that reads them |
| `docstrings-add-information` | A docstring tells the reader something the name, signature and body don't |
| `enum-usage` | No `.value` on a `StrEnum`, `IntEnum` or `TextChoices` member |
| `explicit-discriminated-unions` | A parsed union tags each variant and names its discriminator |
| `factory-methods-by-product` | Factory methods named for the product or input, not the caller |
| `factory-on-built-type` | A function that builds a new instance of a program class is defined on that class |
| `import-own-package-by-module` | Code inside a package imports from the defining module, never through a root that contains it |
| `import-packages-from-root` | Code outside a package imports from the package root, unless the root import would form a cycle |
| `interface-in-consumer-package` | An interface lives in the package of a consumer |
| `interfaces-earn-existence` | A Protocol or ABC has two implementers, or prevents an import cycle |
| `model-validators-intrinsic-only` | Model validators check only the model's own values |
| `names-match-behavior` | Every word of a function or class name is true of its body, and one names what it does |
| `narrow-collaborator-params` | No bundle parameter (context, settings, request) when only a few of its fields are read |
| `no-anonymous-tuples` | No tuple or fixed-key dict returning answers to different questions |
| `no-attribute-mirror-protocols` | No Protocol that copies one class's data attributes |
| `no-bare-identity-wrappers` | No class that only wraps one identifier |
| `no-branch-and-accumulate` | No loop that branches per item to pick what it appends, with no state between items |
| `no-copied-owner-values` | No stored copy of a held object's field or of the registry key |
| `no-duplicate-logic` | No function body copies another in the same file or an imported module |
| `no-foreign-reexports` | A package's `__init__.py` exports only names defined inside the package |
| `no-mutual-package-imports` | Two sibling packages never import from each other |
| `no-overlapping-responsibility` | No overlapping responsibility |
| `no-pre-derived-arguments` | No call to the program's own code passing both a value and the input it was derived from |
| `no-reimplemented-orchestration` | No calling a pipeline's stages in sequence when a component already runs them |
| `no-repeated-type-switches` | No two functions in a file switch on the same types |
| `no-shared-stateful-generics` | No shared instance of a class that stores a use's results on itself |
| `no-silent-key-overwrites` | A dict built from items doesn't silently drop items with a shared key |
| `no-single-use-map-wrappers` | No function that only maps a named function over a collection and has one call site |
| `no-single-use-shape-modules` | A shape only one type uses lives in that type's module |
| `one-concept-per-module` | One concept per module |
| `one-home-for-defaults` | Code outside a type doesn't supply defaults for that type's fields |
| `one-responsibility-per-function` | A function does one job's logic or coordinates calls, never a job's logic alongside other jobs |
| `one-responsibility-per-type` | A class's methods serve one concern, not unrelated groups |
| `one-verb-per-operation` | Collaborating functions and methods use one verb for one operation |
| `parameterized-helper` | No private sibling helpers that differ only by one literal or enum member |
| `queue-messages-carry-ids` | Stored records cross queues and workflows by id |
| `state-model-own-module` | A threaded state model gets its own module |
| `strenum-vs-literal` | No branching on, or keying a table by, a several-value `Literal` |
| `trust-established-invariants` | No guard re-checking a condition that visible code already guarantees |
| `types-live-with-producer` | Types live in the package that constructs them |
| `union-variants-together` | A union's variants are defined together, directly before its alias |
| `value-form-matches-role` | A supplied value's form fits its role: a reference carries an existing record's id, a matched value is fixed |

Judge rules on test files (`test_*.py`, `*_test.py`, `tests/**`, `conftest.py`):

| Rule | Checks |
|---|---|
| `assert-whole-objects` | No assert on a part (field, item, key, slice, membership) of a value that compares by value |
| `build-through-factory` | Build through the production factory |
| `configure-shared-fakes` | A subclass of a shared fake only configures it; its overrides never assert, query another subsystem or record that they ran |
| `deterministic-tests` | No assertion depends on the real clock, randomness, timing, set or listing order, or the machine's environment |
| `equality-over-in` | No `in` fragment check on a string, except a whole line inserted into content the test supplies |
| `helpers-only-set-up` | Helpers and fixtures never get a value from the production code that computes it |
| `helpers-return-what-they-build` | Helpers and fixtures return what they build, not a value got by using it |
| `integration-tests-catch-wiring` | A test in an integration or e2e suite runs two or more components together (files under `integration/` or `e2e/`, or named for them) |
| `mock-only-at-boundary` | A mock or patch replaces only code that leaves the process |
| `no-acting-fixtures` | The call a test asserts on runs in the test body, not in a fixture |
| `no-alternative-helper-inputs` | A helper takes each value through one parameter, not two it picks between |
| `no-dangling-parent-ids` | References in test data point at records the test created |
| `no-default-valued-arguments` | No argument equal to its parameter's default |
| `no-internal-call-assertions` | No assertion on the calls one of the program's components makes to another |
| `no-scenario-fixtures` | Fixtures build and ready the environment; they never run operations that set a test's starting state |
| `no-shared-test-class-state` | No test changes data stored on its test class |
| `no-single-use-fixtures` | A fixture in a test module is requested by more than one test or fixture there |
| `no-test-setup-bundles` | No test-only type that only carries built objects |
| `reuse-test-helpers` | No fake, stub, fixture or helper that duplicates one a shared test module provides |
| `seed-through-creator` | Test records are saved through their production creator |
| `separate-setup-and-data-fixtures` | A fixture sets a condition or returns a value, never both |
| `subject-built-in-test` | The object a test acts on is built in the test, not handed in by a fixture or setUp |
| `test-has-signal` | Every test can fail for a plausible bug that no other test in its file also catches |
| `test-isolation` | A test undoes every change to state that outlives it and releases every resource it acquires |
| `test-names-match-assertions` | A test's name claims only outcomes its assertions check |
| `test-names-use-production-terms` | A test's name uses the code under test's terms for its concepts |
| `test-owns-asserted-ids` | Asserted ids are written in the test, not read from a shared constant |
| `wide-scope-fixtures-share-no-state` | A fixture wider than function scope hands out nothing a test can change, and doesn't defer per-test cleanup |

Pattern rules (ast-grep) on app code:

| Rule | Checks |
|---|---|
| `no-forwarding-wrappers` | No undecorated non-method function whose only statement passes all its parameters (up to 5) unchanged to one call |
| `no-kwargs-for-named-params` | No named key read out of `**kwargs` (`kw["x"]`, `.get/.pop/.setdefault("x")`, `"x" in kw`) |
| `no-literal-lookup-branches` | No `if`/`elif`, consecutive-`if` or `match` chain mapping one value's constants to returned constants |
| `no-packing-helpers` | No function whose only statement returns its parameters packed into a same-name dict, `dict(...)` or tuple |
| `no-restated-type-args` | No subclass attribute restating its base's type argument |

Pattern rules (ast-grep) on test files:

| Rule | Checks |
|---|---|
| `no-attribute-set-after-build` | No attribute assignment on an object a test helper or fixture just constructed |
| `no-conftest-imports` | No import from a `conftest.py` |
| `no-empty-fixtures` | No fixture whose body is only `pass`, `...`, a docstring, a bare `return`/`yield` or `return None` |
| `no-kwargs-reads` | No read of a `**kwargs` parameter other than passing it on (`no-pop-from-kwargs` covers `pop`) |
| `no-stripped-result-copies` | No stripped copy of the result (dump with `exclude`, a `replace` that sets `None`, `del`/`pop` of a key, a filtered dict comprehension, a field set to `None`) that a later assert compares |
