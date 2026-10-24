---
name: layers-earn-their-load
description: Every layer (an interface, a protocol, a wrapper function or class, an argument group, an identity type) hides a real decision; a layer that only passes things through to one other thing is a violation.
---

# Layers earn their load

Every layer a reader has to learn hides a decision they then don't have to make; a layer
that only passes something through adds a name and a hop and hides nothing.

A layer is a name the program declares between a caller and the code that does the
work: an interface, a protocol, a wrapper function, a class that holds a collaborator, an
object built to carry a call's arguments, a type for one identifier. A decision is
something the layer settles for its callers: which of several implementations runs, an
import it keeps from becoming a cycle, a check, a conversion, a default, a retry, a
cache, a filter, a computation, behaviour of its own. Forwarding a call, renaming it, or
holding a value is not a decision.

The code the layer passes through to, its implementers and its callers are in the file
under review or in files of the repository; read them there, and search the repository
for a name when the forms below ask how often it is used.

## The test

For each interface, protocol, wrapper, collaborator-holding class, argument group and
identifier type in the file under review, ask: does this layer hide a real decision, or
does it only pass things through to one other thing, in a way a form below names as a
violation?

### Interfaces with one implementer

An interface is a class whose bases include `Protocol` (`typing.Protocol`,
`Protocol[T]`) or `ABC` (`abc.ABC`, `metaclass=ABCMeta`), with members left for others to
supply: `...` bodies or `@abstractmethod`. An implementer is a class outside test files
that subclasses the interface or, for a `Protocol`, defines all of its members: methods
with the same signatures, data attributes with the same names and types (a dataclass or
`NamedTuple` with those fields implements a protocol of those attributes). A test double (a class under `tests/` or in `conftest.py`, or named
`Fake`, `Stub`, `Mock` or `Dummy`) is not an implementer. A consumer is code that
annotates a parameter, attribute or return value with the interface. An implementer
someone plans to write is not an implementer: only code in the repository counts.

For each interface defined in the file, find its implementers: in the file, and in the
rest of the repository by searching for the interface's name and, for a `Protocol`, its
method names. Then ask:

1. Are there two or more implementers? Yes is not a violation.
2. Otherwise, would retyping each consumer against the one implementer make the
   consumer's module import the implementer's module, when the implementer's module
   already imports the consumer's module, directly or through the modules it imports?
   Yes, the interface prevents an import cycle, so it is not a violation. No is a
   violation.

An interface with no implementer at all is a violation by the same test. The violation is
the interface's class.

Not a violation:

- a `Protocol` in a lower-level package, for what that package needs from a
  higher-level one that imports it, even with one implementer;
- a `Protocol` or `ABC` with two or more implementers in the repository, wherever they
  are;
- an abstract Django model (`class Meta: abstract = True`), a pydantic `BaseModel`, or a
  base class with no members left for others to supply, which are not interfaces.

### Protocols that mirror one class's attributes

A protocol's members are data members (annotated attributes such as
`timeout_seconds: int`, and properties that only return a value) or methods that do
work. A concrete class is a class in the program that holds data: a dataclass, an attrs
class, a pydantic model or `BaseSettings`, a Django or SQLAlchemy model, a `NamedTuple`
or a plain class. It matches a member when it declares a field or attribute of the same
name and type.

For each `Protocol` defined in the file, ask:

1. Are all of its members data members?
2. Does exactly one concrete class in the repository match every member (search the
   repository for the member names)?
3. Does that class declare fields the protocol leaves out?

Yes to all three is a violation, whatever its implementer count; the violation is the
protocol's class. No to any is not.

Not a violation:

- a protocol with a method that does work (`def charge(self, token: str) -> str`),
  however many data members it also has;
- a protocol whose data members several concrete classes match (`HasId` with `id: int`
  matched by many models);
- a protocol whose members no single class matches, or that matches a class field for
  field with nothing left out.

Each form is its own test. A protocol this form allows is still a violation of
"Interfaces with one implementer" when fewer than two classes implement it and it
prevents no import cycle: a protocol matching one class field for field has that one
implementer, and one no class matches has none.

### Pass-through classes

A pass-through class holds one collaborator, an object its `__init__` only stores from
its parameters (`self._store = store`), and every other method only forwards to it: its
body (after an optional docstring) is one call of a method of that collaborator with the
method's own parameters, unchanged, returned or awaited as is
(`def get(self, key): return self._store.get(key)`).

Violation: a class whose methods, every one of them, only forward to the same held
collaborator with the same arguments, whatever the methods are called. The violation is
the class.

Not a violation:

- a class where any method adds a decision: retries, caches, converts its arguments,
  results or errors, checks, defaults a value, combines calls, or chooses between
  collaborators;
- a class that holds two or more collaborators and uses more than one;
- a class that implements an interface the program declares, which it fits its
  collaborator to;
- a class whose `__init__` builds or configures its collaborator rather than receiving
  it;
- one method that delegates inside a class whose other methods do work.

### Single-use map wrappers

