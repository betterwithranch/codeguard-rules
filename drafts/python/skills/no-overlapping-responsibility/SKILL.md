---
name: no-overlapping-responsibility
description: Two differently named types never both own the same job on the same domain concept, such as a factory and a service that both create invoices, or two views that compute the same projection.
---

# No overlapping responsibility

Each job on a domain concept has one owner type.

A job is what a type's public methods do to a domain concept: create it, price it,
validate it, send it, compute a projection of it (a summary, a report row, a
dashboard figure). Two types own the same job when each has a public method that does
that job to the same concept, whatever their names, method names or bodies: an
`InvoiceFactory.create_invoice` and an `InvoiceService.create_invoice`, an
`OrderTotals.compute` and an `OrderSummary.total`, two DRF views or Django admin
classes that each build the same revenue figure.

## The test

For each type the change adds, and each public method the change adds to a type, ask:
does another type, in this file or in the program (Grep for the domain noun and the
verb), already do this job to this concept? Bodies need not match: two methods that
build the same `Invoice` from the same order own the same job even if one also clamps
the total.

Not a violation:

- one type delegating to the owner (`InvoiceService.issue` calls
  `InvoiceFactory.create_invoice` and then sends it);
- two types doing different jobs on one concept (one creates invoices, one sends them);
- the same job on different concepts (creating invoices and creating refunds);
- two passive shapes with the same fields at different boundaries, mapped explicitly
  where they meet (an `InvoiceRow` from the database and an `InvoicePayload` for an
  API): each changes when its own boundary does;
- a subclass that overrides its base's method: one job, specialized.

## Violation

A second type that owns a job another type already owns on the same concept: both
`InvoiceFactory` and `InvoiceService` with a `create_invoice` that builds an `Invoice`
from an order; two report classes that each compute monthly revenue from the same
orders; two passive shapes with the same fields at the same boundary (two models of
one API's response) that change for the same reason.
