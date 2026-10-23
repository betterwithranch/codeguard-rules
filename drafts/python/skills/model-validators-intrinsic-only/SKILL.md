---
name: model-validators-intrinsic-only
description: A validator on a data model checks only the model's own values; a validator that reads a registry, stored data, a service, settings or other instances is a violation.
---

# Model validators check intrinsic invariants only

A model's validation states facts about the model's own values, never facts that
depend on the rest of the running system.

A validator is code a data model runs on its own values when it is built or changed:
pydantic `@field_validator`, `@model_validator`, `@validator` and `@root_validator`,
`model_post_init`, a dataclass `__post_init__`, an attrs `@field.validator`,
`validator=` argument or `__attrs_post_init__`, msgspec `__post_init__`, and a Django
model's `clean()` or `clean_<field>()`.

An intrinsic invariant is one the model's own field values decide: a required field
combination, a normalized field (`value.strip().upper()`), an allowed range or format,
an ordering between two of its fields, a check using constants and pure functions
(a regex, `datetime.fromisoformat`, a currency code table that is a module constant).

## The test

For each validator in the file, ask: can it decide using only the model's own values
and constants? Follow a name it reads to where it is defined.

A violation when the validator reads, calls or queries anything that is runtime state
outside the model:

- a registry, catalog or lookup service (`warehouse_registry.get(...)`);
- stored data: an ORM query (`Order.objects.filter(...)`, `session.execute(...)`), a
  cache, a file;
- a client, repository or other dependency, including one passed in through pydantic's
  validation `context` (`info.context["catalog"]`);
- settings or environment (`settings.MAX_REFUND`, `os.environ`);
- peer collections: other instances of the model or a list of them
  (`all_shipments`, a uniqueness check across rows).

Not a violation:

- a validator that only reads the model's own fields and constants;
- validation in a DRF serializer's `validate()` or `validate_<field>()`, a form's
  `clean()`, or a service: these are not data models;
- a Django model field's `unique=True` or a database constraint, which the database
  enforces.

## Violation

A validator on a data model that depends on state outside the model: a
`@model_validator` that looks up `self.warehouse_code` in a warehouse registry, a
`@field_validator` that checks a SKU against a product catalog, a `__post_init__` that
reads settings, a Django model `clean()` that queries other rows.
