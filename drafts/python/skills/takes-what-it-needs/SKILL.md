---
name: takes-what-it-needs
description: A unit takes exactly what it needs, in the form its role needs; a signature or call doesn't hand it a collaborator per call, a bundle for a few fields, a value along with the input it was derived from, or a value in the wrong form for its role.
---

# A unit takes what it needs, in the form its role needs

Each function, method or class is given exactly the inputs its work needs, each in the
form its role at the receiver calls for, so a reader of the signature or the call sees
what the unit depends on.

A unit is a function, method or class. Its inputs are its parameters, the arguments a
call passes it, and, for a class, its constructor's parameters and fields. Read the
receiver's definition in the file under review or a file of the program it imports to
see what it does with an input.

Two kinds of input:

- a collaborator is an object the unit calls to get work done: a client, a repository
  or DAO, a rate or price provider, a strategy, a formatter or renderer, a registry, a
  clock, a mailer, a cache. Its kind decides it, from its annotation or, when it has
  none, from its name and from what the unit does with it;
- data is what the call is about: the records, ids, amounts, dates, a request or event,
  a model instance, a query, a callback a caller supplies for this one call.

A class taking its collaborators in `__init__`, as dataclass, attrs or pydantic fields,
or through a `@classmethod` that builds the instance and stores them, is how a class is
given collaborators: it is never a violation of this rule, and neither is a call that
builds those collaborators and passes them to the constructor. The rule never asks for
inputs to be grouped into a parameter object: a function taking several plain values is
the form it allows.

## The test

For each input in the forms below, ask: does the unit get it in the form below that
names a violation, or exactly what its work needs, in the form its role needs?

### A collaborator passed per call

For each parameter of a method of a class (other than `self` and `cls`), ask: is it a
collaborator the method calls to do its work, or the data this call works on?

- collaborator: `rate_provider: RateProvider` used as `rate_provider.rate_cents(...)`,
  `formatter: CurrencyFormatter`, `repo: OrderRepository`, `client: httpx.Client`,
  `clock: Clock`, an untyped `mailer` the method calls `.send()` on;
- data: `shipment: Shipment`, `order_id: int`, `lines: list[InvoiceLine]`,
  `request: HttpRequest` in a Django or DRF view method, `since: datetime`, a pydantic
  model, a SQLAlchemy row, `key=` passed to `sorted` for this call.

Violation: a method of a class takes a collaborator as a parameter: in a plain class, a
dataclass, an attrs class, a pydantic model, a Django model or view, whether the method
is public, private, a `@staticmethod`, or an `async def`. It is reported on the
parameter.

Not a violation:

- `__init__`, a dataclass, attrs or pydantic field, or a `@classmethod` that builds the
  instance and stores the collaborator on it (`from_settings(cls, client)`);
- a module-level function that takes a collaborator, since it has no constructor;
- a parameter whose type is data, even when the method calls its methods
  (`order.total_cents()`);
- a method whose signature a base class, `Protocol` or framework declares with that
  parameter (a handler interface `def handle(self, event, bus)` that the class
  implements).

### A bundle taken for a few fields

A bundle is an object whose job is to carry many unrelated values to many consumers:
a context (`CheckoutContext`, `RequestContext`), settings or config (`Settings`,
`AppConfig`, a pydantic `BaseSettings`), a web request (`HttpRequest`, a FastAPI
`Request`), an environment or app-state object. Its fields are inputs for different
parts of the program, not facts about one thing. A domain value is not a bundle: an
`Order`, `Invoice` or `Shipment`, a `DateRange`, a `Money`, a `TypedDict` of one
record's fields, whose fields all describe one thing. The bundle's class is declared in
the file under review or a file it imports; read it there to see its fields. A
framework's request and settings types are bundles.

For each parameter that is a bundle, ask two questions:

1. Is every use of the parameter a read of one of its fields (`context.shipping_region`,
   `settings.page_size`, `request.headers`)? It is not when the function passes the
   object on to another call (`self._printer.archive(context)`), calls one of its methods
   (`context.receipt_lines()`, `request.is_secure()`), or returns it, stores it on
   `self`, or yields it.
2. Count the distinct fields the function reads and the fields the bundle's class
   declares. Does it read half of them or fewer?

Violation: yes to both, in a function or method: a method
`tax_cents(self, context: CheckoutContext)` that reads `context.subtotal_cents` and
`context.shipping_region`, a helper taking `settings: Settings` for one timeout.
Reading 2 of 6 fields is a violation; reading 3 of 4 is not. It is reported on the
parameter.

Not a violation:

- a domain value parameter, however few of its fields the function reads;
- a bundle the function uses as a whole, as listed above;
- several plain values taken as separate parameters, however many;
- a framework method whose signature the framework sets: a Django or DRF view's
  `get(self, request)`, a FastAPI route that declares `request: Request`, a middleware's
  `__call__(self, request)`.

