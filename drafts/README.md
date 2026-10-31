# Draft rules

Judge rules and pattern rules that codeguard doesn't load. codeguard validates only the
ruleset directories named in `codeguard-package.yaml`, so nothing here runs. The gates
the drafts' bindings name are in `python/gates/`, or `general/gates/` for
`nontrivial-function`, where `codeguard test` tests them.

Each draft keeps its `python/` layout and its binding's `skill:` path, so adding a rule
back is `git mv` of its files into `python/`, in a commit whose CI passes. A judge rule
moves its skill, binding and eval, once:

- every `invalid` and `valid` eval case passes 20 of 20 runs (`codeguard eval --repeat 20`)
  on the binding's model, a Gemini model on Vertex AI (`provider: gemini`), checked
  before the commit;
- every case passes CI's 3 runs on each provider in its matrix, `gemini` and
  `claude-cli`; a failure on either fails the build.

One check comes after a rule ships and doesn't hold up the next rule. The README's
rule table tracks it for each rule, and the plan isn't done until every rule has
passed it:

- **Validation**: the rule ships as a `warning`, and its findings on real changes, read
  from codeguard's Logfire traces, show it flags what it should. A validated rule's
  binding moves to `error`.

A pattern rule moves its rule, binding, test and snapshot, once its rule tests have a
case for each branch and `codeguard test` passes.

A rule is shown accurate only by its own cases. Reviewing other code, codeguard's
included, is not part of the bar.

Running the Gemini check needs Google Cloud credentials for Vertex AI where the eval
runs.

Rules are added back highest value first: rules about architecture and design before
rules about style.

A judge rule states one convention, an abstract statement each piece of code keeps or
breaks, as codeguard's `writing-rules` skill requires; the judge reports where the
change breaks it. Its forms illustrate the convention on both sides: the convention
alone decides each form, and no form has its own definition of a violation. When a form
fails its evals, the convention is restated; the form isn't held back or carved out. Each code shape is on
the violation side of at most one rule, so a contradiction or overlap between two rules
is settled before either is added back. An architectural intent groups rules in these
tables; it is not itself a rule.

The judge rules below don't meet this yet. They were regrouped from about 75 narrow
drafts into one rule per intent, and most give each form its own violation definition,
so each is several claims. Before any is added back, every draft is split here into
one draft per claim, each with a single pass/fail, and each claim is marked with what
decides it:

