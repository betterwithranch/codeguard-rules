---
name: no-shared-test-class-state
description: No test changes data stored on its test class, which every test of the class shares
---

# No state shared through test class attributes

Tests of a test class never change data stored on the class itself.

A class attribute of a test class belongs to the class, so every test of the class
sees the same object: it is assigned in the class body, through `cls` (in
`setup_class`, `setUpClass` or a classmethod), through `type(self)`, or through the
class's name. pytest and unittest make a new instance for each test, so an attribute
the test or its setup assigns on `self` (`self.skus = []` in `setup_method` or `setUp`)
belongs to that test alone.

A change is an assignment (`cls.last_cart = cart`, `TestCart.count += 1`), an item
assignment (`self.totals["A-1"] = 3`), or a mutating call (`append`, `extend`,
`insert`, `add`, `update`, `setdefault`, `pop`, `remove`, `discard`, `clear`) on the
attribute's object.

## The test

For each change a test or setup method makes to data reached through `self`, `cls`,
`type(self)` or the class's name, ask: does the data belong to the class, or to this
test's instance?

Not a violation:

- `self.skus = []` in `setup_method`, then `self.skus.append("BOOK-1")` in a test;
- a class attribute the tests only read: `skus = ("BOOK-1", "PEN-2")`, or a list no
  test changes;
- `setup_class` that sets `cls.catalog = load_catalog()` when no test changes it.

A violation:

- `added_skus = []` in the class body, and a test that calls
  `self.added_skus.append(...)`;
- `seen = {}` in the class body, and a test that sets `self.seen["A-1"] = 1`;
- a test that sets `TestCart.last_cart = cart` or `type(self).last_cart = cart` for
  another test to read.

## Violation

A test or setup method that changes data stored on its test class.