### A value passed with the input it was derived from

A value is derived from an input when the caller computes it from that input: a call
that takes it (`select_lines(cart, region)` from `region`), one of its fields
(`order.email` from `order`), or a key of it (`context["region"]`). The derivation is
inline in the argument list or assigned to a local earlier in the same function
(`rate = tax_rate(customer)` and then `invoice_total(subtotal, rate, customer)`).

For each call that receives both an input and a value derived from it, ask: is the
callee a function, method or class the program declares, so it could take the input
and derive the value itself?

Yes, a violation, reported on the call:

- a function or method declared in the file under review or a file of the program it
  imports: `quote(lines=select_lines(cart, region), region=region)`,
  `notify(order.email, order)`, `self._render(self._totals(invoice), invoice)`;
- a class the program declares that stores derived data next to its source: a
  dataclass, pydantic model or attrs class built with
  `Summary(total=total_of(lines), lines=lines)`.

No, not a violation:

- a builtin or library callee, which can't be changed to derive it: `dict.get(key,
  default_for(key))`, `getattr`, `min`, `max`, `print`, `logging`, `os.path.join`,
  `re.sub`, a third-party client's method;
- the derived argument is a collaborator built to be injected, not a value: an object
  the callee calls methods on (`Service(repo=OrderRepository(session), session=session)`,
  `RetryingClient(HttpClient(config), config)`).

### A value in the wrong form for its role

The role of a value is what the receiving code does with it, which the receiver's
definition shows (a model's foreign key, a repository's lookup, a `match` on a field, a
task that runs later):

- a reference: the receiver looks up, joins or links another record by it
  (`order_id`, `customer_id`, `parent`, a foreign key);
- a new identity: the receiver stores it as the new record's own id;
- a matched value: the receiver compares it to fixed values or branches on it
  (`status`, `kind`, `channel`);
- a free value: the receiver stores or shows it without comparing it (a name, a note,
  a description, an amount);
- deferred work: the receiver runs later or in another process, across a queue, task
  or workflow boundary.

A boundary is a call that serializes its arguments and runs the receiver later or in
another process: Celery's `.delay`, `.apply_async`, `.s` and `.si`, RQ's `enqueue`,
Dramatiq's `.send`, a broker client's `publish`, a multiprocessing queue's `put` or a
process pool's `submit`, and Temporal or other workflow calls that start a workflow or
run an activity. A task function is the function such a call runs: one decorated
`@shared_task`, `@app.task`, `@dramatiq.actor`, `@activity.defn` or `@workflow.run`.
In-process hand-offs do not serialize and are not boundaries: an `asyncio.Queue`, a
`queue.Queue` between threads, a thread pool's `submit`, a direct call.

A stored record is an object the program saves and loads again by id: a Django or
SQLAlchemy model instance, a document from a document store, or a domain object a
repository returns. A whole-record dump is a copy of all its fields:
`model_to_dict(order)`, `order.model_dump()`, `asdict(order)`, `vars(order)`,
`order.__dict__`, or a serializer's `.data` for it.

For each value a call supplies, and each parameter of a task function, find its role,
and ask: does its form fit that role?

Fits, so not a violation:

- a reference taken from a record the code created or loaded: `order_id=order.id`,
  `parent=category`, `customer_id=customer.pk`;
- a new identity that is generated: `Order(id=uuid4(), ...)`, `id=ulid()`;
- a matched value written as a literal or an enum member: `status="pending"`,
  `kind=ShipmentKind.EXPRESS`;
- a free value in any form: `notes=f"seeded {uuid4().hex[:6]}"`;
- across a boundary, an id or key (`order.id`, `str(order.pk)`), a value that is not a
  stored record (a date, an amount, a list of ids, a computed result), or a message
  built from chosen fields that states an event (`{"order_id": order.id,
  "total_cents": order.total_cents}`).

Doesn't fit, a violation reported on the value:

- a reference given a fresh generated id that no record has: `order_id=uuid4()`,
  `customer_id=str(uuid.uuid4())`, `account_id=secrets.token_hex(8)`;
- a reference given a made-up literal that no record the code created or loaded has:
  `order_id="ord-1"`, `parent_id=1`;
- a matched value given a generated or random value: `kind=uuid4().hex`,
  `channel=random.choice(["sms", "email"])` passed where the receiver branches on it;
- a stored record, or a whole-record dump of one, passed across a boundary or taken as
  a task function's parameter.

## Violation

Code in the file under review that gives a unit more than, or other than, what it
needs: a method taking a collaborator per call, a function taking a bundle to read a
few of its fields, a call passing a value with the input it was derived from to a
callee the program declares, or a value whose form doesn't fit its role at the
receiver (a reference that carries no existing record's id, a matched value that is
generated, a stored record or its dump handed across a boundary).
