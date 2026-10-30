---
name: command-query-separation
description: A function either changes state or returns an answer, not both; a function that changes state the caller can observe and also returns an answer about that state or other data is a violation.
---

# Command Query Separation

A function either changes state or returns an answer, not both.

A command changes state a caller can observe after it returns: it assigns a field of an
object it was given or of its own instance, adds to or removes from a collection that
outlives the call, writes to a database, file, cache or queue, or sends a message. A
local variable, or an object the function builds and returns, is not observable state.

A query returns an answer: a value computed from data, such as a count, a flag, a total,
a record found, a list of matches.

## Violation

A function the change adds or edits that both runs a command and returns an answer.

Report it on the statement that returns the answer.

## Not a violation

- A command that returns nothing, or only whether it succeeded or an error.
- A command that creates something and returns the new thing or its identity: an id, a
  created record, a handle.
- A command that returns its own object so calls can be chained, as a builder does.
- An operation whose purpose is to take and return a value in one step, so the caller
  cannot ask and then change without a race: removing and returning the next item of a
  queue or stack, getting a value and setting it if missing, incrementing and returning
  a counter, acquiring a lock or claiming a job.
- A query that caches or memoizes its own answer, or writes a log line or a metric
  about it. Any other change it makes, such as a field of a record it reads, is a
  command.

## Why

A caller can't ask a question that also changes something without changing it, so
reading becomes risky: calling the function twice gives different answers, a debugger
or a log statement that evaluates it changes the program, and a test that checks the
answer must also check what changed. Separating the command from the query lets each
be called, read and tested on its own.

Source: Bertrand Meyer, *Object-Oriented Software Construction* (1988), command-query
separation.
