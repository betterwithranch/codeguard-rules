---
name: trust-the-boundary
description: A guarantee is established once, where data enters the program or where its type is built, and trusted after; code doesn't re-check it, leave it undecided, or make it depend on the running system.
---

# Trust the boundary

A guarantee about data is established once, where the data enters the program or where
its type is built, and the rest of the program trusts it.

A guarantee is a fact code can rely on without checking: a value is present, positive,
one particular variant, in range. It is established by:

- the parse at the boundary, which turns outside data into declared values
  (`parse-boundary-data-once` covers reading the raw data);
- a type that rejects bad values when it is built: a pydantic `field_validator` or
  `Field(gt=0)`, a dataclass `__post_init__` that raises, an attrs validator, a Django
  field with `null=False`, a SQLAlchemy column with `nullable=False`;
- control flow the reader can see: an earlier check that already stopped on the failing
  value, an enclosing branch, a dispatch that routes only one variant to this code
  (`HANDLERS[request.kind].handle(request)`), a collaborator that always returns the
  guaranteed form.

The guarantee is in the file under review or a file of the program it imports; read
that file when it comes from there.

## The test

For each check, union and validator in the file, ask: is this guarantee made once,
where the data enters or its type is built, so the code after can trust it?

- **A check** (an `assert`, an `if` that raises or returns early, an `isinstance`, a
  `cast`, a `match` case that raises): does visible code already make its condition true
  every time it runs? Yes means it re-checks a guarantee. No (outside data, an optional
  field, a parameter callers pass either way, `dict.get`, a lookup that may miss) means
  it is validation, which is fine.
- **A union of classes the parser builds from data** (pydantic models, `TypedDict`s
  read by pydantic, msgspec `Struct`s): does the parse decide the variant, with a
  one-value literal tag on every variant and the tag named as the discriminator
  (`Field(discriminator="kind")`, `Discriminator(...)`, msgspec `tag=`/`tag_field=`)?
  No leaves the variant to be guessed from field shape after the boundary.
- **A validator on a data model** (pydantic validators, `model_post_init`, a dataclass
  or attrs post-init or validator, a Django model's `clean()`): does it decide using
  only the model's own values and constants? A validator that reads a registry, stored
  data, settings, a dependency passed through validation `context`, or other instances
  makes the type's guarantee depend on the running system, so it can be false later.

A condition only an annotation guarantees is the type checker's job
(`reportUnnecessaryIsInstance`, `reportUnnecessaryComparison`), not this rule's.

## Violation

- A check whose condition visible code already guarantees where it runs: an
  `isinstance` of a payload in a handler only a registry keyed by its kind calls, an
  `assert x is not None` below `if x is None: raise`, `if amount <= 0: raise` on a
  field whose validator rejects non-positive amounts.
- A parsed union whose variant the parse doesn't decide: no discriminator named, a
  variant with no tag or a plain-`str` tag, two variants with the same tag value. The
  violation is on the union and on the missing or plain tag.
- A data model's validator that depends on state outside the model: a registry lookup,
  an ORM query, settings, a validation-context dependency, other instances.

Not a violation:

- validation of what nothing guarantees yet: outside data, optional values, lookups
  that may miss;
- a union of classes the program builds itself and tells apart by class
  (`case CardPayment():`), a union with `None`, a union of plain values;
- validation that needs the running system in a DRF serializer's `validate()`, a form's
  `clean()` or a service, which are not data models; a database constraint.
