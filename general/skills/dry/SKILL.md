---
name: dry
description: Don't Repeat Yourself. Every piece of knowledge has a single, unambiguous, authoritative representation within the system; code that states a piece of knowledge a second time, instead of using the place that already states it, is a violation.
---

# Don't Repeat Yourself

Every piece of knowledge has a single, unambiguous, authoritative representation within
the system.

A piece of knowledge is something the program decides that changes for one reason:

- the steps of a computation or a check, whatever the names of the code that holds them
  and the order of its inputs;
- the order in which a process runs its stages, each stage's output feeding the next;
- the members of a set the program supports or recognises;
- the fields the program gives one outside thing, such as one service's message, one
  file format or one API's response.

Its representation is the code that states it: a function or method, the process that
runs the stages, the collection or enumeration that lists the set, the type or schema
that models the outside thing. Code uses the knowledge when it calls, reads, or derives
from that representation.

The other representation is in the file under review or in a module of the program
that file imports. The changed code alone never shows it: the file's imports may sit
outside the change, and the modules they name aren't in it. Decide only after reading
the whole file under review and each module of the program it imports, and comparing
the changed code with what they state.

## Violation

Code the change adds or edits that states a piece of knowledge again, when the file
under review or a module of the program it imports already states it, instead of using
that representation. When the knowledge changes, both statements have to change.

This includes:

- steps that repeat another function's steps, with different names, a different input
  order, or only a different literal or constant where the other has its own;
- a function that repeats the steps of a method the type it works on already has;
- code that runs a process's stages in the process's order, outside the process;
- a collection that lists exactly the members of another set and states nothing more;
- a second type or schema with the fields of a type or schema that already models the
  same outside thing.

Repeated steps state the knowledge again wherever they sit: on their own, inside a loop,
or before, after or between steps of the code's own. Steps the code adds don't turn the
repeat into a use of the representation. Only a call to it, a read of it or a derivation
from it uses it.

Report it on the code the change adds or edits that states the knowledge again: the code
a fix would replace with a use of the existing representation.

## Not a violation

- Code that calls, reads, or derives from the representation, including code that adds
  steps of its own around that call, and a collection built from another.
- Steps that differ from the other's within the sequence they share: a different
  operation, condition, call, or input or field read in place of one of the other's
  steps. Each states its own knowledge. Steps added before, after or around a repeated
  sequence leave it repeated.
- A collection that selects some of a set's members, or maps them to values of its own.
  The selection, or each value, is knowledge of its own.
- Two types with the same fields at different boundaries, such as a stored row and an
  API's response, mapped where they meet. Each changes when its own boundary does.
- Code too small to state a decision: one statement that only returns, reads or forwards
  a value.
- Structure the language or a framework requires of every implementation, such as an
  interface's declared signatures or a framework's per-class settings.

## Why

When one piece of knowledge is stated in two places, changing it means finding and
changing both. The place that is missed keeps the old rule, and two parts of the program
disagree without any error.

Source: Andrew Hunt and David Thomas, *The Pragmatic Programmer* (1999).
