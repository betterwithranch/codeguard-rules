---
name: comments-state-reasons
description: A comment states a reason or fact the code cannot hold, never what the code does, did, or does not do
---

# Comments state reasons

A comment says only what the code itself cannot say: why it is this way, or a fact
about something outside it.

## Definitions

- A **comment** is a `#` line or trailing `#` text. Tool directives (`# noqa`,
  `# type: ignore`, `# pragma: no cover`, `# fmt: off`, `# pyright:`) are not comments
  here; the gate skips them.
- **What the code says** is everything a reader learns from the names, types, values,
  calls and control flow in the file: that a loop adds line totals, that a function
  returns early on an empty list, that a constant is 500.
- A **reason the code cannot hold** is a fact from outside the code that explains it: an
  external system's limit or quirk (`# Stripe rejects metadata values over 500
  characters`), a law or contract, a measured cause (`# the carrier API times out
  above 50 parcels per request`), a bug in a library with a link, or why a choice that
  looks wrong is right (`# sorted first so the cache key is stable`).

## The test

For each comment the change adds or edits, ask: does it state a reason the code cannot
hold?

Yes: not a violation. No: violation.

The test reads these forms the same way:

- a comment that restates or narrates the code (`# loop over the lines and add them
  up`, `# return the total`, `# increment counter`, a heading comment over each step of
  a function): violation;
- a comment about what the code used to do or no longer does (`# this used to read the
  legacy table`, `# removed the retry`), or what it does not do (`# doesn't handle
  refunds`): violation, since none of it is in the code;
- commented-out code: violation;
- a `TODO` or `FIXME` that names a concrete outside reason or tracker link
  (`# TODO(#412): drop once the carrier ships v2`): a reason, not a violation; a bare
  `# TODO: clean up`: violation;
- a comment that labels a value's unit or source where the name already says it
  (`timeout_seconds = 30  # seconds`): violation; one that gives a fact the name can't
  (`TIMEOUT = 30  # the gateway closes idle sockets after 35s`): not a violation;
- comments in Django settings, SQLAlchemy models, pydantic models, CLI modules and
  scripts are read the same way.

## Violation

A comment added or edited in the file under review that states no reason the code
cannot hold: it restates or narrates the code, records what the code used to do or does
not do, or holds commented-out code.
