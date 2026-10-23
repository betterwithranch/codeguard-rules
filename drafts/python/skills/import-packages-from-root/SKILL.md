---
name: import-packages-from-root
description: Code outside a package imports the package's names from the package root, never from a module inside it, unless importing from the root would form an import cycle.
---

# Import other packages from their root

Code outside a package reaches the package only through its root.

- A package is a directory of the project that holds an `__init__.py`, its root. The
  standard library and installed libraries are not packages for this rule; the
  project's files show which directories are its own (Glob them).
- A module's package is the nearest directory above the module file that holds an
  `__init__.py`. A subpackage is a package of its own: `billing/invoices/` with an
  `__init__.py` is the package of `billing/invoices/line.py`.
- A file is inside a package when it sits in the package's directory or below it, and
  outside it otherwise. `shop/cli.py` is inside `shop` and outside `shop/billing`.
- Importing from the root forms a cycle when the package's `__init__.py` imports,
  directly or through the modules it imports, the file under review.

## The test

For each import in the file under review that names a project module that is not a
package root, ask:

1. Is the file under review outside that module's package?
2. Would importing from that package's root instead form a cycle?

Outside and no cycle: a violation. Inside, or a cycle: not a violation.

A module is named whatever the import's form: `from billing.invoice_total import InvoiceTotal`,
`import billing.invoice_total`, `from billing import invoice_total` (a module imported
as a name), `from ..billing.invoice_total import InvoiceTotal`,
`from .labels.slip import Slip` when `labels/` is a package.

The answer doesn't depend on what the root exports today: a name the root doesn't
export yet, imported from its module from outside the package, is a violation too.

Not a violation:

- `from billing import InvoiceTotal`: the package root;
- `from billing.invoices import Invoice` where `billing/invoices/` is a package: that
  package's root;
- `from billing.invoice_total import InvoiceTotal` or `from .invoice_total import InvoiceTotal`
  in `billing/invoice.py`: inside the package;
- `from django.db.models import Q`, `import os.path`, `from pydantic.fields import Field`:
  library modules;
- a module import where the root import would form a cycle.

## Violation

An import in the file under review, outside a project package, of one of that
package's modules (not its root), where importing from the root would form no cycle.
