---
name: package-cohesion
description: Package cohesion
---

# Package cohesion

Modules that form one pipeline or feature belong in one package. A reader should be able to guess a concept's package from its responsibility. Flag:

- One flow split across sibling packages that import sideways into each other.
- A package that only re-exports another package's symbols.
- A module (such as a registry or builder) that sits outside the package owning its concept.
- A package of unrelated single-purpose modules.
