---
name: deterministic-tests
description: No assertion in a test depends on a value the test doesn't control, such as the real clock, randomness, timing, set order or the machine's environment
---

# Tests are deterministic

A test's result depends only on the code under test and the inputs the test sets.

An uncontrolled input is a value or event the test doesn't set that can differ between
two runs of the same code:

- the real clock: `datetime.now()`, `datetime.utcnow()`, `date.today()`, `time.time()`,
  `time.monotonic()`;
- real randomness and generated ids: `random.*`, `uuid4()`, `secrets.*`, an unseeded
  `Faker()`;
- timing: a fixed `time.sleep()` or `asyncio.sleep()` that waits for a thread, process
  or task, a thread or task read before it is joined or awaited, a timeout
  (`wait_for(..., timeout=0.1)`) the work must beat;
- order the language doesn't fix: iterating a set (`list(tags)`, `", ".join(tags)`
  where `tags` is a set), or files a directory lists (`os.listdir`, `Path.glob`,
  `os.walk`);
- the machine's environment: environment variables the test doesn't set, the current
  directory, the home directory, the hostname, the user, the locale, the network.

Controlled, so not uncontrolled inputs: a frozen or fake clock (`freeze_time`,
`time_machine.travel`, a `FakeClock` the test passes in), a seeded generator
(`random.Random(42)`, `Faker().seed_instance(7)`), an id factory the test passes in, a
value the test sets (`monkeypatch.setenv`, `tmp_path`), `sorted(...)` of a set or
listing, comparing sets with `==`, `thread.join()` or `await task` before the
assertion.

## The test

For each uncontrolled input a test or its fixtures read, ask: can it change whether an
assertion in the test passes?

Not a violation:

- a `uuid4()` or `Faker().name()` used for a field no assertion reads;
- `assert order.tags == {"gift", "rush"}`: set equality ignores order;
- `assert sorted(os.listdir(tmp_path)) == ["a.csv", "b.csv"]`;
- `with freeze_time("2026-03-01"): ...` then `assert invoice.issued_on == date(2026, 3, 1)`;
- `assert report.path == Path.home() / "reports"`: the expected value reads the same
  input as the code, so it holds on every machine.

A violation:

- `assert order.created_at == datetime.now()`;
- `worker.start(); time.sleep(0.1); assert results == [...]`;
- `assert list(order.tags) == ["gift", "rush"]` where `tags` is a set;
- `assert load_config().data_dir == Path("/home/ci/data")` where `load_config` reads the
  home directory: the expected value holds on one machine only;
- `assert load_config().mode == "live"` where `load_config` reads `PAYMENTS_MODE` from
  the environment and the test doesn't set it;
- `sku = random.choice(skus)` and an assertion whose expected value depends on which
  `sku` was picked.

## Violation

A test whose assertion can pass on one run and fail on another run of the same code,
because what it checks depends on an uncontrolled input.
