---
name: pure-validators
description: A data model's validator depends only on the model and its input; a validator that reads stored data, an outside service, settings, a registry, other instances or a dependency passed in for validation is a violation.
---

# Pure Validators

A data model's validator depends only on the model and its input.

A data model is a type, or a schema that defines one, whose instances hold data the
program passes on, and which checks that data whenever an instance is built, wherever
it is built: a schema or settings model, a record with validation, a database model's
own validation. Request validation is not a data model: a form, a serializer or a
request handler checks one request's input in the code that handles that request, and
the program carries on with the values it hands over, not with the form or serializer.
A validator is the code a data model runs to accept or reject a value as an instance is
built: a field or model validator, a refinement, a post-construction check.

What a validator may use is the value being built, the model's other values, and
constants the code declares. What it may not use is the running system: a database or
other stored data, an outside service, settings or environment, a registry the program
fills as it runs, other instances of the model (such as a check that no other record
has the same value), or a dependency handed to it for this validation, such as a
validation context.

## Violation

A validator the change adds or edits, on a data model, that decides whether a value is
valid using anything from the running system.

Report it on the line that reads the running system.

## Not a violation

- A validator that checks the value against a constant: a positive amount, a maximum
  length.
- A validator that checks the value against the model's other values: an end after a
  start.
- A validator that checks the value against a set or table the code declares: a
  currency in a set the module declares.
- Request validation that needs the running system: a form's or serializer's
  validation, a service, a request handler.
- A database constraint, such as a unique column: the database enforces it where the
  data is stored, not the model's validator.

## Why

A type's guarantee holds wherever an instance exists. When its validator reads the
running system, the same input parses in one place and fails in another, an instance
built yesterday may fail today, and every test that builds one needs that system set
up. Checks that need the running system belong where the data is used, which can say
what it needs.

Source: pydantic's documentation of validation `context`, which this rule flags on
purpose: a model's validity should depend only on its data, so it parses the same
anywhere and its tests need no setup.
