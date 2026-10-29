---
name: construction-in-its-home
description: What a new instance holds is decided by its type, its module, its factory or its source's mapper; code elsewhere that decides a program type's field values from a source, or supplies a default for one of its fields, is a violation.
---

# Construction in Its Home

What a new instance holds is decided by its type, its module, its factory or its
source's mapper.

A program type is a class, record or model the program declares; a library's types are
not the program's. Building an instance of one is deciding its field values from a
source: reading them off another object of the program, translating outside data (a
payload, a file, a row) into them, or picking them.

These are not building:

- calling the type's own alternative constructor, a factory or a mapper;
- passing the function's own parameters through to the fields unchanged;
- raising an exception;
- returning a result the function built from values it computed itself, as the answer
  to what it was asked;
- copying an existing instance with some fields changed.

A type's homes, where building it is decided:

- the type itself: its constructor or an alternative constructor on it;
- the type's module: a function beside the type;
- a factory: a class whose only job is building the type, because building needs
  collaborators the type can't hold (a clock, an id generator, a lookup), injected into
  the factory and used to decide the field values;
- a mapper: a module or class whose only job is translating one source into the
  program's types.

A default is the value a field takes when the caller has none: a literal, a constant,
an enum member, an empty collection, or a freshly generated id or time. A fallback to
other data, such as a customer's saved preference, is not a default, nor is a value a
factory's injected collaborator produces. A field's default is declared by the type.

## Violation

Code the change adds or edits that:

- builds an instance of a program type, deciding its field values from a source, in a
  place that is not one of the type's homes: a service, a handler, a view, another
  domain type, or a module of other jobs, among its other work;
- supplies a default for a field of a program type from outside the type: as a
  fallback in the argument, a fallback assigned before the call, a parameter default
  passed straight to the field, or a freshly generated value passed for a field the
  type leaves required. This holds in the type's homes too: a default belongs on the
  type.

Report it at the construction, or at the argument that supplies the default.

## Not a violation

- Anything the list above says is not building.
- Building in one of the type's homes.
- A type that declares its default itself, built by a caller that leaves the field
  out.
- A value from other data or from a factory's collaborator, passed for a field.
- A literal passed without a fallback, as this call's own choice.
- A default for a library call's parameter, or for a parameter that configures the
  function and never reaches a field.

## Why

How a type is built changes with the type. Built in one home, a new field or a changed
rule is one edit; built inline wherever it's needed, each place needs the change, and
the ones missed build instances the type no longer means. A default supplied by callers
drifts the same way: each caller picks its own.

Source: Creator (Craig Larman, *Applying UML and Patterns*, 1997); factories (Gamma et
al., *Design Patterns*, 1994).
