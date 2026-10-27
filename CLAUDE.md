# codeguard-rules

The rule package codeguard reviews with. [README.md](README.md) explains the layout and
the tests.

## Scope

codeguard makes coding agents follow a project's conventions: it loads a rule's skill
before an agent edits a file, and reviews each change with pattern rules and an LLM
judge at the agent's Stop hook and in CI.

The point of this repository is a set of standards a project can adopt easily, by
enabling a ruleset, without writing or maintaining checks of its own. Linters already do
that for what their built-in rules cover, so codeguard doesn't reinvent linting: it
isn't a linter and doesn't wrap one.

This repository holds only codeguard rules that any project can use:

- **Pattern rules** (ast-grep), for a claim syntax decides exactly.
- **Judge rules** (a skill bound to files by a binding), for a claim that needs
  judgment, with the **gates** that pick the code each one reads.

What doesn't belong here:

- **A linter's built-in rules and settings.** A claim a built-in rule of a mainstream
  linter for that language decides (ruff, basedpyright or import-linter for Python) is
  the app's to turn on in its own lint configuration, and gets no rule here. Don't
  recommend linter settings in this repository either.
- **A project's own conventions.** Rules only one app (such as otter) needs live in that
  app's `.codeguard/`, along with which rulesets it enables and at what severity.

A claim no built-in linter rule decides belongs here, even when a project could write a
custom linter plugin for it (a Pylint checker): a project adopting these standards
shouldn't have to write or keep custom lint rules.

Choosing a tool for a claim:

1. If a built-in rule of a linter for the language decides it, it isn't a rule here.
2. Else, if ast-grep decides it exactly, it's a pattern rule, never a judge rule. A
   judge rule with a mechanical part is split: the pattern rule owns that part.
3. Otherwise it's a judge rule. A part that can't be matched without false positives
   stays in the judge rule.

Each claim is written in exactly one place, and idiomatic code never fails a rule.
Every rule says why it exists: a judge rule in its skill's `## Why` section, a pattern
rule in `metadata.why`, each with an optional source.

Drafts in `drafts/` aren't loaded by codeguard. They're promoted highest value first:
architecture and design, then test design, then style and naming.

codeguard's design and decisions are recorded in the vault (obsidian-vault,
`10 Personal/Projects/Agent Coding Quality/`): `codeguard/Architecture.md`,
`Rules Implementation Plan.md` and `History/codeguard Decisions.md`. Ask the user when a
change seems to need a decision those don't cover.

## Rules

Before adding or changing a rule, and whenever a rule test or eval fails, flips between
runs or reports a warning, load codeguard's `writing-rules` skill and follow it, and the
references it points to. A case that fails is fixed in the rule's criterion or in the
case, never by re-running it until it passes.

This repository owns its rules' accuracy, and proves it only with its own tests run
through codeguard: `codeguard test` for pattern rules and gates, `codeguard eval` for
judge rules. Reviewing other code, codeguard's included, is not part of that.

## Repositories

Work only in this repository. Don't attach other repositories; ask the user for any
reference material you need.
