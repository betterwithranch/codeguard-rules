---
name: one-home-for-defaults
description: Code outside a type does not supply the default value for one of that type's fields; the type declares its own defaults.
---

# One home for defaults

A field's default value is declared once, by the type that owns the field.

A default is the value a field takes when the caller has none: a literal or constant
(`"EUR"`, `DEFAULT_CARRIER`), an enum member, an empty collection, or a freshly
generated value (`uuid4()`, `datetime.now(UTC)`, `secrets.token_hex(8)`). It does not
depend on the call's other inputs. A fallback to other data is not a default: a
customer's preferred carrier, a value read from the order, a setting passed in.

The owning type is a class the program declares: a dataclass, pydantic model, attrs
class, `NamedTuple`, Django or SQLAlchemy model, or plain class whose `__init__` sets the
field. It is declared in the file under review or in a file of the program that file
imports; read that file to see which fields declare defaults.

## The test

For each value passed to a field of a class the program declares — a constructor
argument, a `model_validate` or `objects.create` key, an attribute set on a new
instance — ask: is it a default supplied by code outside that class?

Forms that supply a default, so the answer is yes:

- a fallback in the argument: `invoice_id=invoice_id or str(uuid4())`,
  `carrier=carrier if carrier is not None else "DHL"`, `currency=data.get("currency",
  "EUR")`;
- a fallback assigned before the call: `if carrier is None: carrier = "DHL"`, then
  `Shipment(carrier=carrier)`;
- a parameter default passed straight to the field: `def book(order_id, carrier="DHL")`
  then `Shipment(order_id=order_id, carrier=carrier)`;
- a freshly generated value passed for a field the class leaves required:
  `Invoice(invoice_id=str(uuid4()), total=total)` where `Invoice.invoice_id` has no
  default, `created_at=datetime.now(UTC)`.

The answer is no when:

- the class declares the default itself: a field default, `field(default_factory=...)`,
  pydantic `Field(default=...)` or `default_factory`, attrs `attrs.field(default=...)`,
  a Django `models.CharField(default=...)`, a SQLAlchemy `mapped_column(default=...)`,
  `__post_init__`, a validator, or a `@classmethod` constructor on the class;
- the value comes from other data, not a default (`carrier=customer.preferred_carrier`,
  `currency=order.currency`);
- a literal passed without a fallback, as this call's choice
  (`Notification(channel="email", ...)` in an email sender);
- the field belongs to a class the program doesn't declare: a library call's keyword
  (`requests.get(url, timeout=10)`, `httpx.Client(base_url=...)`);
- the parameter default configures the function itself and never reaches a field
  (`def fetch(page_size=50)` used only to slice).

## Violation

Code outside a class the program declares that supplies a default for one of that
class's fields, in any of the forms above.
