# codeguard-rules

Rulesets for [codeguard](https://github.com/betterwithranch/codeguard). Each ruleset is a
directory a project opts into from its `.codeguard/config.yaml`.

## Rulesets

### `python`

Rules for any Python project. No framework rules.

Pattern rules (ast-grep):

| Rule | Checks |
|---|---|
| `no-print` | No `print` calls. Use a logger, or `sys.stdout` in a command-line tool. |
| `no-del-param` | No `del` of a parameter to mark it unused. Prefix it with `_`. |
| `no-type-checking` | No `if TYPE_CHECKING:` blocks. Fix the import cycle. |
| `import-at-module-level` | No imports inside functions. |
| `no-getattr-literal` | No `getattr(obj, "name")`. Write `obj.name`. |

Judge rules (Claude reads each changed file against the skill):

| Rule | Files | Checks |
|---|---|---|
| `python-code-quality` | `**/*.py` | Naming, module structure, responsibility, function design, typing, duplication. |
| `test-quality` | test files and `conftest.py` | Determinism, signal, mocking, assertions, helpers, fixtures. |
| `python-generics` | `**/*.py` | TypeVar binding, parameterized annotations, variance. |

Each judge rule makes one Claude call per changed file it matches.

## Use a ruleset

In the project's `.codeguard/config.yaml`:

```yaml
packages:
  - git: https://github.com/betterwithranch/codeguard-rules.git
    ref: v0.1.0
    rulesets:
      python:
        exclude: [no-print]
        rules:
          python-code-quality:
            paths: ["src/**/*.py"]
            severity: warning
```

- `exclude` turns rules off.
- `rules.<id>` overrides `paths` or `severity`, and `model` on a judge rule.
- `codeguard update` moves `ref` to the newest tag.

Diagnostics name a rule by package, ruleset and id: `betterwithranch/python/no-print`.

## Layout

```
codeguard-package.yaml                 # name and rulesets
python/
  rules/pattern/<id>.yml               # ast-grep rules
  rule-tests/pattern/<id>-test.yml     # their tests and __snapshots__/
  skills/<id>/SKILL.md                 # judge rules
  bindings/<id>.yaml                   # skill path (from the repo root) and default paths
```

## Test

```sh
codeguard test               # every ruleset's pattern rule tests
codeguard test --update-all  # regenerate snapshots
```
