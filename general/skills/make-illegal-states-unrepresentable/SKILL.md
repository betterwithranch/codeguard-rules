---
name: make-illegal-states-unrepresentable
description: A type's fields can't hold a combination the domain forbids; a type whose optional fields must be set for some values of its status or kind field and empty for others, or must be set together or one at a time, is a violation.
---

# Make Illegal States Unrepresentable

A type's fields can't hold a combination the domain forbids.

A forbidden combination is a set of values for two or more fields of one type that the
domain never has together: a status of delivered with no delivery time, a kind of card
with a bank account number, a failed state with no error.

The usual form is a status or kind field beside optional fields, each meant for only
some of its values: a field that must be set when the status is one value and empty
when it is another. The type then allows every optional field with every status, and
only code that checks the status keeps them in step. The same holds with no status
field: optional fields of which exactly one is set, or which are set together or not at
all, allow every combination the domain rules out.

## Violation

A type the change adds or edits whose fields allow a combination the domain forbids:

- a status, state or kind field, and optional fields whose presence the domain ties to
  its values;
- optional fields whose presence the domain ties to each other: exactly one of them is
  set, or all of them are set or none.

Report it on the first field of the forbidden combination that the change adds or
edits, not on the type's declaration.

## Not a violation

- Optional fields that are each optional on their own: any combination of them set and
  empty is one the domain allows.
- One type per state or kind, each with the fields that state has, joined in a union.
- An optional field that may be set or empty whatever the type's other fields hold,
  such as a note beside a status.
- A type whose shape an outside system decides: a model mapped to one database table,
  or a type mirroring an outside API's payload as it arrives.
- A boolean field that repeats what another field holds: a separate rule judges it.

## Why

When the type allows a forbidden combination, every reader has to check for it, and
the one that forgets acts on a state that can't happen: it shows a delivery date that
is empty, or charges a card that isn't there. With one type per state, the type checker
makes every reader handle each state, and the forbidden ones can't be built.

Source: make illegal states unrepresentable (Yaron Minsky, "Effective ML", 2010); parse,
don't validate (Alexis King, 2019).
