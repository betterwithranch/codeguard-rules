---
name: parameterized-helper
description: Two or more private helper functions or methods in one class or module whose bodies are the same except for one literal or enum member are a violation.
---

# One parameterized helper, not one helper per variant

Helper code that varies by one value takes that value, instead of repeating itself once
per value.

A private helper is a function or method whose name starts with a single underscore
(`_missing`, `_add_issue`), or a function nested in another. Helpers are siblings when
they are defined in the same class body or at the top level of the same module. A
variant value is a string, number or other literal, or an enum member
(`IssueType.MISSING`).

## The test

For each private helper in the file, ask: is there a sibling private helper whose body
is the same, statement for statement, except that one literal or enum member is
replaced by another value wherever it appears?

Yes is a violation, for helpers on any kind of class (plain, `ABC`, `Generic`,
dataclass, Django model, DRF serializer) and for module functions, whether static,
class or instance methods, sync or async, and whether the value is an argument, a
return value, a dictionary value, or part of an f-string. The helpers' names usually
echo the value (`_missing` and `_invalid` passing `IssueType.MISSING` and
`IssueType.INVALID`).

Not a violation:

- helpers whose bodies differ by more than one value: other statements, other calls, or
  a second value that also differs;
- one helper that takes the varying value as a parameter (`_add_issue(field,
  issue_type)`), however many public methods call it;
- public methods, whose names are part of what callers use (`warning()` and `error()`
  on a logger); only private helpers are tested.

## Violation

Two or more sibling private helpers in the file under review whose bodies are the same
except for one literal or enum member: `_missing(field)` appending
`ValidationIssue(field, IssueType.MISSING)` and `_invalid(field)` appending
`ValidationIssue(field, IssueType.INVALID)`.
