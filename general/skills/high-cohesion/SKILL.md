---
name: high-cohesion
description: A module's public classes belong to its one concept; a public class with behavior of its own beside the module's primary type, a class unrelated to it, or unrelated classes grouped by construct kind is a violation.
---

# High Cohesion

A module's public classes belong to its one concept.

A module's concept is its primary type, or one family of types, and the shapes that
belong to them. A public class belongs to the concept when it is one of these:

- the primary type: the class the module is about;
- a member of one family: classes that share a base the module defines, such as an
  exception hierarchy or the subclasses of one abstract base, or the variants of a union
  the module declares;
- a passive shape of the primary type: a class with no behavior of its own that appears
  in the primary type's fields or method signatures, and in no other public class of
  the module.

A class with behavior of its own is its own concept, even when the primary type is its
only caller or builds it. Judge by the classes the module defines, not its file name: a
module of enumerations or constants by kind is not one concept.

## Violation

A public class the change adds or edits, in a module whose public classes are not all
one concept, that falls outside the module's concept: a class with behavior beside the
primary type, a class unrelated to the primary type, or one of several unrelated
classes grouped by construct kind.

Report it on the line that declares the class outside the concept, or, when that line
is unchanged, on a changed line inside the class.

## Not a violation

- A module with one public class, or whose public classes are one concept as above.
- Private classes, which are the module's implementation.
- A module a framework expects to group classes by kind: a web framework's models,
  admin, forms, serializers or schemas module, a package's re-export file, a framework
  route file.

## Why

Knowledge grouped by kind is found by guessing which kind module holds it; grouped by
concept, it sits where its next change will look. A module holding one concept changes
for one reason, and a reader who opens it finds everything about that concept and
nothing else.

Source: Larry Constantine and Edward Yourdon, *Structured Design* (1979), cohesion;
Robert C. Martin, the Common Closure Principle; package by feature.
