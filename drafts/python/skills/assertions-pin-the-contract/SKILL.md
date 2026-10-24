---
name: assertions-pin-the-contract
description: A test's assertions check the behaviour the test names, no less and no more; each fails when that behaviour breaks, and its expected value is stated by the test, not computed by the code under test or left to the run.
---

# Assertions pin the contract

A test's assertions check the behaviour the test is about, no less and no more: each
one fails when that behaviour breaks, and the value it expects is stated by the test
from the requirement.

The contract is the behaviour the test names: its name, and what its act calls and
checks. The produced value is what the call under test returned, changed or sent (a
request or message a fake recorded), read from the test's code. Which side of a
comparison it is on doesn't matter.

The contract decides, not the shape of the assertion: one field, one item, a set of
members, an identity, or a whole value can each be the property the test is about.

## The test

For each assertion, including `self.assert...` methods, ask two questions:

1. If the behaviour the test names broke, would this assertion fail, including when
   the break is in a field the produced value gains later?
2. Is its expected value stated by the test (a literal, a value the test builds or
   assigns, a value read from inputs the test controls), rather than computed by the
   code under test, read from a shared constant, or dependent on the run?

Two yeses: not a violation. Any no, in one of the forms below: a violation. Each form
says where the violation is reported.

### Parts instead of the whole produced value

Parts of a produced value are its fields, items and keys, members of a set it is or
holds, how many items it has, and values computed from it, such as a filtered subset of
its items or an outcome derived from it. Fields that together are one property the
test is about, such as a node's start and end line as its span, are one part.

One comparison of the whole value could replace parts when its type has `__eq__`: a
dict, list, set or tuple, a dataclass or attrs class (unless declared with
`eq=False`), a `NamedTuple`, a `TypedDict`, a pydantic model, a class that defines
`__eq__`. A value whose type the file and the files it imports don't show counts as
having `__eq__` only when the test shows it does: it compares the value, or a value of
the same type, with `==` against an expected value it builds. Otherwise it counts as
having none. A field that changes each run (a generated id, a timestamp, a duration)
doesn't stop a whole comparison: the test can control its source.

Violation: the assertions on one produced value whose type has `__eq__`:

- check one part when the behaviour the test names covers more of the value (`assert
  parcels[0].sku == "A1"` in a test that parcels are ordered by sku);
- check several of its parts, each in its own assertion (`assert invoice.number ==
  "42"` then `assert invoice.total == 120`), or several at once (`assert
  (invoice.number, invoice.total) == expected_pair`, `assert [(p.sku, p.qty) for p in
  parcels] == [("A1", 1), ("B2", 2)]`), even when they cover every field today: a
  field added later goes unchecked;
- check several members of one set or collection (`assert "draft" in tags` with
  `assert "published" not in tags`): comparing the expected set also catches members
  nobody expected;
- check a value derived from it instead of it: a filtered subset of its items
  (`[f for f in report.findings if f.is_failure] == []`) or an outcome computed from it
  (`status_of(report) is Status.PASSED`), alone or beside other parts;
- check several fields of a value whose other fields change each run (`assert
  (attrs["cache_hit"], attrs["sku"]) == (False, "A1")` on span attributes that also
  hold durations);
- check all of it but some fields, dropped or replaced before the comparison, on a copy
  or in place: `dataclasses.replace(order, id=None)`, `order.model_copy(update={"id":
  None})`, `order.model_dump(exclude={"id"})`, `del` or `pop` of a key, a dict
  comprehension that filters keys out, `order.id = None`, or `Order(id=ANY, ...)` as
  the expected value;
- check how many items it, or each of its items, has instead of what they are (`assert
  len(parcels) == expected_count`, `assert parcels`, `assert all(len(t) == 2 for t in
  tables)`).

The violation is reported on the first assertion on that value.

Not a violation:

- one part, when that part is what the test names: `assert invoice.number == "42"` in a
  test of the invoice number, `assert payload["status"] == "paid"` in a test that the
  payload marks paid orders, `assert [p.sku for p in parcels] == ["A1", "B2"]` in a
  test of the parcels' order;
- one property that spans fields or items: `assert [(n.start_line, n.end_line) for n
  in scopes] == [(1, 3), (2, 3)]` in a test of the nodes' spans;
- the produced value compared once with an expected value, however the expected value
  is built: a constructor, a literal, `baseline.model_copy(update={"total": 2})`,
  `len(skus)` as the expected value of a produced count, a tuple of another object's
  fields as the expected value of a produced tuple;
- a produced scalar or bool asserted directly (`assert can_ship(shipment)`);
- the fields the test is about, when the value's type has no `__eq__`: a
  `subprocess.CompletedProcess`'s `returncode` and `stdout`, a plain class's fields, a
  Django model instance or SQLAlchemy row, an exception's `code`, a framework
  response's `status_code`; one `==` on such a value compares identity and checks
  nothing;
- identity checks on wiring: `assert cached.store is judges.store`; an `==` on the
  whole value can't state that two references are the same object.

### Expected values that don't pin the result

Violation: an assertion whose expected value accepts results the behaviour the test
names rules out: an order or bound instead of the value (`assert quote.total_cents >
0` in a test that shipping is charged), or a fragment of a string instead of the
string.