- **ast-grep**: a code shape, decided by syntax. It becomes a pattern rule.
- **LSP**: a fact about symbols across the project, such as an interface's implementers
  or a function's references, which a language server answers exactly. codeguard has
  no language-server rules yet, so these claims are out of scope until it does; they
  wait in [Waiting on a language-server tier](#waiting-on-a-language-server-tier).
- **LLM**: judgment. It stays a judge rule.
- **drop**: low value next to the architecture rules, or it would flag idiomatic code.
  Each drop and its reason is recorded in the plan.

A claim an existing linter or import-linter already decides is out of scope: it
belongs in the app's linter configuration, not here. codeguard runs what a linter
can't decide; it isn't a linter or a wrapper for one.

[split-plan.md](split-plan.md) has each architecture draft's claims and what decides each.

A rule, its test and its eval cases ask for only as much scope as decides pass or fail.
Most judge rules are about the change: the test asks about each thing the change adds
or edits, answered from the code it touched and the definitions of names that code
uses. A rule that keeps something unique or consistent across the repository (one home
for a job, one word for one operation) asks whether the change adds a second one,
names the one search that finds the first, and has eval cases whose `unchanged` files
hold it.

Judge rules on every `.py` file except test files (the judge reads each changed file
against the rule's skill):

| Rule | Checks |
|---|---|
| `trust-the-boundary` | A guarantee is made once, where data enters or its type is built, and trusted after: no re-checks, parsed unions decide their variant, model validators use only the model's own values |
| `domain-in-data-structures` | A domain rule is stated once in a declared structure: no repeated type switches, branches on a `Literal` value set, anonymous multi-answer results, silent key overwrites, helpers differing by one value, or flags mirroring another field |
| `knowledge-has-one-home` | Each piece of knowledge (logic, a job on a concept, a pipeline's sequence, a domain answer about one object, a value an object holds, a set of things) has one home; no code copies what another place owns |
| `construction-has-one-home` | A program type's field values are decided on the type, in its module, in a factory whose injected collaborators decide them, or in a mapper for one source; a field's default is declared by the type |
| `layers-earn-their-load` | Every layer hides a real decision: no interface with one implementer, protocol mirroring one class's attributes, pass-through class, single-use map wrapper, argument group built only to be unpacked, or bare identity wrapper |
| `state-narrowest-scope-one-writer` | Mutable state has the narrowest scope its use needs and one writer: no shared instance of a stateful class, and no module- or class-level container or global holding one call's or one instance's data or written by two functions |
| `modules-own-knowledge` | Definitions live with the code they change with: one concept per module, shapes with their one owner, threaded state in its own module, types with their producer, context types and interfaces with their consumer, union variants as one run before the alias, no mutual sibling-package imports, no modules split by execution phase |
| `one-responsibility` | Each function or class has one job statable without "and": no function doing a job inline beside another job, no class serving unrelated concerns, no loop that works out each item's result by branching and collects it |
| `takes-what-it-needs` | A unit takes exactly what it needs, in the form its role needs: no collaborator passed per method call, no bundle taken to read a few fields, no value passed with the input it was derived from, no value in the wrong form for its role |
| `errors-surface-at-cause` | An error surfaces where it's caused: no except/suppress that swallows an error it doesn't handle, no silent fallback default for data that should exist, no clamp hiding a state that should never exist |
| `names-tell-the-truth` | Names, comments and docstrings say what the code does, in the domain's one word for it: no name that claims or hides behavior, second verb for one operation, request/action name on an in-process argument group, creation method named for its caller, one-shot `...Builder`, narrating comment, or repeating docstring |

Judge rules on test files (`test_*.py`, `*_test.py`, `tests/**`, `conftest.py`):

| Rule | Checks |
|---|---|
| `assertions-pin-the-contract` | Assertions check the behaviour the test names, no less and no more, against expected values the test states |
| `tests-survive-refactoring` | Tests depend only on observable results: no test double inside the process, assertion on internal calls, shared fake made to check or record, or copy of shared test support |
| `real-test-data` | Test data is made the way production makes it: no hand-built object a production factory builds, record saved around its production creator, reference to a record the test never created, or generated value where the receiver matches on fixed values |
| `arrange-act-assert-in-body` | A test shows its arrange, act and assert in its body: no subject handed in by a fixture or setUp, act or scenario run in a fixture, helper returning what it got by using an object, fixture both setting a condition and returning a value, single-use module fixture, setup bundle type, or helper taking one input two ways |
| `tests-dont-affect-each-other` | No test or fixture leaves state changed for the next test, changes data stored on its test class, or shares a changeable value or end-of-scope reset through a wide-scope fixture |
| `tests-earn-their-place` | Every test can fail for a plausible bug no other test in its file catches; in integration/e2e files a test crosses a seam between components; a test's name claims only what its assertions check, in the code under test's own terms |
| `no-default-valued-arguments` | No argument equal to its parameter's default (kept on its own: it's noise in a call, not setup hidden from the test body) |

Pattern rules (ast-grep) on every `.py` file:

| Rule | Checks |
|---|---|
| `no-kwargs-for-named-params` | No named key read out of `**kwargs` (`kw["x"]`, `.get/.pop/.setdefault("x")`, `"x" in kw`); iterating arbitrary keys is fine |

Pattern rules (ast-grep) on app code:

| Rule | Checks |
|---|---|
| `no-forwarding-wrappers` | No undecorated non-method function whose only statement passes all its parameters (up to 5) unchanged to one call |
| `no-literal-lookup-branches` | No `if`/`elif`, consecutive-`if` or `match` chain mapping one value's constants to returned constants |
| `no-packing-helpers` | No function whose only statement returns its parameters packed into a same-name dict, `dict(...)` or tuple |
| `no-restated-type-args` | No subclass attribute restating its base's type argument |

Pattern rules (ast-grep) on test files:

| Rule | Checks |
|---|---|
| `no-attribute-set-after-build` | No attribute assignment on an object a test helper or fixture just constructed |
| `no-conftest-imports` | No import from a `conftest.py` |
| `no-empty-fixtures` | No fixture whose body is only `pass`, `...`, a docstring, a bare `return`/`yield` or `return None` |
| `no-stripped-result-copies` | No stripped copy of the result (dump with `exclude`, a `replace` that sets `None`, `del`/`pop` of a key, a filtered dict comprehension, a field set to `None`) that a later assert compares |

## Decided for the split

- Domain answers away from their data (`knowledge-has-one-home`): the home is the
  module that declares the type, not only the class. A function the change adds or
  edits outside that module, computing a domain answer about the type from only its own
  data, is a violation; a module function beside the type is not.
- Anonymous results (`domain-in-data-structures`): stays. A project function returning
  `(user, created)` is a violation; unpacking a third-party API's result, such as
  Django's `get_or_create`, is not, since that shape isn't the change's.
- Docstrings that restate the name or signature (`names-tell-the-truth`): stays. It
  doesn't conflict with D401, which only sets a docstring's mood.
- One verb per operation (`names-tell-the-truth`): stays as a consistency rule. The
  synonym list becomes pairs of one operation under two verbs, so a judge doesn't read
  it as words that always mean the same.
- `names-tell-the-truth` splits into four judge rules and a pattern rule: the name is
  a true summary of its body (no word the body doesn't do, and a word for its main
  action; a creation method named for its caller is a form of this); a method does a
  sibling's operation under a different verb; a request- or action-named type the
  change builds only groups an in-process call's arguments; a comment or docstring the
  change adds says nothing the code doesn't. A `*Builder` class with no part methods
  before `build()` is a pattern rule. Commented-out code and bare TODOs go to ruff
  (ERA001, TD003). FIX002 is left out: it flags every TODO, including one with a
  tracker link, which the draft allows.
  Revised in the split plan after review: the request-named type claim needs where the
  type is built and read across the repository, so it waits for the language-server
  tier; the comment test becomes "states no fact from outside the code", since a
  comment like `# doesn't handle refunds` says something the code doesn't and the draft
  still flags it.

Splitting costs judge calls only where a change touches more than one split rule's
trigger: one judge call measured about 3.8 s, 200 output tokens and $0.02 on
`claude-sonnet-5-5`. Anthropic's and Google's guidance both favour one criterion per
judge call.

## Proposed codeguard changes

- A language-server rule kind (below).
- The code under review comes before the rule in each judge call, so rules judging the
  same file share it from the prompt cache. Today each rule's instructions are the
  system prompt, so the cached prefix differs per rule.

## Waiting on a language-server tier

A proposed codeguard rule kind: an ast-grep match on the changed code picks a symbol, one
language-server query (`textDocument/implementation`, `textDocument/references`) runs
on it, and a test on the result decides the rule, with no model call. basedpyright's
language server answers both queries, including a `Protocol`'s structural implementers
that never name it. These claims are taken out of the judge drafts until codeguard
supports it:

- An interface (`Protocol` or ABC) has two or more implementers outside test code.
- A function or method whose whole body maps an already-named function over its input
  has more than one call site.
- A passive shape used by only one type lives in that type's module.
- A data type, result, record, exception or enum lives in the module that builds it.
- A protocol is more than a mirror of one class's data attributes.
- A context type lives in its consumer's package.
- An interface lives in its consumer's package.
- A request- or action-named type is more than an in-process call's argument group,
  judged from where it is built and read.

## Import-graph tier candidates

These claims were removed from the judge drafts: they're about the import graph, which an
import linter checks across the whole project better than a per-file judge.

- Code outside a package imports the package's names from the package root, never from a
  module inside it, unless importing from the root would form an import cycle.
- Code inside a package imports names from the module that holds them, never through the
  root of a package that contains the file.
- A package's `__init__.py` exports only names defined inside the package's directory,
  never a name it imports from outside the package.
