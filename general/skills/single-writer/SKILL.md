---
name: single-writer
description: Module-level state has one writer; module-level state that two or more functions write after start-up, or that code in another module writes, is a violation.
---

# Single Writer

Module-level state has one writer.

Module-level state is a variable or container declared at the top level of a module, or
an object exported from one, that code changes after the program has started: a name it
rebinds, a container it adds to, removes from or assigns into, a field of an exported
object it sets.

A writer is one function, or the methods of one class that holds the state. Code that
runs once while the module loads to fill the state, such as registration decorators or
top-level calls, is setup, not a writer.

## Violation

Code the change adds or edits that writes module-level state when another writer also
writes it:

- two or more functions in the module write the same state, such as one that reloads a
  table and another that overrides one entry, or one that sets a flag and another that
  sets it from somewhere else;
- a function in another module writes state the module declares or exports: it sets a
  field of an exported settings object, or adds to or clears another module's container.

Report it on each write after the first writer's: the assignment into a container, the
mutating call, the field it sets, or, for a name a function rebinds, the statement that
declares the name global or nonlocal in that function.

## Not a violation

- State only one function writes, such as a cache or memo only its function fills, or a
  counter only one function advances, however many functions read it.
- State filled while the module loads and only read afterwards, such as a registry.
- State held on an object whose own methods are the only code that writes it, such as a
  lock, a connection pool, a metrics counter or a store class.
- A constant, and a local variable or container inside one function.
- Module-level state that holds one call's data: a separate rule judges it.

## Why

With two writers, neither owns the value: each write can undo the other, as a reload
wipes out an override or a second setter leaves the flag in a state the first never
meant, and a reader can't tell which one set what it sees. With one writer, every
change to the value goes through one place, which can keep it consistent.

Source: avoid global mutable state; the single writer principle (Martin Thompson,
"Single Writer Principle", 2011).
