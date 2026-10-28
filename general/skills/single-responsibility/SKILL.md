---
name: single-responsibility
description: A function or class has one reason to change; a function whose own body holds the details of two concerns, or a class whose methods serve two concerns that never touch, is a violation.
---

# Single Responsibility

A function or class has one reason to change.

A concern is one source of change: a body of rules (pricing, payroll, eligibility), an
outside system's interface (a vendor's API, a printer, an accounting package), or a data
format (a file layout, a wire format, a report's markup). Code belongs to a concern when
a change in that concern would force the code to change.

A function's own body is the code written in it: its conditions, calculations, string
building and parsing. A call to another function puts only the call in the body; the
called function's details stay with it.

## Violation

- A function the change adds or edits whose own body holds the details of two or more
  concerns, so a change in either one edits it: it parses a vendor's export layout and
  applies the payroll rules to what it parsed, or it lays out a printed label's markup and
  works out the shipping charge printed on it. Report it on the first line of the body
  that belongs to the second concern.
- A class whose methods serve two or more concerns, so a change in one concern edits some
  of its methods and not the others: a class that manages members' bookings and also
  writes them in an accounting package's file format. A method that puts the class's data
  into an outside system's or file's format serves that format's concern, even when it
  reads nothing but the class's data. Report it on the method the change adds or edits
  that serves the other concern.

## Not a violation

- A function that coordinates: its body calls one function per concern and passes
  results between them. Running the sequence is its one job, however many calls it
  makes.
- One concern worked out in several steps: totalling lines and then rounding the total,
  reading every field of one format, checking input before using it.
- Receiving a request, a command's arguments or a message, calling the code that does
  the work, and shaping the reply: the transport is one concern.
- A guard that rejects bad input, a log line or a metric, as part of the job it serves.
- A class whose methods all read or change its own data in the program's own terms,
  however many topics they cover: a value object's arithmetic, comparison and display, or
  a record's fields and the answers derived from them.
- A class whose methods carry out the steps of one workflow, calling each other or
  feeding each other's results.
- A domain decision made beside the I/O that reads or writes its data: a separate rule
  judges that.

Size doesn't decide it: a long function or a large class in one concern keeps the rule,
and a short one in two breaks it.

## Why

Code that serves two concerns changes whenever either does, so every change to one risks
breaking the other, and neither can be read, tested or reused alone.

Source: Robert C. Martin, the single responsibility principle (*Agile Software
Development*, 2002); Martin Fowler, Divergent Change (*Refactoring*).
