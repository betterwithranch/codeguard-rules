---
name: no-derived-argument
description: A call doesn't pass a value together with the input it was derived from; a call to a function, method or class the program declares that receives both an input and a value computed from it is a violation.
---

# No Derived Argument

A call doesn't pass a value together with the input it was derived from.

A value is data the callee reads. A value is derived from an input when the caller
computes it from that input:

- by a call that takes the input, such as `seats(hall, show)` passed with `show`;
- by reading one of the input's fields, such as `ticket.seat` passed with `ticket`;
- by reading one of the input's keys or indexes, such as `booking["seat"]` passed with
  `booking`;
- in a local the same function assigned earlier from one of these, such as
  `fee = price(ticket)` and then `charge(fee, ticket)`.

The derivation can be a whole argument or sit inside one, such as a field read placed in
a collection literal or an unpacked argument.

The callee is declared by the program when its definition is in the file under review
or in a file of the program it imports. Read that definition to see what it does with
each argument.

## Violation

A call the change adds or edits that passes both an input and a value derived from it
to a callee the program declares:

- a function the program declares, such as `charge(price(ticket), ticket)`;
- a method on the same object, called through the object's own reference, that takes
  both;
- a class the program declares, built with both, such as a record that stores derived
  data next to its source.

Report it on the call.

## Not a violation

- A builtin, or a method of a builtin type: the language's runtime can't be changed to
  derive the value.
- A function or class from a library outside the program.
- A method of a library object, such as a third-party client or a logger.
- An argument derived from the input that is a collaborator the callee calls methods on,
  such as a repository or client built from a connection that is also passed. A
  collaborator is an object with behaviour, not a value, so it holds no copy of the
  input's data that could disagree with it.
- A value derived from a different input than the one passed alongside it.
- A derived value passed without its input.

## Why

A derived value is a second copy of what its input already says, so passing both lets
the two disagree: a caller that passes one ticket and another ticket's seat books the
wrong seat, and nothing in the callee can tell. Every caller also repeats the
derivation, so changing how the value is computed means finding each of them. When the
callee is given what the derivation needs and derives the value itself, the value has
one source and the derivation one home.

Source: house convention, from Kent Beck's "once and only once" and the Single Source of
Truth principle, applied to a call's arguments.
