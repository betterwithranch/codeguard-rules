---
name: state-narrowest-scope-one-writer
description: Mutable state has the narrowest scope its use needs and one writer; state shared wider than its use (module-level, class-level, a default argument, a cached factory) or written by more than one actor is a violation.
---

# State has the narrowest scope its use needs, and one writer

State a program changes lives in the narrowest scope its use needs, and one actor
writes it, so a reader of that state has one place to look.

State is a value code changes after the program has started: a container it adds to,
removes from or assigns into, an object whose methods store results on itself, a name it
rebinds. Its scope is where it lives: local to one call, on one instance, or shared by
every caller (at module level, as a class attribute, as a parameter default, or as the
result of a cached function such as `@cache` or `@lru_cache`). Its use is the work that
reads and writes it: one call, one instance's lifetime, or every call for the life of
the process. A writer is a function or method that writes it; code run once at import
or start-up to fill it is setup, not a writer.

The class of a shared instance, and the functions that write shared state, are in the
file under review or a module it imports; read them there.

## The test

For each piece of mutable state the file shares at module or class level, as a
parameter default or through a cached function, ask: is it shared wider than its use
needs, or written by more than one actor, in a way a form below names as a violation?

### Shared instances of stateful classes

A class is stateful when a method called while doing the work, not while setting the
object up, writes that work's results to the instance: it appends to or adds to an
attribute (`self.issues.append(...)`, `self.rows.extend(...)`), reassigns one
(`self.total += amount`, `self.current = order`), or calls a method that does. An
instance is shared when one instance serves every use: it is assigned at module level,
as a class attribute (including a dataclass or pydantic field default), as a parameter
default, or returned by a cached function.

For each shared instance in the file, find its class and ask: does a method called while
doing the work write that work's results to the instance?

Violation: yes, whatever builds the instance: the class itself
(`validator = OrderValidator(region="eu")`) or a factory function that returns one
(`validator = create_order_validator()`). The violation is where the instance is
created.

Not a violation:

- a shared instance whose methods write nothing to the instance during the work: a
  stateless calculator or formatter, a frozen dataclass or pydantic settings object, a
  compiled regex, a logger, an HTTP client;
- state written once while setting the object up, at import or start-up, and only read
  afterwards: routes added to a FastAPI `APIRouter` or Flask `Blueprint`, handlers added
  to a registry by decorators, a Celery app's configuration;
- state that exists to be shared across uses rather than to hold one use's results: a
  cache keyed by its inputs, a connection pool, a lock, a metrics counter;
- an instance created inside a function, per call, which is not shared.

### Module-level and class-level mutable state

Module-level state is a name assigned at the top of a module that a function changes: a
`dict`, `list`, `set`, `defaultdict`, `Counter` or `deque` it assigns into or calls a
mutating method on (`_errors.append(...)`, `_sessions[key] = ...`), or a name it rebinds
through `global`. Class-level state is a container assigned in a class body
(`items = []`) that a method changes through `self` or `cls`, so every instance shares
the one container.

Violation: module-level or class-level state written after import, when:

- its use is one call: each call that uses it clears, rebinds or fills it and reads it
  back before returning, so nothing it holds is needed after the call;
- its use is one instance: a class-level container a method changes through `self`
  (`self.items.append(item)` on `items = []` in the class body), or a module-level
  mapping keyed by an instance or its id, holding what belongs to each instance;
- two or more functions or methods write it, besides setup at import: `_sessions`
  filled by `open_session` and emptied by `close_session`, or `global _current_user`
  rebound in both `login` and `logout`.

The violation is each statement that writes the state inside a function or method: for a
name rebound through `global`, the `global` statement; for a container, the assignment
into it or the mutating call (`_errors.append(...)`, `self.items.append(...)`). It is
never the function's `def` line or the state's declaration.

Not a violation:

- a constant: module- or class-level data no code changes after import;
- a registry filled at import time, by decorators or module-level calls, and only read
  afterwards, even when a `register` function does the filling;
- a cache or counter one function owns: only that function reads and writes it, and its
  contents are meant to outlive the call (`functools.cache`, `lru_cache`, a module dict
  memoizing by the function's inputs, an id counter only `next_id()` advances);
- state that exists to be shared by every use: a lock, a connection pool, a metrics
  counter;
- state on `self` set in `__init__`, which is per instance;
- a local container built and returned inside one function.

## Violation

Mutable state in the file under review that is shared wider than its use or written by
more than one actor: a shared instance of a class that stores each use's results on
itself, or a module-level or class-level container or global that holds one call's or
one instance's data, or that two or more functions write.
