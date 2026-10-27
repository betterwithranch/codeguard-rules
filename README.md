# codeguard-rules

Rulesets for [codeguard](https://github.com/betterwithranch/codeguard). Each ruleset is a
directory a project opts into from its `.codeguard/config.yaml`. The rules supplement a
linter; they don't repeat one. A Python project should run
[ruff](https://docs.astral.sh/ruff/) for what it covers, such as `print` (T201), imports
inside functions (PLC0415), `getattr` with a literal (B009), `TYPE_CHECKING` (TID251),
untyped parameters (ANN001, ANN003) and unused arguments (ARG001),
but not the missing-docstring rules (D100–D107), which push docstrings that restate the
name, and [basedpyright](https://docs.basedpyright.com) with these rules on:

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
| `no-asserting-action-helpers` | No test helper that asserts and then returns a call |
| `no-clock-moves-in-fixtures` | No sleep or clock tick inside a pytest fixture |
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
| `one-form-per-input` | No parameter reconciled from another parameter when missing (`if index is None: index = build(catalog)`) |
| `typed-dispatch-registries` | A class takes a registry, not a `dict[str, Callable]` |

Judge rules on every `.py` file except test files (Claude reads each changed file
against the rule's skill):

| Rule | Checks |
|---|---|
| `parse-boundary-data-once` | Outside data is read only through the part of the program that declares and checks its shape |

The other judge rules, and some pattern rules, are drafts in `drafts/python/`, which
codeguard doesn't load. A draft moves back into `python/` one rule at a time, highest
value first: a judge rule once it passes every eval case 20 of 20 runs on each eval
provider, a pattern rule once its rule tests cover each branch and pass. codeguard's
`writing-rules` skill has the steps, and [drafts/README.md](drafts/README.md) the
conditions.

Reviews and evals both judge a rule with its binding's `provider` and `model`, and a
project can't override them, so a rule is only ever judged by the model its evals pass
on. The bindings here leave both out, so codeguard's default, `claude-sonnet-5-5`
through the `claude` CLI, judges them. To move a rule to another model, set them in its
binding and pass its evals again. [drafts/README.md](drafts/README.md) lists them.

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
        exclude: [no-del-param, no-duplicate-logic]
        rules:
          names-match-behavior:
            paths: ["src/**/*.py"]
            severity: warning
```

- `exclude` turns rules off.
- `rules.<id>` overrides `paths`, `exclude_paths` or `severity`. `exclude_paths: []`
  brings test files back into an app rule.
- `codeguard update` moves `ref` to the newest tag.

Diagnostics name a rule by package, ruleset and id: `betterwithranch/python/no-del-param`.

The pattern rules work with ast-grep `>=0.45`, set in `codeguard-package.yaml`. A
project that sets `ast-grep` in its config must pick a version in that range.

## Layout

```
codeguard-package.yaml       # name, rulesets, and supported ast-grep and codeguard versions
python/
  rules/pattern/<id>.yml     # ast-grep rules
  gates/<id>.yml             # ast-grep rules that decide when a judge rule runs
  rule-tests/<id>-test.yml   # tests for both, with __snapshots__/
  skills/<id>/SKILL.md       # judge rules
  bindings/<id>.yaml         # a skill or pattern rule and its default paths
  rule-evals/<id>.yaml       # judge rule evals: cases codeguard judges with the binding
```

codeguard rejects any other entry in a ruleset directory.

## Test

```sh
task test                # codeguard test: pattern rule and gate tests, eval triggers
task test -- -U          # the same, regenerating snapshots
task eval                # codeguard eval: judge each eval case and review each rule; calls Claude
```

`CODEGUARD=<path>` runs another codeguard build, such as a checkout's `.venv/bin/codeguard`.

CI judges only the rules a change can affect: a rule whose skill, binding, eval or a
trigger's gate changed, or every rule when `codeguard-package.yaml`, the workflow or
`scripts/affected_judge_rules.py` changed. That script prints the affected rules, and
CI passes each to `codeguard eval --rule`. The `eval` job runs once per provider in its
matrix (`claude-cli` today). Locally, `codeguard eval --rule <id> --repeat 20` judges one
rule, and `--provider gemini` judges it with Gemini instead of its binding's model.

[Which test to write](https://github.com/betterwithranch/codeguard#which-test-to-write)
says which test covers which change. Every judge rule has a rule eval with `invalid`,
`valid` and `skipped` cases, each named after what its edit does. Each case is a clear
violation, a clear non-violation, or clearly outside the rule's gate. A case a reviewer
could argue either way doesn't belong in a rule eval.

A case or finding that flips between runs, or comes back as a low-confidence warning,
means the rule's criterion or the case is unclear. Fix the criterion or the case. Don't
re-run or loosen the gate. [CLAUDE.md](CLAUDE.md) has the details.

The rules are tested only by their own cases, through codeguard, so they are shown
accurate as codeguard runs them. CI's `test` job runs `codeguard test`, then its `eval`
job runs `codeguard eval --repeat 3` with Claude; a case that fails or isn't judged in
any run fails the build. The `eval` job needs the repository secret `CLAUDE_CODE_OAUTH_TOKEN`.
CI runs the codeguard release in `CODEGUARD_REF` in `.github/workflows/ci.yaml`, so
moving to a new release is a change here, which judges every rule.
