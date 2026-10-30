---
name: domain-logic-separate-from-io
description: A domain decision is made in code that does no I/O; a function that makes a domain decision and, in the same body, reads or changes state outside the program is a violation.
---

# Domain Logic Separate from I/O

A domain decision is made in code that does no I/O.

A domain decision is code that applies the program's own rules to data: a condition,
calculation or choice whose answer the domain sets, such as whether a loan can be
renewed, what a late fee comes to, or which plan an account qualifies for.

I/O is reading or changing state outside the program's memory: a database, a file, a
network service, a message queue, email, the environment, the clock or a random source.
Code does I/O when it does so itself or calls a function of the program that does.

The core is code that decides from the values it is given. The shell is code that does
the I/O: it reads, passes what it read to the core, and writes or sends what the core
answers.

## Violation

A function the change adds or edits that makes a domain decision and, in the same body,
does I/O. This includes:

- a decision on data the same function reads from a database, file or service;
- a decision whose result the same function writes, stores or sends;
- a decision that reads the clock or a random source itself, instead of receiving the
  time or the value.

Report it on the decision: the condition or calculation a fix would move into code that
does no I/O.

## Not a violation

- A shell function: it does I/O and gets each decision by calling a function that does
  none, passing it what was read and acting on its answer, including choosing which
  write to do from that answer.
- Handling an I/O operation's own outcome: a record that isn't found, a status code, a
  timeout, a retry, an error the outside system returned.
- Checking input's shape where it is read: a required field, a type, a format.
- Writing a log line or a metric.
- A decision on values the function receives or on objects already in memory.

## Why

A decision tangled with I/O can only be tested by faking the I/O around it, and it has
to change whenever the database, service or schema does. A decision made from values it
is given is tested with plain values and changes only when the rules do.

Source: Alistair Cockburn, "Hexagonal Architecture" (2005); Gary Bernhardt, "Boundaries"
(2012), which calls the two sides the functional core and the imperative shell.
