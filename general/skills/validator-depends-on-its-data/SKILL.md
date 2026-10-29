---
name: validator-depends-on-its-data
description: A data model's validator depends only on the model and its input; a validator that reads stored data, settings, a registry, other instances or a dependency passed in for validation is a violation.
---

# Validator Depends on Its Data

A data model's validator depends only on the model and its input.

A data model is a type that holds data and checks it as it is built: a schema or
settings model, a record with validation, a database model's own validation. A
validator is the code that type runs to accept or reject a value as it is built: a
field or model validator, a refinement, a post-construction check.

What a validator may use is the value being built, the model's other values, and
constants. What it may not use is the running system: a database or other stored data,
an outside service, settings or environment, a registry the program fills, other
instances, or a dependency handed to it for this validation, such as a validation
context.

## Violation

A validator the change adds or edits, on a data model, that decides whether a value is
valid using anything from the running system.

Report it on the line that reads the running system.

## Not a violation

- A validator that checks the value against the model's other values or constants: a
  positive amount, an end after a start, a currency in a set the module declares.
- Validation outside a data model that needs the running system: a form's or
  serializer's validation, a service, a request handler, a database constraint.
- A database model's validation that checks the record is unique by querying for
  others like it.

## Why

A type's guarantee holds wherever an instance exists. When its validator reads the
running system, the same input parses in one place and fails in another, an instance
built yesterday may fail today, and every test that builds one needs that system set
up. Checks that need the running system belong where the data is used, which can say
what it needs.

Source: pydantic's documentation of validation `context`, which this rule flags on
purpose: a model's validity should depend only on its data, so it parses the same
anywhere and its tests need no setup.
