# codeguard-rules

The rule package codeguard reviews with. [README.md](README.md) explains the layout and
the tests.

## Rules

[docs/rule-design.md](docs/rule-design.md) records how rules here are designed and the
mistakes already corrected. Read it before changing a rule or an eval, and add to it
when a design mistake is corrected.

Before adding or changing a rule, and whenever a rule test or eval fails, flips between
runs or reports a warning, load codeguard's `writing-rules` skill and follow it and its
judge rule guide (`references/judge-rules.md`). A case that fails is fixed in the rule's
criterion or in the case, never by re-running it until it passes.

This repository owns its rules' accuracy, and proves it only with its own tests run
through codeguard: `codeguard test` for pattern rules and gates, `codeguard eval` for
judge rules. Reviewing other code, codeguard's included, is not part of that.

## Repositories

Work only in this repository. Don't attach other repositories; ask the user for any
reference material you need.
