---
name: no-mutual-package-imports
description: Two sibling packages never import from each other; a module that imports from a sibling package is a violation when any module of that sibling imports from the importing module's package.
---

# No mutual imports between sibling packages

Imports between two sibling packages go one way only.

- A package is a directory of the project that holds an `__init__.py`. The standard
  library and installed libraries are not packages for this rule.
- For an import from the file under review of a project module, the two sibling
  packages are the first directories that differ under the directory the two share:
  `shop/billing/invoices/line.py` importing `shop.shipping.labels.slip` makes
  `shop/billing` and `shop/shipping` the siblings. Top-level packages are siblings of
  each other. A module that sits in the shared directory itself (`shop/money.py`), or in a
  package that contains the importing file, has no sibling package.
- A package imports from another when any module in its directory, or below it,
  imports any module in the other's directory or below it, through any import form
  (`from billing import X`, `from billing.invoice import X`, `import billing.invoice`,
  `from ..billing import X`).

## The test

For each import in the file under review of a module in a sibling package, ask: does
any module of that sibling package import from the package that holds the file under
review? Search the sibling's files for imports of the file's package (Grep). If yes, it
is a violation. If no module of the sibling imports it back, it is not.

Not a violation:

- `billing` imports from `shipping`, and nothing in `shipping` imports from `billing`;
- `billing` and `shipping` both import from `catalog`;
- `billing/invoice.py` imports `billing.invoices.line`, and `billing/invoices/` imports
  `billing.customer`: one package contains the other, so they are not siblings;
- an import of a library module.

## Violation

An import in the file under review from a sibling package that, in some module of its
own, imports from the package holding the file under review.
