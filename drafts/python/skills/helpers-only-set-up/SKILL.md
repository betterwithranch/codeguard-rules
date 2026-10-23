---
name: helpers-only-set-up
description: A test helper or fixture never gets a value from the production code that computes that value for the code under test
---

# Helpers set up; they never compute what production computes

A value a test checks against comes from the test, not from the code being tested.

The code under test is what the test's act calls, together with the production
functions, classes and allocators it calls to produce its result. A computed value is
one the code under test derives rather than receives: an id or number it allocates, a
key, slug, hash or token it derives, an ordering or ranking it sorts by, a total or
price it calculates. The production module the test imports shows which code computes
which value.

## The test

For each value a helper or fixture returns, ask: is it obtained by calling the code
under test, or a production function, method or class that the code under test calls
to compute that same value?

Not a violation:

- a literal or a value the helper writes out: `"eu:A1"`, `["urgent", "normal"]`,
  `"INV-0002"`;
- a value the helper computes itself with plain code or the standard library
  (`hashlib.sha256(body).hexdigest()`, `sorted(tasks, key=lambda task: task.due)`),
  even when production computes the same thing;
- an input built with production code: a constructor, factory or creator that makes
  the records, objects and collaborators the act uses
  (`ArticleService(db).create(title="Hello")`).

A violation:

- `return cache_key(product.sku, product.region)` when the cache under test stores
  entries under `cache_key(...)`;
- `return InvoiceNumberAllocator(db).peek_next()` when the invoice service under test
  numbers invoices with that allocator;
- `return sorted(tasks, key=priority_key)` when the scheduler under test orders by
  `priority_key`;
- `return article.build_slug()` or `return Article.slug_for(title)` when the save under
  test sets the slug with that method.

## Violation

A test helper or fixture that returns a value it gets by calling the code under test,
or the production code that computes that value for it.
