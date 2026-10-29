# codeguard-rules

Rulesets for [codeguard](https://github.com/jig-code/codeguard). Each ruleset is a
directory a project opts into from its `.codeguard/config.yaml`. The rules supplement a
linter; they don't repeat one. A Python project should run
[ruff](https://docs.astral.sh/ruff/) for what it covers, such as `print` (T201), imports
inside functions (PLC0415), `getattr` with a literal (B009), `TYPE_CHECKING` (TID251),
untyped parameters (ANN001, ANN003) and unused arguments (ARG001),
but not the missing-docstring rules (D100–D107), which push docstrings that restate the
name, and [basedpyright](https://docs.basedpyright.com) with these rules on:

- `reportExplicitAny`: no `Any`.
- `reportAny`: no value of type `Any`, such as an untyped `json.loads`, `yaml.safe_load`
  or `.json()` result read before it's parsed into a declared type.
- `reportMissingTypeArgument`: generic annotations and base classes are parameterized.
- `reportGeneralTypeIssues` (on in `standard`): every TypeVar is bound by its class, and
  variance matches use.
- `reportArgumentType` (on in `standard`): pass enum members, never a bare literal.
- `reportUnnecessaryIsInstance`, `reportUnnecessaryComparison`: no re-checks of a fact
  the types already guarantee.

## Rulesets

### `general`

Architecture rules for any language. Most are judge rules. A judge rule's `SKILL.md`
states the convention in no language's terms, and a supplement beside it for each
language, `python.md` and `typescript.md`, gives that language's forms and examples. The judge
gets the skill and the supplement for the file's language. Its binding's `paths` name
the languages it runs on.

| Rule | Checks | Validated |
|---|---|---|
| `dry` | Don't Repeat Yourself: code the change adds doesn't state a computation, process, set or outside shape again when the file or a module it imports already states it | Not yet |
| `domain-logic-separate-from-io` | Domain logic separate from I/O: a domain decision is made in code that does no I/O, so a function the change adds or edits doesn't decide and read or change state outside the program in the same body | Not yet |
| `single-responsibility` | Single responsibility: a function or class has one reason to change, so a function's own body doesn't hold the details of two concerns (business rules, an outside system, a data format) and a class's methods don't serve two | Not yet |
| `no-repeated-switches` | No repeated switches: behaviour chosen by which kind a value is (its class, or an enum member or tag naming its variant) is chosen in one place, unless the type checker proves every place covers every kind | Not yet |
| `no-feature-envy` | No feature envy: a domain answer computed from one type's data lives in that type's module, so code elsewhere doesn't work an answer out from one value's fields alone | Not yet |
| `fail-fast` | Fail fast: a failure, missing data or an impossible state is reported where it's found, so code the change adds doesn't swallow an error, default data that should exist, clamp an impossible value or drop the items that failed | Not yet |
| `no-shared-mutable-state` | No shared mutable state: data belonging to one call or use is kept where only that call or use sees it, so code the change adds doesn't keep one call's data in module-level state or store each use's results on a shared instance | Not yet |
| `liskov-substitution` | Liskov substitution: a subclass keeps every promise its base class makes, so an override the change adds doesn't raise where the base doesn't, ignore an argument, accept or return less, or stub out the base's work | Not yet |
| `no-shotgun-surgery` | No shotgun surgery: one type owns each job on a concept, so a type the change adds or edits doesn't do a job another type already does to the same concept | Not yet |
| `construction-in-its-home` | Construction in its home: what a new instance holds is decided by its type, its module, its factory or its source's mapper, so code the change adds doesn't build a program type from a source elsewhere or supply a default for one of its fields | Not yet |
| `make-illegal-states-unrepresentable` | A type's optional fields aren't tied to the values of its status or kind field | Not yet |
| `composition-over-inheritance` | A class inherits only from a type it is a kind of, not to reuse its code | Not yet |

Pattern rules (ast-grep), one per language where a convention's form is syntax. They
start as `warning`s and skip test files:

| Rule | Checks |
|---|---|
| `no-middle-man-python`, `no-middle-man-typescript` | No middle man: a class without a base doesn't forward every method to the same collaborator |

Each judge rule passes 20 of 20 eval runs on Claude before it ships, and CI's 3 runs
before it merges. One check follows, and doesn't hold up the next rule:

- **Validated**: its findings on real changes, read from codeguard's Logfire traces,
  show it flags what it should. Until then it's a `warning`: its findings print but don't
  block. Once validated, its binding's `severity` moves it to `error`.

A rule's evals have cases in each language, reported apart, such as `dry (python)` and
`dry (typescript)`. Gates in `general/gates/` are ast-grep rules for one language each;
on a TypeScript file, every trigger fires.

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

The `python` ruleset has no judge rules yet. Its judge rules, and some pattern rules, are drafts in
`drafts/python/`, which codeguard doesn't load. A draft moves into a ruleset one rule at a time, in the order in
[drafts/split-plan.md](drafts/split-plan.md), highest
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
as `fixture` or `import`, or a gate in the ruleset's `gates/`, an ast-grep rule
such as `mock-use`. A rule ast-grep or the type checker can check is a pattern rule or a checker
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
general/, python/            # one directory per ruleset
  rules/pattern/<id>.yml     # ast-grep rules
  gates/<id>.yml             # ast-grep rules that decide when a judge rule runs
  rule-tests/<id>-test.yml   # tests for both, with __snapshots__/
  skills/<id>/SKILL.md       # judge rules
  skills/<id>/<language>.md  # a judge rule's forms and examples in one language
  bindings/<id>.yaml         # a skill or pattern rule and its default paths
  rule-evals/<id>.yaml       # judge rule evals: cases codeguard judges with the binding
```

codeguard rejects any other entry in a ruleset directory.

## Test

```sh
task test                # codeguard test: pattern rule and gate tests, eval triggers
task test -- -U          # the same, regenerating snapshots
task eval                # codeguard eval: judge each judge rule eval case; calls Claude
```

`CODEGUARD=<path>` runs another codeguard build, such as a checkout's `.venv/bin/codeguard`.

A Claude Code session here installs codeguard at the release CI pins (`CODEGUARD_REF`
in `.github/workflows/ci.yaml`) when it starts, through `.claude/hooks/session-start.sh`,
so local runs match CI. Moving to a new codeguard release is that one line.

CI judges only the rules a change can affect: a rule whose skill, binding, eval or a
trigger's gate changed, or every rule when `codeguard-package.yaml`, the workflow or
`scripts/affected_judge_rules.py` changed. That script prints the affected rules, and
CI passes each to `codeguard eval --rule`. The `eval` job runs once per provider in its
matrix, `claude-cli`. Gemini is out of the matrix until codeguard's Gemini judge
is faster and steadier; its auth step stays, so adding `gemini` back turns it on. Locally, `codeguard eval --rule <id> --repeat 20` judges one
rule, and `--provider gemini` judges it with Gemini instead of its binding's model.

[Which test to write](https://github.com/jig-code/codeguard#which-test-to-write)
says which test covers which change. Every judge rule has a rule eval with `invalid`,
`valid` and `skipped` cases, each named after what its edit does. Each case is a clear
violation, a clear non-violation, or clearly outside the rule's gate. A case a reviewer
could argue either way doesn't belong in a rule eval.

A case or finding that flips between runs, or comes back as a low-confidence warning,
means the rule's criterion or the case is unclear. Fix the criterion or the case. Don't
re-run or loosen the gate. [CLAUDE.md](CLAUDE.md) has the details.

The rules are tested only by their own cases, through codeguard, so they are shown
accurate as codeguard runs them. CI's `test` job runs `codeguard test`, then its `eval`
job runs `codeguard eval --repeat 3` with each provider; a case that fails or isn't
judged in any run fails the build. The `eval` job needs, in the repository's Actions
settings, the secret `CLAUDE_CODE_OAUTH_TOKEN` for Claude, and for Gemini the secret
`GOOGLE_CREDENTIALS` (a service account key with the Vertex AI User role) and the
variable `GOOGLE_CLOUD_PROJECT`. codeguard's README, under "Judge with Gemini on Google
Cloud", has the setup.
CI runs the codeguard release in `CODEGUARD_REF` in `.github/workflows/ci.yaml`, so
moving to a new release is a change here, which judges every rule.
