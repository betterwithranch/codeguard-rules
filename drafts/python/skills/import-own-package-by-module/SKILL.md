---
name: import-own-package-by-module
description: Code inside a package imports names from the module that holds them, never through the root of a package that contains the file.
---

# Import your own package by module

Code inside a package imports its package's names from their modules, never through
the package's root.

- A package is a directory of the project that holds an `__init__.py`, its root. The
  standard library and installed libraries are not packages for this rule.
- A file is inside a package when it sits in the package's directory or below it.
  `billing/invoices/line.py` is inside `billing/invoices` and inside `billing`.
- An import goes through a root when it imports a name from a package's
  `__init__.py`: `from billing import InvoiceTotal`, `import billing` followed by
  `billing.InvoiceTotal`, `from . import InvoiceTotal`, `from .. import Customer`.
  Importing a module or a subpackage by name (`from . import invoice_total`,
  `from billing import invoices` where `invoices/` is a package) goes through no root.

## The test

For each import in the file under review that goes through a package root, ask: is the
file under review inside that package? If yes, it is a violation. If the file is outside
the package, it is not.

Not a violation:

- `from .invoice_total import InvoiceTotal` or `from billing.invoice_total import InvoiceTotal`
  in `billing/invoice.py`: the module that holds the name;
- `from . import invoice_total`: a module imported by name;
- `from shipping import Shipment` in `billing/invoice.py`: the root of a package the
  file is outside;
- `from django.db import models`: a library.

## Violation

An import in the file under review that takes a name through the root of a package the
file is inside: its own package's root or the root of a package that contains it.
