---
name: package-public-interface
description: Package public interface
---

# Package public interface

- Code outside a package imports from the package root: `from billing import InvoiceTotal`, not `from billing.invoice_total import InvoiceTotal`.
- Code inside a package imports its siblings by direct submodule path (`from .invoice_total import InvoiceTotal`), never through its own package root.
- When importing through another package's root would create a cycle, import the specific leaf module instead.
- Keep `__init__.py` free of eager heavy imports.
