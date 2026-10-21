# Draft judge rules

Judge rules that codeguard doesn't load. codeguard validates only the ruleset
directories named in `codeguard-package.yaml`, so nothing here runs.

Each draft keeps its `python/` layout and its binding's `skill:` path, so adding a rule
back is `git mv` of its skill, binding and eval into `python/`, in a commit whose CI
passes:

- every `invalid` and `valid` eval case passes 3 of 3 runs (`codeguard eval --repeat 3`)
  on the model its binding names;
- a judged review of codeguard with the rule loaded reports no false positive, and every
  real violation it finds is fixed in codeguard.

Rules are added back highest value first: rules about architecture and design before
rules about style.

Judge rules on every `.py` file except test files (Claude reads each changed file
against the rule's skill). `comments-and-docstrings` also runs on test files.

| Rule | Checks |
|---|---|
| `behavior-on-data-owner` | Behavior lives on the type whose data it reads |
| `comments-and-docstrings` | Comments and docstrings only where no structure or name can hold the reason |
| `constructor-dependencies` | Constructor state over repeated arguments |
| `enum-usage` | No `.value` on an enum member |
| `explicit-discriminated-unions` | Discriminated unions are explicit |
| `function-has-owner` | Every loose function has an owner |
| `interfaces-earn-existence` | Interfaces must earn their existence |
| `map-models-field-by-field` | Map between models field by field |
| `names-match-behavior` | Names match what the code does |
| `narrow-collaborator-params` | Pass only what a collaborator needs |
| `no-anonymous-tuples` | No anonymous tuples or dicts for concepts |
| `no-branch-and-accumulate` | No branch-and-accumulate loops |
| `no-duplicate-logic` | No duplicate logic |
| `no-overlapping-responsibility` | No overlapping responsibility |
| `no-pre-derived-arguments` | No pre-derived arguments |
| `no-reimplemented-orchestration` | Do not re-implement orchestration |
| `no-shared-stateful-generics` | No shared instances of stateful classes |
| `no-single-use-shape-modules` | No single-use shape modules |
| `one-concept-per-module` | One concept per module |
| `one-home-for-defaults` | One home for defaults |
| `one-responsibility-per-function` | One responsibility per function |
| `one-responsibility-per-type` | One responsibility per type |
| `package-cohesion` | Package cohesion |
| `package-public-interface` | Package public interface |
| `parameterized-helper` | One parameterized helper, not one method per variant |
| `state-model-own-module` | Threaded state models get their own module |
| `strenum-vs-literal` | `StrEnum` or `Literal`, by how the value is used |
| `trust-established-invariants` | Trust established invariants |
| `type-args-in-init-subclass` | Read type arguments in `__init_subclass__` |
| `type-name-suffixes` | Standard type-name suffixes |
| `types-live-with-producer` | Types live with their producer |
| `types-model-domain-concepts` | Types model real domain concepts |
| `value-form-matches-role` | A supplied value's form matches its role |

Judge rules on test files (`test_*.py`, `*_test.py`, `tests/**`, `conftest.py`):

| Rule | Checks |
|---|---|
| `arrange-act-assert-in-test` | Arrange, act, and assert stay in the test body |
| `assert-whole-objects` | Assert whole result objects |
| `build-through-factory` | Build through the production factory |
| `configure-shared-fakes` | Extend shared fakes by configuration |
| `deterministic-tests` | Tests are deterministic |
| `equality-over-in` | Prefer `==` over `in` |
| `fixture-shape` | Fixture shape |
| `helpers-only-set-up` | Helpers set up; they never perform the act |
| `integration-tests-catch-wiring` | Integration tests catch a wiring bug (files under `integration/` or `e2e/`, or named for them) |
| `mock-only-at-boundary` | Mock only at the process boundary |
| `no-normalized-results` | Do not normalize the result before asserting |
| `no-wrapper-fixtures` | No wrapper or projection fixtures |
| `real-test-data` | Use real data, real parents, and real ids |
| `reuse-test-helpers` | Reuse shared fakes and helpers |
| `test-has-signal` | Every test has signal |
| `test-helper-parameters` | Construction helper parameters |
| `test-isolation` | Test isolation |
| `test-names-match-assertions` | Test names match assertions and vocabulary |

