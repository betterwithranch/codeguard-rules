# codeguard-rules

Rulesets for [codeguard](https://github.com/betterwithranch/codeguard). Each ruleset is a
directory a project opts into from its `.codeguard/config.yaml`. The rules supplement a
linter; they don't repeat one. A Python project should run
[ruff](https://docs.astral.sh/ruff/) for what it covers, such as `print` (T201), imports
inside functions (PLC0415), `getattr` with a literal (B009) and `TYPE_CHECKING` (TID251),
and [basedpyright](https://docs.basedpyright.com) with these rules on:

- `reportExplicitAny`: no `Any`.
- `reportMissingTypeArgument`: generic annotations and base classes are parameterized.
- `reportGeneralTypeIssues` (on in `standard`): every TypeVar is bound by its class, and
  variance matches use.
- `reportArgumentType` (on in `standard`): pass enum members, never a bare literal.
- `reportUnnecessaryIsInstance`, `reportUnnecessaryComparison`: no re-checks of a fact
  the types already guarantee.

## Rulesets

### `python`

Rules for any Python project. No framework rules. Each rule checks one thing, so a
project can exclude any of them.

Pattern rules (ast-grep). Rules about tests run only on test files; rules about app
code skip test files:

| Rule | Checks |
|---|---|
| `all-only-in-init` | `__all__` only in `__init__.py` or a `.pyi` stub |
| `no-assert-in-fixtures` | No `assert` inside a pytest fixture |
| `no-append-in-every-branch` | No loop `if`/`else` that appends to the same list in every branch |
| `no-assert-on-lookup-field` | Don't assert the field used to find an item |
| `no-bucket-module-names` | No `utils`, `helpers`, `common`, `shared`, or `contracts` modules |
| `no-comments-in-tests` | No comments in test files, except tool directives |
| `no-constructed-test-constants` | No module-level `UPPER = SomeClass(...)` in test files; build it in a fixture |
| `no-default-constructor-fixtures` | No fixture or test helper that only returns `SomeClass()` |
| `no-del-param` | No `del` of a parameter to mark it unused. Prefix it with `_`. |
| `no-dict-round-trip-between-models` | No `asdict`/`model_dump` round-trip from one model into another |
| `no-field-tuple-asserts` | Don't assert a tuple of one value's fields; compare the whole object |
| `no-len-asserts` | Don't assert only a collection's length |
| `no-manual-kwargs-check` | No hand-written `TypeError` for unexpected `**kwargs` keys |
| `no-normalized-asserts` | No `replace`, `model_copy` or `model_dump(exclude=...)` of the result inside an assert |
| `no-pop-from-kwargs` | No `.pop()` from a `**kwargs` parameter in test code |
| `no-sleep-in-async-tests` | No `sleep` in an `async def test_…`; wait on an event |
| `no-tuple-fixtures` | A pytest fixture returns or yields one object, never a tuple |
| `typed-dispatch-registries` | A class takes a registry, not a `dict[str, Callable]` |

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
| `no-dead-code` | No dead code |
| `no-duplicate-logic` | No duplicate logic |
| `no-overlapping-responsibility` | No overlapping responsibility |
| `no-pre-derived-arguments` | No pre-derived arguments |
| `no-reimplemented-orchestration` | Do not re-implement orchestration |
| `no-shared-stateful-generics` | No shared instances of stateful generic classes |
| `one-concept-per-module` | One concept per module |
| `one-form-per-input` | One way to specify each input |
| `one-home-for-defaults` | One home for defaults |
| `one-responsibility-per-function` | One responsibility per function |
| `one-responsibility-per-type` | One responsibility per type |
| `package-cohesion` | Package cohesion |
| `package-public-interface` | Package public interface |
| `parameterized-helper` | One parameterized helper, not one method per variant |
| `parse-boundary-data-once` | Parse boundary data once |
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

A judge rule runs on a changed file only when a changed line falls inside code it could
flag. Its binding's `triggers` names that code: a change kind built into codeguard, such
as `fixture` or `import`, or a gate in `python/gates/`, an ast-grep rule such as
`mock-use`. A rule ast-grep or the type checker can check is a pattern rule or a checker
setting, never a judge rule.

## Use a ruleset

In the project's `.codeguard/config.yaml`:

```yaml
packages:
  - git: https://github.com/betterwithranch/codeguard-rules.git
    ref: v0.2.0
    rulesets:
      python:
        exclude: [no-del-param, no-dead-code]
        rules:
          no-dead-code:
            paths: ["src/**/*.py"]
            severity: warning
```

- `exclude` turns rules off.
- `rules.<id>` overrides `paths`, `exclude_paths` or `severity`, and `model` on a judge
  rule. `exclude_paths: []` brings test files back into an app rule.
- `codeguard update` moves `ref` to the newest tag.

Diagnostics name a rule by package, ruleset and id: `betterwithranch/python/no-del-param`.

The pattern rules work with ast-grep `>=0.45,<0.46`, set in `codeguard-package.yaml`. A
project that sets `ast-grep` in its config must pick a version in that range.

## Layout

```
codeguard-package.yaml                 # name, rulesets and supported ast-grep versions
python/
  rules/pattern/<id>.yml               # ast-grep rules
  rule-tests/pattern/<id>-test.yml     # their tests and __snapshots__/
  gates/<id>.yml                       # ast-grep rules that decide when a judge rule runs
  rule-tests/gates/<id>-test.yml       # their tests and __snapshots__/
  skills/<id>/SKILL.md                 # judge rules
  bindings/<id>.yaml                   # a skill or pattern rule and its default paths
  rule-evals/<id>-eval.yml             # judge rule evals
  rule-evals/<id>/                     # their case files
```

codeguard rejects any other entry in a ruleset directory.

## Test

```sh
codeguard test               # pattern rule and gate tests; warns on broad triggers
codeguard test --update-all  # regenerate snapshots
codeguard eval               # judge rule evals and the rule review; calls Claude
```

An eval lists case files the judge must pass (`valid`) and must flag at the confidence
threshold (`invalid`). Name case files for their code, not their expected result, because
the judge reads their directory.
