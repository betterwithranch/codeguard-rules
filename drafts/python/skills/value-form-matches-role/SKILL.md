---
name: value-form-matches-role
description: A value code supplies has the form its role calls for; a reference to another record carries that record's id, and a value matched against fixed values is fixed
---

# A supplied value's form matches its role

Each value code passes to a call or constructor has the form that the receiving code's
use of it calls for.

The role of a value is what the receiving code does with it, which the receiver's
definition shows (a model's foreign key, a repository's lookup, a `match` on a field):

- a reference: the receiver looks up, joins or links another record by it
  (`order_id`, `customer_id`, `parent`, a foreign key);
- a new identity: the receiver stores it as the new record's own id;
- a matched value: the receiver compares it to fixed values or branches on it
  (`status`, `kind`, `channel`);
- a free value: the receiver stores or shows it without comparing it (a name, a note,
  a description, an amount).

## The test

For each value a call supplies, find its role, and ask: does its form fit that role?

Fits, so not a violation:

- a reference taken from a record the code created or loaded: `order_id=order.id`,
  `parent=category`, `customer_id=customer.pk`;
- a new identity that is generated: `Order(id=uuid4(), ...)`, `id=ulid()`;
- a matched value written as a literal or an enum member: `status="pending"`,
  `kind=ShipmentKind.EXPRESS`;
- a free value in any form: `notes=f"seeded {uuid4().hex[:6]}"`.

Doesn't fit:

- a reference given a fresh generated id that no record has: `order_id=uuid4()`,
  `customer_id=str(uuid.uuid4())`, `account_id=secrets.token_hex(8)`;
- a reference given a made-up literal that no record the code created or loaded has:
  `order_id="ord-1"`, `parent_id=1`;
- a matched value given a generated or random value: `kind=uuid4().hex`,
  `channel=random.choice(["sms", "email"])` passed where the receiver branches on it.

## Violation

A value passed to a call whose form doesn't fit its role at the receiver: a reference
that carries no existing record's id, or a matched value that is generated.
