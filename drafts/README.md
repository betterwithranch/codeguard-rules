# Draft rules

Judge rules and pattern rules that codeguard doesn't load. codeguard validates only the
ruleset directories named in `codeguard-package.yaml`, so nothing here runs. The gates
the drafts' bindings name are in `python/gates/`, where `codeguard test` tests them.

Each draft keeps its `python/` layout and its binding's `skill:` path, so adding a rule
back is `git mv` of its files into `python/`, in a commit whose CI passes. A judge rule
moves its skill, binding and eval, once:

- every `invalid` and `valid` eval case passes 20 of 20 runs (`codeguard eval --repeat 20`)
  on its binding's model, checked before the commit; CI then repeats 3 runs;
- a judged review of codeguard with the rule loaded reports no false positive, and every
  real violation it finds is fixed in codeguard.

A pattern rule moves its rule, binding, test and snapshot, once
`codeguard review --all --dry-run` over codeguard flags nothing it shouldn't.

Rules are added back highest value first: rules about architecture and design before
rules about style.

The drafts' judge rules each state one architectural intent with a yes/no test; the
code shapes that intent allows or forbids are its forms, listed on both sides. They were
regrouped from about 75 narrow drafts, each policing one code shape, and are refined one
at a time as they're added back.

Judge rules on every `.py` file except test files (Claude reads each changed file
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

## Import-graph tier candidates

These claims were removed from the judge drafts: they're about the import graph, which an
import linter checks across the whole project better than a per-file judge.

- Code outside a package imports the package's names from the package root, never from a
  module inside it, unless importing from the root would form an import cycle.
- Code inside a package imports names from the module that holds them, never through the
  root of a package that contains the file.
- A package's `__init__.py` exports only names defined inside the package's directory,
  never a name it imports from outside the package.
