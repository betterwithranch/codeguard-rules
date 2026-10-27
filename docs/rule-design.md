# Rule design

How rules in this package are designed, and the mistakes already corrected. Read it
before adding or changing a rule or an eval. [drafts/README.md](../drafts/README.md)
has the promotion bar and what was decided for each draft.

## A rule

- **One claim, one yes/no test.** A rule's forms illustrate that test on both sides;
  the test alone decides each form, and no form defines its own violation. A rule
  whose top-level test only points at its forms ("in a way a form below names") is
  several rules.
- **The cheapest exact tool decides it.** In order: a linter or type checker setting
  (ruff, basedpyright's `reportAny`), import-linter, an ast-grep pattern rule, a
  language-server query, and only then a judge rule. A judge rule is for judgment,
  never for something syntax, types or a symbol lookup decide.
- **Scoped to the change.** A rule and its cases ask for only as much as decides pass
  or fail: the code the change adds or edits, and the definitions of names it uses.
  Only a rule that keeps something unique or consistent across the repository (one
  home for a job, one word for one operation) searches beyond that, and it names the
  one search it needs.
- **Plain language.** Write a rule the way a reviewer would say it. No invented terms
  ("shape read"); if the rule needs a word nobody uses, the rule isn't clear yet.
- **Idiomatic Python never fails a rule.** A bad pattern isn't idiomatic because a
  framework uses it: calling Django's `get_or_create` is fine, writing a project
  function that returns `(user, created)` isn't.
- **Each code shape is on the violation side of at most one rule.** Settle a
  contradiction or overlap between two rules before either is promoted.

## Proving a rule

- **Only by its own cases, run through codeguard**: `codeguard test` for pattern rules
  and gates, `codeguard eval` for judge rules, at the codeguard release CI pins.
  Reviewing other code, codeguard's included, is not part of it.
- **A case shows what's at stake.** A reader of the case alone sees why the code is a
  problem or why it is fine; its name says that, not only what the code does. A case
  doesn't mix in a second defect (a CSV split on `","` is also just a bug).
- **A case a reviewer could argue either way is fixed or dropped.** Don't change a
  rule's wording to get a weak case to pass.
- **A failing or flipping case is fixed in the rule or the case**, never by re-running
  it until it passes.
- **Open: the eval method.** codeguard runs evals as pydantic-evals datasets, but the
  cases are hand-written boundary pairs that must all pass every run, which is closer
  to unit testing. It is being aligned with the eval practice used elsewhere (otter);
  no new eval cases are written until that's settled.
