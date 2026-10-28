---
name: no-feature-envy
description: A domain answer computed from one type's data lives in that type's module; code in another module that computes an answer about a value of the program's own type from that value's fields alone is a violation.
---

# No Feature Envy

A domain answer computed from one type's data lives in that type's module.

A type is a class, record, model or interface the program defines; the standard
library's, a framework's and installed libraries' types are not the program's. A type's
module is the module that defines it.

A domain answer is a value the program's rules give about something: whether a loan is
overdue, what an order's balance is, how many seats a plan has left. An answer from one
type's data is computed from the fields of one value of that type, reading two or more
of them, and from nothing else but literals and parameters that are not the program's
types, such as a date passed in.

## Violation

Code the change adds or edits, in a module other than the type's module, that computes a
domain answer from one value of a program type's data. This includes:

- a function that takes the value and returns the answer;
- a method of another class that computes the answer from a value it holds or receives;
- an inline expression in a longer body that works the answer out from the value's
  fields before using it.

Report it on the first line of the code a fix would move into the type's module: the
function's or method's definition, or the expression.

## Not a violation

- Code in the type's module, whether a method or a function beside the type.
- A call to the type's method or to a function in its module, with steps of its own
  around the call.
- Code that combines the value's fields with data of its own module or of another value:
  a rate table or constant the module defines, a second type's fields. The answer then
  needs knowledge the type doesn't have.
- Code that reads one field of the value.
- Code that copies fields into another shape without deciding anything: building a
  response, a row, a message or a display.
- A type that is not the program's.

## Why

An answer about a value belongs with the data it reads. In the type's module, the next
change to the type's fields meets every answer that reads them; elsewhere, the field
changes and the answer is missed, or it is worked out again in a third place.

Source: Martin Fowler, *Refactoring* (1999), Feature Envy; Craig Larman, *Applying UML
and Patterns* (1997), Information Expert.
