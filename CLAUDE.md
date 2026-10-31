# codeguard-rules

The rule package codeguard reviews with. [README.md](README.md) explains the layout and
the tests.

## Rules

Before adding or changing a rule, and whenever a rule test or eval fails, flips between
runs or reports a warning, load codeguard's `writing-rules` skill and follow it, and the
references it points to. A case that fails is fixed in the rule's criterion or in the
case, never by re-running it until it passes.

This repository owns its rules' accuracy, and proves it only with its own tests run
through codeguard: `codeguard test` for pattern rules and gates, `codeguard eval` for
judge rules. Reviewing other code, codeguard's included, is not part of that.

Judge rules are judged with their binding's `provider` and `model`: Gemini on Vertex AI
(`dry` on `gemini-4-argon`), in local `task eval` and in CI. CI's `eval`
job also judges each affected rule with Claude Haiku 5.5 on Bedrock. A rule moves to another
model only by setting it in its binding and passing its evals there.

## Repositories

Work only in this repository. Don't attach other repositories; ask the user for any
reference material you need.
