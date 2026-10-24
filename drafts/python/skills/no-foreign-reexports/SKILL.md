---
name: no-foreign-reexports
description: A package's __init__.py exports only names defined inside the package's directory, never a name it imports from outside the package.
---

# A package exports only its own names

A package's root exports only what the package itself defines.

- The package is the directory holding the `__init__.py` under review. A module is
  inside it when it sits in that directory or below it, including a subpackage
  (`billing/invoices/line.py` is inside `billing`). Every other module is outside: another
  project package, a sibling (`from ..shipping import Shipment`), the standard library
  or an installed library.
- A name is exported when the `__init__.py` lists it in `__all__`; imports it as
  `from x import Name as Name`; or, in an `__init__.py` without `__all__`, imports it and
  no code in the `__init__.py` uses it.

## The test

For each name the `__init__.py` under review imports, ask: does it come from a module
outside the package, and is it exported? If both, it is a violation.

Not a violation:

- `from .invoice import Invoice` or `from billing.invoice import Invoice` in
  `billing/__init__.py`, exported: the package's own module;
- `from billing.invoices import Invoice` in `billing/__init__.py`, where
  `billing/invoices/` is a subpackage: inside the package;
- a name imported from outside and used only by code in the `__init__.py`, not listed
  in `__all__` when there is one.

## Violation

An `__init__.py` that exports a name imported from a module outside its package: an
import of it from another package, a sibling or a library, or its entry in `__all__`.
