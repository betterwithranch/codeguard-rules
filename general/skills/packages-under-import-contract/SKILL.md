---
name: packages-under-import-contract
description: A package the change adds is under the project's import-boundary configuration; a module the change adds in a package the configuration leaves out, while it lists that package's siblings, is a violation.
---

# Packages Under Import Contract

A package the change adds is under the project's import-boundary configuration, which
keeps its siblings from importing each other.

The import-boundary configuration is the project's configuration of a tool that checks
imports between packages: an independence, layers or forbidden contract, or a rule that
names packages or folders and the imports allowed between them. A package is under it
when the configuration names the package, a pattern that matches it, or a parent
package whose children the contract covers by wildcard.

A module the change adds is a file with no earlier version: every line of it is new.
A file with any line the change left as it was existed before the change, and so did
its package.

A package is the directory a module is in. Two sibling packages are directories under
the same parent directory.

Read the configuration where the project keeps it. When the project has none, or the
configuration names none of the package's siblings, this rule has nothing to check.

## Violation

A module the change adds, in a package the import-boundary configuration doesn't put
under any contract, when the configuration names one or more of that package's sibling
packages.

Report it on the module's first import.

## Not a violation

- A module in a package the configuration names, matches by pattern or covers by
  wildcard.
- A module in a package none of whose siblings the configuration names.
- A project with no import-boundary configuration.
- A change to a module that already existed, even one that adds imports or sits in a
  package the configuration leaves out. Its package was there before the change.
- A test module, migration or script outside the packages the configuration covers.

## Why

Two packages that import each other are one unit: neither can change, be tested or be
read without the other. The boundary tool enforces that siblings don't, but only for
the packages its configuration names, so a new package left out of it can be imported
from anywhere and import anything. Checking the configuration when a package is added
keeps the contract covering the whole set.

Source: import-linter's independence and layers contracts; Robert C. Martin, the
Acyclic Dependencies Principle.
