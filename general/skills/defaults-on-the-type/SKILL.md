---
name: defaults-on-the-type
description: A default for one of a type's fields is declared by the type, not supplied by code that builds it; a fallback, a parameter default or a freshly generated id or time that code building an instance supplies for one of its fields is a violation.
---

# Defaults on the Type

A default for one of a type's fields is declared by the type, not supplied by code that
builds it.

A type is a class, record or model the program declares; a library's types are not the
program's. A default is the value a field takes when the code building the instance has
none for it: a literal, a constant, an enum member, an empty collection, or a freshly
generated id or time.

A type declares a default on the field itself: in the field's declaration, or in its
constructor's parameter for that field. A type that can't hold defaults, such as an
interface, has them declared once beside it, in its module. An alternative constructor,
a function in the type's module, a factory or a mapper that supplies a default is still
code that builds the type.

These are not defaults:

- a fallback to other data, such as a customer's saved preference;
- a value a factory's injected collaborator produces, such as its clock's time or its
  id generator's next id;
- a literal, constant or enum member passed without a fallback, as this call's own
  choice of value.

## Violation

Code the change adds or edits that supplies a default for a field of a program type
while building an instance of it:

- a fallback in the argument for the field;
- a fallback assigned to the value before the call;
- a parameter default that the function passes straight to the field;
- a freshly generated id or time passed for a field the type leaves required.

Report it on the line that supplies the default: the fallback, the parameter default or
the generated value.

## Not a violation

- A type that declares its default itself, built by a caller that leaves the field
  out.
- Anything the list above says is not a default, passed for a field.
- A default for a library call's parameter, or for a parameter that configures the
  function and never reaches a field.
- Building an instance from values the code has, with no default, wherever it is
  built.

## Why

A default supplied by the code that builds a type drifts: each builder picks its own,
and the type can't say what an instance holds when nobody chose. Declared on the type,
every instance built without a value gets the same one, and changing it is one edit.
