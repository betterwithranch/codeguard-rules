---
name: construction-has-one-home
description: Code that decides a new instance's field values lives in one home that changes with the built type (on the type, in its module, in a factory whose building needs injected collaborators, or in a mapper for one source), and a field's default is declared by the type; construction or defaults decided anywhere else is a violation.
---

# Construction has one home

Building an instance of one of the program's types, deciding its field values and its
defaults, happens in one home that changes with that type, in the form that fits what
building it needs.

The built type is a class the program declares: a plain class, a dataclass, a pydantic
model, an attrs class, a `NamedTuple`, a Django or SQLAlchemy model. It is declared in
the file under review or in a file of the program that file imports; read the built
type's module when it is imported, to see whether the code under review is that module,
and what the type provides (alternative constructors, field defaults).

Building it is deciding its field values: computing them from a source, reading them
off another object, or picking them. `Shipment(order_id=order.id,
address=order.address)` builds a `Shipment` from an `Order`. Passing values straight
through to code that builds is not building: calling an alternative constructor
(`Shipment.from_order(order)`, `Quote.model_validate(raw)`), or calling the class with
the function's own parameters unchanged (`Handler(name)`).

The source is what the field values come from: another program type (`Order`), or
outside data: a payload, file contents, a command's output, a raw row (data whose shape
something outside the program decides).

## The test

For each construction of a program type, and each value passed to one of its fields,
ask: is this decided in the type's home, in the form the form below names?

### Construction outside the type's home

The places where a type `C` may be built:

- on `C`: a `@classmethod` alternative constructor (`from_order`, `from_row`,
  `from_acme`), `__init__`, `__post_init__`, or another method of `C`;
- in `C`'s module: a function beside the class (`def default_settings() -> Settings`
  defined below `Settings`);
- in a factory: a class whose job is building `C` and nothing else, because building
  needs collaborators the type can't hold: a clock, an id generator, a repository, a
  rate lookup, injected through the factory's constructor and used to decide the field
  values (`InvoiceFactory(clock, numbers).create(order)`);
- in a mapper: a module or class whose job is translating one source into the
  program's types, and nothing else. `carriers/acme.py` turning Acme's API payloads
  into `TrackingEvent`s, `class OrderRowMapper` turning database rows into `Order`s,
  `orders/shipping_mapping.py` turning `Order`s into `Shipment`s. A mapper may also make
  the calls that fetch its source, such as a carrier client that requests the payload
  and translates it.

Anything else is not one of those places:

- the source type: `Order.to_shipment()` builds a `Shipment` from inside `Order`;
- code whose job is something else: a service method, a use case, a view, a command or
  a task handler that builds `C` inline among its other work, even one that holds
  collaborators;
- a module that is neither `C`'s module nor a mapper for this source:
  `shipping/planning.py` with a `make_shipment(order)` among planning functions.

Code that only delegates may live anywhere: a cache, registry or service that gets its
instance from an alternative constructor, a factory or a mapper (`_handlers[name] =
Handler.for_name(name)`, `events = acme.events_from(payload)`,
`self._invoices.create(order)`).

Violation: a construction that decides a program type's field values, in a place that
is not on that type, in its module, in a factory for it, or in a mapper for its source.
The violation is the construction call.

Not a violation:

- any construction on the built type or in its module;
- any construction in a mapper for one source, whether the source is outside data or
  another program type; a mapper is never required, and never a violation;
- any construction in a factory whose collaborators decide field values;
- delegation to an alternative constructor, a factory or a mapper, from anywhere;
- instances of classes the program doesn't declare (`Path`, `datetime`, `Decimal`, a
  third-party SDK's request object);
- copies of an existing instance with changed fields (`dataclasses.replace(order, ...)`,
  `order.model_copy(update=...)`, `attrs.evolve(order, ...)`).

### Defaults supplied outside the type

A default is the value a field takes when the caller has none: a literal or constant
(`"EUR"`, `DEFAULT_CARRIER`), an enum member, an empty collection, or a freshly
generated value (`uuid4()`, `datetime.now(UTC)`, `secrets.token_hex(8)`). It does not
depend on the call's other inputs. A fallback to other data is not a default: a
customer's preferred carrier, a value read from the order, a setting passed in. A value
a factory's injected collaborator produces (`self._clock.now()`,
`self._numbers.next()`) is not a default either: it is what the factory was given to
decide.

A field's default is declared by the type that owns the field, on the class itself: a
field default, `field(default_factory=...)`, pydantic `Field(default=...)` or
`default_factory`, attrs `attrs.field(default=...)`, a Django
`models.CharField(default=...)`, a SQLAlchemy `mapped_column(default=...)`,
`__post_init__`, a validator, or a `@classmethod` constructor on the class.

Violation: code outside the class that supplies a default for one of the class's
fields, as a constructor argument, a `model_validate` or `objects.create` key, or an
attribute set on a new instance, in any of these forms:

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

This holds wherever the construction is, including in the type's module, a factory or
a mapper: those homes decide field values from their source or their collaborators,
and a default still belongs on the class. A freshly generated value produced by the
building code itself (`datetime.now(UTC)`, `uuid4()`), not by an injected
collaborator, is always a default. The violation is the argument or assignment that
supplies the default.

Not a violation:

- the class declares the default itself, and the caller omits the field;
- the value comes from other data, not a default (`carrier=customer.preferred_carrier`,
  `currency=order.currency`), or from a factory's injected collaborator;
- a literal passed without a fallback, as this call's choice
  (`Notification(channel="email", ...)` in an email sender);
- the field belongs to a class the program doesn't declare: a library call's keyword
  (`requests.get(url, timeout=10)`, `httpx.Client(base_url=...)`);
- the parameter default configures the function itself and never reaches a field
  (`def fetch(page_size=50)` used only to slice).

## Violation

Code in the file under review that decides how a program type is built outside that
type's home: a construction deciding its field values somewhere other than the type,
its module, a factory whose collaborators decide them, or a mapper for its source; or a
default for one of its fields supplied by code outside the class.
