---
name: no-redundant-comments
description: A comment or docstring states a fact from outside the code; a comment that restates or narrates the code, describes what it used to do or doesn't do, or labels a unit the name already says, and a docstring that only rewords the name or signature, narrates the body or lists the parameters, is a violation.
---

# No Redundant Comments

A comment or docstring states a fact from outside the code.

A comment is a line comment or trailing comment. Tool directives, such as lint
suppressions, type-checker pragmas and formatter switches, are not comments here.

A docstring or doc comment is the documentation attached to a module, class, function
or method.

A fact from outside the code is something a reader needs that the code can't show:

- a reason: an external system's limit or quirk, a law or contract, a measured cause,
  a bug in a library with a link, why a choice that looks wrong is right;
- for a docstring, what a caller needs that the signature doesn't carry: units or
  ranges, which errors are raised and when, side effects, behavior on edge inputs,
  thread-safety, the format of a string it takes or returns.

## Violation

A comment or docstring the change adds or edits that states no fact from outside the
code:

- a comment that restates or narrates the code: `# loop over the lines and add them
  up`, `# return the total`, a heading comment over each step of a function;
- a comment or docstring about what the code used to do, no longer does, or doesn't
  do;
- a comment that labels a unit or source the name already says;
- a docstring that rewords the name or signature, narrates the body, or lists the
  parameters by name with nothing more.

Report it on the comment or on the docstring's first line.

## Not a violation

- A comment or docstring with at least one fact from outside the code, even when it
  also restates the code.
- A command-line command's docstring that is its help text.
- License headers, shebangs, encoding lines and tool directives.

## Why

A comment restating code goes stale with it: when the code changes, the comment is
left saying the old thing, and readers can't tell which to trust. A comment giving an
outside reason is the only kind the code can't replace, and the one a reader can't
recover once its author is gone.

Source: Robert C. Martin, *Clean Code* (2008), chapter 4, "Comments".