A map wrapper is a function whose whole body returns one comprehension, generator or
`map` that calls an already-named function or method on each item and does nothing
else: `return [label(shipment) for shipment in shipments]`,
`return {s.id: label(s) for s in shipments}`, `return list(map(label, shipments))`,
`return [self.label(s) for s in shipments]`.

It adds behaviour when the comprehension does more than call the named function: it
filters (`if shipment.active`), computes inline (`shipment.weight * RATE`, an f-string,
a constructor with several fields), unpacks (`for sku, qty in rows`), sorts,
deduplicates, or handles errors.

A call site is a call or reference to the function anywhere in the project: in the file
under review, or in any other file (search the repository for its name). A reference
passed as a value (`sorted(..., key=labels)`, a registry entry, a framework hook name,
an overridden or `Protocol` method) counts as more than one, since the caller is outside
the code.

Violation: a map wrapper that adds no behaviour, has exactly one call site, and
implements no method a base class or `Protocol` declares: `_labels(shipments)` returning
`[label(s) for s in shipments]`, called once by `dispatch`. The violation is the
wrapper.

Not a violation: a map wrapper that adds behaviour, has two or more call sites or a
reference passed as a value, or implements a method a base class or `Protocol` declares.

### Unpacked argument groups

An argument group is an object of a class the program declares only to carry values
together: a dataclass, attrs class, pydantic model, `NamedTuple` or `TypedDict`, or a
plain class whose `__init__` only stores its parameters. Unpacking it is reading its
fields back out as the arguments of a call: as attributes (`build_quote(args.cart,
args.region)`, `build_quote(cart=args.cart)`), or by splatting a dump of it
(`build_quote(**asdict(args))`, `*astuple(args)`, `**args.model_dump()`, `**vars(args)`,
`**args._asdict()`).

For each call that takes its arguments from an object's fields, ask:

1. Was the object built in the same function, from values that function already had,
   and is it an argument group?
2. Are reads that feed this call, or calls like it, the only uses of the object: it is
   not passed whole to any call, returned, yielded, stored on `self` or in a collection,
   and none of its methods are called?

Violation: yes to both, a function that builds an argument group and then only unpacks
it into a call's arguments:

```python
def quote(cart: Cart, region: Region) -> Quote:
    args = QuoteArgs(cart=cart, region=region)
    return build_quote(args.cart, args.region)
```

`build_quote(**asdict(QuoteArgs(cart=cart, region=region)))` is the same violation in
one expression. The violation is the call that unpacks it, not the line that builds the
group.

Not a violation:

- an argument group handed whole to the callee, which reads its fields itself:
  `QuoteFactory().create(QuoteParams(cart=cart, region=region))`;
- an object the function received as a parameter or got from another call, whose fields
  it passes on (`ship(order.id, order.address)`);
- an object that is also used whole: returned, stored, logged as one value, or passed to
  another call;
- an object whose construction does work beyond storing values: it validates, converts
  or defaults them (a pydantic model that parses strings into dates, a dataclass with a
  `__post_init__` that normalizes), so its fields differ from the values it was given; a
  pydantic model given values already of its fields' types converts nothing, so it is an
  argument group;
- a splat of a dict that is not a dump of an argument group (`**headers_for(payload)`,
  `**kwargs`).

### Bare identity wrappers

An identifier is a value whose job is to name one record or thing: an id, key, code,
slug, reference number or UUID (`order_id: str`, `sku: str`, `customer_key: UUID`).
Behaviour is a method or property beyond construction, `__repr__`, `__str__`, equality
and hashing. A check is code the class runs on the value: a pydantic validator or
constrained field (`Field(pattern=...)`, `constr`), an attrs validator, a check in
`__init__` or `__post_init__` that raises, or an enum's closed set of members.

Violation: a class whose instances hold exactly one value, an identifier, and which
defines no behaviour and no check, in any form: a dataclass, attrs class or
`NamedTuple` with one identifier field; a pydantic `BaseModel` with one identifier field
and no validator or constraint; a plain class whose `__init__` stores one identifier; a
subclass of `str`, `int` or `UUID` with an empty body. The violation is the class.

Not a violation:

- `NewType("UserId", str)` and type aliases, which brand an identifier for the type
  checker without a class;
- a class that checks its value (an `Iban` that verifies its checksum, a `Sku` whose
  pydantic field has a `pattern`), or an enum;
- a class with behaviour (`TrackingNumber.carrier()`);
- a class with two or more values (`OrderRef(region, number)`), or one value that is not
  an identifier (`Money(cents)`, `Percentage(value)`);
- a Django or SQLAlchemy model, which stores a record, not a key.

## Violation

A layer in the file under review that hides no decision: an interface with fewer than
two implementers that prevents no import cycle, a protocol that mirrors one class's
data attributes, a class whose methods only forward to one held collaborator, a map
wrapper used once that adds no behaviour, an argument group built only to be unpacked
into one call, or a class that holds only one identifier with no behaviour and no
check.
