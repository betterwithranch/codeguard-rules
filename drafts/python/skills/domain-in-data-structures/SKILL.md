---
name: domain-in-data-structures
description: A domain rule is stated once, in a structure the program declares (an enum, a named type, a table, one dispatch, one helper, one field), never repeated across branches, positions, sibling helpers or fields kept in agreement by hand.
---

# The domain is modelled in data structures, not scattered conditionals

Each rule of the domain is stated once, in a structure the program declares, and the
code reads that structure instead of restating the rule.

A domain rule is a fact about the program's subject that code acts on: which kinds of
payment exist and how each behaves, which states an order can be in, what a result's
parts mean, which item a key stands for. A declared structure states it once: an enum,
a named type (dataclass, `NamedTuple`, `TypedDict`, attrs class, pydantic model), a
table or registry, one dispatch, one helper taking the varying value, one field the
others are derived from.

## The test

For each piece of code the forms below describe, ask: is a domain rule here restated,
or carried only by position, string values or hand-kept agreement, in a way the form
names as a violation?

A single branch, one `if`/`else`, or one lookup is never a violation on its own: each
form needs the rule repeated, or left where the program's types can't see it.

### Repeated type switches

A type switch picks a branch by which of several types a value has: an `if`/`elif`
chain of `isinstance` or `issubclass` checks, `type(x) is` or `type(x) ==`
comparisons, a `match` with class patterns (`case CardPayment():`), or a lookup keyed
by `type(x)` (`handlers[type(event)]`).

Violation: two or more functions or methods in the file each switch on a value of the
same kind with at least two of the same types among their choices, whether module
functions, methods of one class or of several, Django or DRF views, or a serializer's
`to_representation`. The violation is each switch after the first.

Not type switches: a single `isinstance` guard that rejects or narrows one type (in a
pydantic `field_validator`, an `__eq__`), `functools.singledispatch` registrations,
methods each type defines for itself, and `except` clauses. A switch on values (`match`
on strings, `payment.kind == "card"`) is not a type switch.

### Branching on a `Literal` value set

A literal value set is a single `Literal[...]` listing two or more values, in an
annotation or an alias (`type OrderStatus = Literal["pending", "shipped", "cancelled"]`).
A one-value `Literal["card"]` is a tag, and stays one when read through a union of
variants that each declare their own (`payment.kind` where
`payment: CardPayment | BankTransfer`).

Find the branched-on value's type from its annotation, the field or parameter it is
read from, or the alias it names, following an import to the file that defines it.

Violation: code branches on a value typed as a literal value set: `==` or `!=` against
one of its values, `in` a tuple, list or set of them, `case` on them, or a dict or
registry keyed by them and indexed with the value. This holds for a dataclass,
pydantic, attrs or `TypedDict` field, a parameter, and a SQLAlchemy `Mapped[...]` or
Django field annotated with the Literal. For a keyed table, the violation is the dict
literal that spells the keys.

Not a violation: branching on members of a `StrEnum`, `IntEnum` or Django
`TextChoices`; a literal value set only stored, validated, passed on or serialized; a
branch on a tag or on the variant's class; comparing a value typed `str`, or whose
type the code doesn't show, to a string.

### Anonymous results

A function returns an anonymous result when it returns a tuple (`return reason, held`)
or a dict with a fixed set of string keys written in the function
(`return {"reason": reason, "held": held}`), read by position or key.

Violation: the anonymous result's elements answer different questions about the
input: a reason and a flag, a fee and a delivery date, a parsed value and its warnings,
a record and whether it was created (`return user, created`). The violation is the
return.

Not a violation: elements that are one kind of thing in a collection
(`tuple[Order, ...]`, `{order.id: order for ...}`); a pair whose positions a language
or library protocol fixes (`__divmod__`, `(key, value)` items for `dict(...)`,
`__reduce__`, `(status, headers, body)` for WSGI or ASGI); a dict in the shape
something outside the program defines (an HTTP body, a documented JSON payload, a
template context, `**kwargs` for a library call); a named type returned instead.

### Silent key overwrites

A mapping build fills a dict from a collection: `index[key] = item` in a loop, a dict
comprehension, `dict(...)` over pairs or `zip`, `setdefault(key, item)`, or
`update({key: item})` in a loop. Its key is unique when no two items can have it: the
items' own id or primary key, a field the model declares unique, the keys of another
mapping, an `enumerate` index. Anything else is a key two items can share: a foreign
key (`order.customer_id`), a status, a category, a date, a name. Decide from the
item's model when it can be read; when it can't, the field's name decides: the item's
own `id` or `pk` is unique, and a field naming another record (`payment.invoice_id`), a
status, a category, a region or a date is a key two items can share.

Violation: a build keyed by a value two items can share keeps one item per key (a
later one replaces an earlier one, or `setdefault` with the item blocks it), and
nothing chooses which item is kept or notices the duplicate:
`{order.customer_id: order for order in orders}`.

Not a violation: a unique key; every item kept, grouped into lists
(`setdefault(key, []).append(item)`, `defaultdict(list)`) or merged
(`totals[key] = totals.get(key, 0) + item.cents`); a duplicate that raises; the code
choosing the item kept, by iterating items sorted by the deciding field or comparing
before replacing (`if event.at > latest[key].at`).

### Helpers differing by one value

A private helper is a function or method whose name starts with a single underscore,
or a function nested in another. Siblings are defined in the same class body or at the
top level of the same module. A variant value is a literal or an enum member.

Violation: two or more sibling private helpers whose bodies are the same, statement
for statement, except that one literal or enum member is replaced by another wherever
it appears (`_missing(field)` appending `ValidationIssue(field, IssueType.MISSING)` and
`_invalid(field)` appending `ValidationIssue(field, IssueType.INVALID)`), on any kind
of class or at module level, sync or async. The violation is each helper after the
first.

Not a violation: helpers differing by more than one value or by any other statement or
call; one helper taking the value as a parameter; public methods, whose names callers
use.

### Fields kept in agreement by hand

A derived flag is a boolean field of a class that states a fact another field of the
same class already holds: `is_shipped` beside `shipped_at`, `is_paid` beside
`status: PaymentStatus` with a `PAID` member, `is_cancelled` beside `cancelled_on`. A
boolean field holding a fact no other field holds (`is_gift`, `newsletter_opt_in`) is
not derived.

Violation: a derived flag, declared as a dataclass, pydantic, attrs, SQLAlchemy or
Django field, or set on `self` in `__init__`; or code that sets a derived flag and the
field it mirrors together (`order.shipped_at = now` then `order.is_shipped = True`).
The violation is the flag's declaration, or its assignment where the class isn't in
the file.

Not a violation: a `@property` or `cached_property` that computes the flag from the
other field (`return self.shipped_at is not None`); a boolean whose fact is its own;
a flag on a different class (a read model or an API response copying both fields
from the record).

## Violation

Code in the file under review that restates a domain rule in one of the forms above:
a repeated type switch, a branch on a `Literal` value set, a return of an anonymous
result whose parts answer different questions, a mapping build that silently drops
items sharing a key, a sibling helper differing only by one value, or a derived flag
kept in agreement with the field it mirrors.
