---
name: no-copied-owner-values
description: A class that stores a copy of a value it can already reach, either a field of an object it also stores (`self.email = customer.email` beside `self.customer = customer`) or the key it is registered under (`kind = "express"` in a class registered as `"express"`), is a violation.
---

# No copies of a value the class can already reach

A value has one home; a class that can already reach it reads it there instead of
keeping its own copy.

A class can reach a value in two ways:

- through an object it stores: when the class stores `customer` (an attribute, or a
  dataclass, attrs or pydantic field), `customer.email` is reachable;
- through the key it is registered under: when the file, or a module it imports from,
  maps a key to the class or an instance of it (`STRATEGIES = {"express":
  ExpressShipping()}`, `@register("express")`, an enum member's value), that key is
  where the class is found, and so already known wherever the class is looked up.

A copy is an attribute, field or class attribute that the class stores whose value is
one of these: read from the stored object, or equal to the registration key.

## The test

For each attribute, field or class attribute the class stores, ask two questions:

1. Is its value read from, or always equal to, a field of another object this class
   also stores?
2. Is its value equal to the key this class, or an instance of it, is registered under?

Yes to either is a violation, in any form: `self.email = customer.email` in `__init__`,
`__post_init__` or another method beside `self.customer = customer`; fields
`customer: Customer` and `customer_email: str` filled from the customer; a class
attribute `kind = "express"` or `format_name = "csv"` on a class registered under
`"express"` or `"csv"`.

Not a violation:

- a value stored without the object it came from: a `SentReceipt` that keeps the email
  it was sent to and stores no customer;
- a key kept to look an object up later (`self.customer_id`), when the class does not
  also store that object;
- a value computed from several sources (`self.total = sum(line.cents for line in
  lines)`), which is no single object's field;
- a class attribute that differs from the registration key (`base_cents = 1500` on the
  class registered as `"express"`);
- a property or method that reads the value where it lives (`return
  self.customer.email`).

## Violation

A class in the file under review that stores a copy of a field of an object it also
stores, or of the key it is registered under.