A fragment check is an assert that a substring is, or is not, inside a string: `assert
"42" in title`, `assert "draft" not in title`, `self.assertIn("42", title)`, or `in`
inside an expression the assert tests (`assert any("42" in line for line in lines)`).
The searched string can be any text, however the test gets it: a return value, an
f-string the code builds, `str(exc.value)` from `pytest.raises`, a test client's
`response.text`, `capsys.readouterr().out`, `caplog.text`, a file the code writes.

Supplied content is text another component provides that the test passes to the code
under test without spelling it out: a template the test loads, a file it reads, a
fixture document it opens. A code-built string stays code-built when the code's own
template, a module constant or another function of the program supplies the words.

A fragment check is a violation unless both hold: the searched string holds supplied
content the test passed in, and the fragment is a whole line the code under test
inserts into it, from a line start to a newline (`"Order number: ord-42\n"`). So these
are violations: a short value inside text the code builds (`assert "7" in
order_label(order)`), a word in an exception message, response body, log or captured
output, a `not in` check that a word is absent, a fragment of supplied content that is
not a whole inserted line.

The violation is reported on the assertion.

Not a violation: `in` on a list, tuple, set or dict (decided by the form above); `in`
outside an assert; an `==` comparison of the whole string, whatever it contains.

### Results that depend on the run

An uncontrolled input is a value or event the test doesn't set that can differ between
two runs of the same code:

- the real clock: `datetime.now()`, `datetime.utcnow()`, `date.today()`, `time.time()`,
  `time.monotonic()`;
- real randomness and generated ids: `random.*`, `uuid4()`, `secrets.*`, an unseeded
  `Faker()`;
- timing: a fixed `time.sleep()` or `asyncio.sleep()` that waits for a thread, process
  or task, a thread or task read before it is joined or awaited, a timeout the work
  must beat;
- order the language doesn't fix: iterating a set (`list(tags)`, `", ".join(tags)`
  where `tags` is a set), or files a directory lists (`os.listdir`, `Path.glob`,
  `os.walk`);
- the machine's environment: environment variables the test doesn't set, the current
  directory, the home directory, the hostname, the user, the locale, the network.

Controlled, so not uncontrolled inputs: a frozen or fake clock (`freeze_time`,
`time_machine.travel`, a `FakeClock` the test passes in), a seeded generator
(`random.Random(42)`), an id factory the test passes in, a value the test sets
(`monkeypatch.setenv`, `tmp_path`), `sorted(...)` of a set or listing, comparing sets
with `==`, `thread.join()` or `await task` before the assertion.

Violation: an assertion whose pass or fail can change with an uncontrolled input the
test or its fixtures read: `assert order.created_at == datetime.now()`;
`worker.start(); time.sleep(0.1); assert results == [...]`; `assert list(order.tags) ==
["gift", "rush"]` where `tags` is a set; `assert load_config().data_dir ==
Path("/home/ci/data")` where `load_config` reads the home directory; an expected value
that depends on which `random.choice` was picked. The violation is reported on the
assertion.

Not a violation: a `uuid4()` or `Faker().name()` for a field no assertion reads; an
expected value that reads the same input as the code (`assert report.path ==
Path.home() / "reports"`), so it holds on every machine.

### Expected identity values from shared constants

An identity value names one record or object: an id, a key, an order or invoice
number, a slug, a code, an email used to find a user. A shared constant is a name the
test reads but doesn't own: a module-level `UPPER_CASE` name, a class-level constant
read through `self` or the class, or a name imported from another module
(`tests.constants`, `conftest`).

Violation: an assertion that compares an identity value read from a shared constant,
directly or inside an expected value (`assert shipment.order_id == ORDER_ID`, `assert
invoice == Invoice(account_id=ACCOUNT_ID, ...)`, `self.ORDER_ID`, a constant read in a
`parametrize` list). The violation is reported on the assertion.

Not a violation: a literal in the test, a local the test assigns, a value read from a
record the test or a fixture it requests built (`assert shipment.order_id ==
order.id`); a constant that isn't an identity value (`MAX_RETRIES`); a shared constant
passed as an input that no assertion compares.

### Expected values computed by the code under test

The code under test is what the test's act calls, together with the production
functions, classes and allocators it calls to produce its result. A computed value is
one the code under test derives rather than receives: an id or number it allocates, a
key, slug, hash or token it derives, an ordering it sorts by, a total or price it
calculates.

Violation: a test helper or fixture that returns a value it gets by calling the code
under test, or the production function, method or class the code under test calls to
compute that same value: `return cache_key(product.sku, product.region)` when the cache
under test stores entries under `cache_key(...)`, `return
InvoiceNumberAllocator(db).peek_next()`, `return sorted(tasks, key=priority_key)` when
the scheduler under test orders by `priority_key`, `return article.build_slug()`. The
violation is reported on the helper's return.

Not a violation: a literal or a value the helper writes out; a value the helper
computes itself with plain code or the standard library
(`hashlib.sha256(body).hexdigest()`), even when production computes the same thing; an
input built with production code (a constructor, factory or creator that makes the
records, objects and collaborators the act uses).

## Violation

An assertion in the file under review that misses a break of the behaviour its test
names, or whose expected value the test doesn't state: parts, members, a count or a
derived value checked instead of a produced value that compares whole; fields dropped
before the comparison; a bound or a string fragment as the expected value; a result
that depends on the clock, randomness, timing, unordered iteration or the machine; an
identity value from a shared constant; or, in a helper or fixture, an expected value
computed by the code under test.
