---
name: types-live-with-producer
description: A type is defined in the package whose code constructs it; a type that several packages construct is defined in a package that imports none of its sibling packages.
---

# Types live with their producer

A type is defined where it is produced, not where it is used.

A package is a directory of modules one level below the source root or the project's
top package (`billing/`, `shipping/`, `app/billing/`). Its sibling packages are the
other packages at that level.

A type's producers are the packages whose code constructs it: instantiates it
(`Invoice(...)`, `Invoice.model_validate(...)`, `Invoice.objects.create(...)`), returns
one it built, raises it, or subclasses it. Code that only imports it, annotates with it,
reads its fields or catches it is a consumer. How many packages consume a type has no
bearing on where it is defined.

## The test

For each class the file defines, ask: which packages construct it? Grep the program for
its name.

- One package constructs it: it is defined in that package.
- Several packages construct it: it is defined in a package that imports none of its
  sibling packages.
- No package constructs it yet (a new type, a base class only subclassed in its own
  package): it is defined where it is, and the rule holds.

This holds alike for dataclasses, pydantic models, attrs classes, `TypedDict`s,
exceptions, enums and plain classes. An enum's producers are the packages whose code
assigns or returns its members (`invoice.status = InvoiceStatus.PAID`).

Not a violation:

- a type defined in its one producer's package and imported by many consumers;
- a type that several packages construct, defined in a low-level package (one whose
  modules import no sibling package);
- a type constructed only in tests.

## Violation

A type defined in a package that doesn't construct it while another package does
(`Invoice`, built only in `billing/`, defined in `shipping/`), or a type several
packages construct defined in a package that imports a sibling package.
