---
name: no-repeated-switches
description: Behaviour chosen by which kind a value is is chosen in one place, unless the type checker proves every place covers every kind; a second switch over the same kinds that a new kind could slip past is a violation.
---

# No Repeated Switches

Behaviour chosen by which kind a value is, is chosen in one place, unless the type
checker proves that every place choosing it covers every kind.

A kind is one of a fixed set of variants a value can be: its class among a family of
classes, or the member of an enumeration or the tag that names its variant (a payment's
method, a shape's type). A switch is code that picks a branch, or a table entry, by which
of two or more kinds a value is.

A switch is checked complete when the type checker rejects the program if any kind
reaches no branch: its last branch hands the value to a check that only a value of no
remaining kind passes, or its table's type demands an entry for every kind. A switch with
a default branch that handles whatever kind is left, or that simply ends after its last
kind, is not checked complete.

## Violation

- A switch the change adds or edits that chooses among two or more of the same kinds as
  another switch in the file, or in a module the file imports, when either of them is not
  checked complete. Adding a kind then means finding every switch by hand, and the one
  that's missed takes its default, or a table's missing entry, with no error until that
  kind reaches it at run time. Report it on the first line of the switch the change adds
  or edits.

## Not a violation

- One switch, whatever behaviour hangs off it: the file chooses by kind once, and the
  code that needs the choice calls it or reads what it returns.
- Each kind carrying its own behaviour, such as a method every class in the family
  defines, so a new kind is written with all of it.
- Several switches over the same kinds that are all checked complete: the type checker
  finds every one when a kind is added.
- A switch that turns outside data (a tag in a payload, a column in a row) into the
  matching kind: it decides which kind to create, not what a kind does.
- A check for one kind that guards or narrows a value, or that handles one kind
  differently from all the rest.
- A switch on something other than a value's kind: a number's range, a user's command,
  an outside system's status code.

## Why

When several places each decide what every kind does, a new kind must be added to each.
The compiler or type checker can't point to the place that was missed unless the switch
is checked complete, so the new kind takes a default it was never meant to, or reaches a
table with no entry for it, far from the change that added it.

Source: Martin Fowler, Repeated Switches (*Refactoring*, 2nd ed., 2018); the open/closed
principle (Bertrand Meyer, *Object-Oriented Software Construction*, 1988; Robert C.
Martin).
