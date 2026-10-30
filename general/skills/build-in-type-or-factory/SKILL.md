---
name: build-in-type-or-factory
description: What a new instance holds is decided by its type, its module, its factory or its source's mapper; code elsewhere that builds an instance of a program type, deciding its field values from another object or from outside data, is a violation.
---

# Build in the Type or Its Factory

What a new instance holds is decided by its type, its module, its factory or its
source's mapper.

A program type is a class, record or model the program declares; a library's types are
not the program's. Building an instance of one is deciding its field values from a
source: reading them off another object of the program, translating outside data (a
payload, a file, a row) into them, or working them out from those values.

These are not building:

- calling the type's own alternative constructor, a factory or a mapper;
- passing the function's own parameters through to the fields unchanged;
- filling a field with a value that comes from no source: a literal, a constant, an enum
  member, an empty collection, or a freshly generated id or time;
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

## Violation

Code the change adds or edits that builds an instance of a program type, deciding its
field values from a source, in a place that is not one of the type's homes: a service, a
handler, a view, another domain type, or a module of other jobs, among its other work.

Report it at the construction.

## Not a violation

- Anything the list above says is not building.
- Building in one of the type's homes.
- Creating a database record, an instance of a class the persistence library maps to a
  table, wherever the record is written, with the library's create call or the record
  class's constructor: the library builds it, and its fields are the columns being
  stored.
- Building an instance of a library's type.

## Why

How a type is built changes with the type. Built in one home, a new field or a changed
rule is one edit; built inline wherever it's needed, each place needs the change, and
the ones missed build instances the type no longer means.

Source: factories (Gamma et al., *Design Patterns*, 1994).
