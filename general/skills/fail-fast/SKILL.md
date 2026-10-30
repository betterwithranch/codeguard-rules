---
name: fail-fast
description: A failure, missing data or an impossible state is reported where it's found, never turned into a normal-looking result; code that catches an error it doesn't handle and carries on, puts a default in place of data that should exist, clamps a value the program's rules say can't leave its range, or silently drops items it can't use is a violation.
---

# Fail Fast

A failure, missing data or an impossible state is reported where it's found, never
turned into a normal-looking result.

A failure is an error an operation reports: a raised or thrown exception, a rejected
promise, an error value. Missing data is data that should exist and doesn't: a field the
type declares required, a setting the program can't work without (a secret, a service
address), a key the program itself stored, a record the program created. A state is
impossible when the program's own rules say a value can never reach it: a stock count
below zero, a payment larger than the amount owed.

Code reports a problem when it raises, throws or returns an error, or, at the program's
top level, turns it into an error response, a message to the user or an exit code and
stops that unit of work. Code handles a failure when it does something that answers it:
retries, raises an error in the program's own terms, or takes another path that still
does the job. A normal-looking result is anything else that lets the work carry on: a
default value, an empty collection, a zero, a clamped number, a partial list.

Data is optional when the program has a real value for its absence: a query parameter, a
user preference, a page size, a display name.

## Violation

Code the change adds or edits that turns a failure, missing data or an impossible state
into a normal-looking result:

- a handler that catches a failure it doesn't handle and carries on: it does nothing,
  skips to the next item, returns a default, or only logs and continues as if the work
  were done;
- a fallback that puts a default in place of data that should exist;
- a clamp that forces a value back into a range the program's rules say it can never
  leave;
- building a collection of one result per input that leaves out the inputs whose
  parse, lookup or call failed or whose required data is missing, and passes on the
  rest as the whole result. The leaving out turns the failure into a shorter, normal-
  looking collection, even when the function it calls signalled the failure with an
  empty value.

Report it on the handler, the fallback, the clamp or the skipping condition.

## Not a violation

- Handling a failure: a retry, an error raised in the program's own terms, another path
  that still does the job.
- Cleaning up and raising the same failure again.
- A top-level boundary that reports the failure and stops that one unit of work: a
  command's exit code, a request's error response, a worker's loop logging one failed
  job and moving to the next independent one.
- Catching a specific failure whose case is expected and harmless where it happens:
  deleting a file that may already be gone, reading optional data that may be absent.
- A default for optional data that is a real value for it.
- A lookup with no default, which fails when the data is missing.
- A clamp on outside input, which may hold anything, or one that states a business rule
  where both sides are valid states, such as a discount capped at the price.
- A filter that selects the items a rule asks for, such as the unpaid invoices, rather
  than hiding the items it couldn't use.

## Why

A problem turned into a normal-looking result travels on as a wrong value. It shows up
later, far from its cause, as a wrong total, an empty report or a charge to the wrong
account, if anyone notices at all. Reported where it's found, it names its cause and
stops the work it would have spoiled.

Source: Jim Shore, "Fail Fast", *IEEE Software* (2004); Tim Peters, *The Zen of Python*
(PEP 20): "Errors should never pass silently."
