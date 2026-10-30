---
name: no-shared-mutable-state
description: Data belonging to one call or use is kept where only that call or use sees it; module-level state that holds one call's data, or a shared instance that stores each use's results on itself, is a violation.
---

# No Shared Mutable State

Data belonging to one call or use is kept where only that call or use sees it.

A use is one piece of work the code does: one call of a function, one request, one job,
one document checked. Data belongs to a use when it is that use's input, its working
values or its results, and nothing after the use needs it.

Shared state is state every use sees: a variable or container at module level, a
class's or a type's static field, or an object that one instance serves to every use
because it is created at module level, held in a static field, given as a default, or
returned by a cached factory. A local variable, a parameter, and an object created
inside the call are seen only by that call.

## Violation

Code the change adds or edits that keeps one use's data in shared state:

- module-level state that a function writes one call's data into and reads back, such
  as a container it clears and refills on each call, a container it adds each call's
  data to and reads in later calls as if it were theirs, or a variable it sets to the
  current request, user or item;
- a shared instance of a class whose methods, while doing the work, store that work's
  results on the instance: they append to a list it holds, add to a total, or set the
  current item on it.

Module-level state that a function both reads and adds to holds that call's data,
unless the code says the state is meant to serve every use: its name, a comment or a
docstring says it keeps what every use adds, or its keys are the function's inputs, as
a cache's are. A name that only says what the state holds doesn't say how long it is
kept. Without that, what an earlier call left in it is one call's data leaking into the
next.

Report it where the use's data is written into module-level state, or where the shared
instance is created.

## Not a violation

- State written once while the program sets up, then only read: routes, registered
  handlers, loaded configuration.
- State meant to outlive every use and serve them all: a cache keyed by its inputs, a
  connection pool, a lock, a metrics counter, an id sequence.
- Module-level state whose name, comment or docstring says it keeps what every use
  adds, for as long as the program runs.
- A shared instance whose methods store nothing on it while working: a stateless
  service, a client, a formatter, a compiled pattern, frozen settings.
- An object created inside the call, a local container, or data passed as arguments
  and returned.
- Module-level state that two functions write: a separate rule judges it.
- A class-level container that each instance changes: a separate rule judges it.

## Why

When one use's data sits where every use can see it, it leaks into the next use: a
report repeats the last run's lines, a request sees the previous user. When uses run at
the same time, as requests do in a server, they overwrite each other's data and each
gets a mix of both.

Source: shared mutable state, the root of most concurrency bugs (Brian Goetz et al.,
*Java Concurrency in Practice*, 2006).
