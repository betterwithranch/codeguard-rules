---
name: test-quality
description: Determinism, signal, mocking, assertion, helper, and fixture rules for Python test code.
---

# Test Quality

These rules apply to Python test code: test modules, shared fixture modules such as `conftest.py`, and test helper modules. They add to the general Python code-quality rules; they do not replace them.

## Tests are deterministic

A test must not pass or fail based on timing, ordering, or environment. Every assertion compares against a known, fully predictable value. Control unpredictable values (ids, timestamps, random numbers) with a fixture or a frozen clock; do not ignore them. A containment check (`in`, `<=`) written because the full result is unknown is a sign to pin the value instead.

## Every test has signal

A test must fail for some plausible bug in the project's own code. Ask: if this went red, would you fix the code or the test? If the test, delete it. Three defects have no signal:

- Tautology: the expected value is copied from the code under test's own declarations, so only editing the declaration can break it. Example: asserting a model's declared config equals a hand-written copy of the same config.
- Framework behavior: the test checks what the language, standard library, or a library guarantees, with no decision of the project under test. Examples: a field defaults to its declared default; a field without a validator accepts any value of its type; a model without custom serializers round-trips; every enum member is accepted.
- Redundancy: another test already covers the behavior. Examples: tests of a subclass that adds no logic; `isinstance` or protocol-conformance tests when other tests already use the object; tests that stub a collaborator and assert its stubbed output passes through unchanged.

Not tautology: a test of a constraint that answers to something outside the declaration. A test that a 0-100 percentage field rejects 150 has signal. A test that a label equals `"Frequency"` does not.

Do not find an item by a field value and then assert that same field. Assert the set of keys present, or find by one field and assert a different one.

Bad:

```python
assert next(i for i in result.items if i.sku == "A1").sku == "A1"
```

Good:

```python
assert {i.sku for i in result.items} == {"A1", "B2"}
```

## Integration tests catch a wiring bug

An integration or end-to-end test must catch a bug no unit test on either side of the seam can: a key two components must agree on, a reference one side must register, a step order the pipeline must keep. Running one more real type through already-tested generic code is a replay, not integration signal. If you cannot name the wiring bug the test alone catches, it is redundant. Needing to normalize framework noise out of the result is a sign the test sits at the wrong level.

## Mock only at the process boundary

`Mock`, `MagicMock`, and `patch()` are allowed only where code leaves the process: HTTP calls to third-party APIs, cloud SDK calls, services that need external credentials. Controlling time or randomness, and forcing hard-to-trigger error paths (network failure, full disk), are also allowed.

- The database is not a boundary. Use a real test database. Never mock queries, query results, or record objects.
- Never mock or patch collaborating classes, internal functions, factories, module-level callables, or private methods. Inject the dependency or use a real object.
- `monkeypatch.setattr` is `patch()` by another name. Reassigning a module function, constant, or attribute of the code under test so its real work does not run is not allowed. Example: `monkeypatch.setattr(report_module, "load_catalog", lambda: {...})`. Pass in a value the test builds instead.
- Patching settings, feature flags, or environment variables is allowed only when varying that value is what the test is about.
- Do not assert on the arguments one internal component passes to another.

Preference order: real object, then shared fake, then an inline stub implementing a protocol (only for framework contract tests), then a mock (only at the process boundary).

## Use real data, real parents, and real ids

- Do not replace real inputs with empty or dummy data to get past a failure. That failure is a production bug. Empty inputs are allowed only in wiring tests where the code under test provably does not use them.
- When production has one creator for a record (a service, a planner, a repository `create`), seed test data through that creator or a thin helper that calls it. Do not hand-write a parallel insert path in shared fixtures.
- Do not give a child record a fresh `uuid4()` foreign id that points at a parent that was never created. Create the parent.
- Do not put a fixed UUID or other id constant in a fixture unless the code under test correlates on that id and the matching object exists or is asserted. If the id is only there because a wide setup object requires it, narrow the setup to the real inputs.

## Extend shared fakes by configuration

A shared fake stands in for one layer. Configure it and assert on its in-layer state in the test body. Do not subclass a shared fake to override a method so that the override asserts, or queries a different subsystem. Signs: an overridden method containing `assert`, a database query, or a list that exists only to record that the override ran. A subclass that only configures the fake (canned responses, queue setup) is fine.

Bad:

```python
class CheckingFakeQueue(FakeQueue):
    def enqueue(self, queue_name, message):
        assert self._db.count_orders(message["order_id"]) == 1
        return super().enqueue(queue_name, message)
```

Good:

```python
queue = FakeQueue()
OrderSubmitter(queue).submit(order)
assert [m.body for m in queue.drain("orders")] == [{"order_id": order.id}]
```

## Build through the production factory

When a production factory or builder assembles an object graph, the test calls that factory. Inject a test double for the boundary collaborator through a constructor parameter. Do not rebuild the same graph by hand in a fixture. If the factory does not accept the double, the fix is a constructor parameter with a production default, not a bypass.

The same holds for derivation. If the factory computes intermediate values from its input, build the factory's input and call the factory. Do not re-derive those values in the fixture to construct the output type directly.

## Reuse shared fakes and helpers

Do not define an inline stub, fake, or helper that duplicates one already in a shared fixture module or test utility module. Do not redefine a fixture the shared fixture module already provides. Import types from their defining module, not from a shared fixture module.

## Prefer `==` over `in`

Use exact equality when the value is deterministic.

```python
assert result.name == "Invoice 42"
assert result.lines == [expected_line]
assert result.totals == {"net": 100, "tax": 20}
```

`in` is allowed only when all of these hold:

- The asserted fragment is exact and complete (a whole line, token, or value the code under test produces), not a loose substring.
- It sits inside a larger value whose content another component authors (a template, a loaded text file, a separate formatter). A unit that only joins sections does not own their content.
- Asserting the whole value with `==` would pin that other component's content.

Check: breaking the logic under test fails the assertion, and editing the unrelated component does not.

## Assert whole result objects

Build the expected object and compare once: `assert result == Invoice(number="42", total=120)`. Do not assert one field and leave the siblings unchecked.

- When the result type has `__eq__`, separate `==` lines for each field are a violation even if they cover every field today. They miss fields added later.
- A bare `len()` check, or `len(x) == 1` followed by checks on `x[0]`, is incomplete. Assert the full collection: `assert [i.sku for i in items] == ["A1", "B2"]`.
- Field-by-field checks are correct only when equality is impossible (no `__eq__`, generated keys, timestamps) or the result is a scalar. Then assert every observable field. Do not compare a tuple of fields; it drops the field names.

## Do not normalize the result before asserting

Do not rebuild the actual result with `dataclasses.replace`, a copy-with-update, a dump that excludes fields, or a comprehension that strips fields before `==`. Each removed field is unguarded. Assert the noisy field's meaningful part directly (`assert error.context["input"] == "abc"`) and assert the rest of the object normally.

## Test names match assertions and vocabulary

- A test name states what the assertion proves, not how the code works.
- Use the production code's terms. No synonyms (inject vs resolve, build vs assemble).
- Do not coin a phrase for a condition that already has a name. Use the production symbol or the standard term (`test_empty_result_...`, not `test_no_reaction_...`).

## Helpers set up; they never perform the act

A test helper or fixture builds inputs, collaborators, and records. It must not take over the act the test verifies. Three forms cross the line:

- Computing a value production already computes (an id, key, hash, ordering) by calling the same builder or allocator. A helper named after one scenario or domain is a sign. Get the value from the production path, or mock at a higher seam so the test never has to predict it. If the value must appear in a mock, build it in the test body and bind it to a named variable.
- Ending by calling a method or reading an attribute on the object it just built, and returning that instead of the object: `return InvoiceMapper(rules).map(raw)`, `return build_runtime(...).context`. This applies even when the method is not the one under test. Calling methods while building (builder chains, constructors) is fine. Split into a helper that returns the built object and a separate action-named helper, or an inline line in the test.
- An action helper that takes a result, asserts on it, drives the next workflow step, and returns the new result. Inline the step in the test body. Simulate out-of-band actors (a queue worker, a callback) inline by reading the boundary fake and running the real component. Drop repeated assertions a unit test already owns.

Exception: calling a production function inside the expected value is fine when all hold: the value is a deterministic output field computed from other fields asserted in the same expected object; the code under test hands that computation to a collaborator; and that collaborator's function has its own test built another way.

Bad:

```python
def submit_and_resume(workflow, result):
    assert result.status == Status.WAITING
    return workflow.resume(result.job_id)
```

Good:

```python
result = workflow.resume(result.job_id)
```

## No wrapper or projection fixtures

- Do not write a fixture or helper whose body only calls one constructor or factory with default arguments. Inline the call. Keep it only if it applies real, non-default configuration.
- Do not write a fixture that builds objects, calls selection or filter methods on them, and returns the projection. Put the projection call in the test body, or move it into production code that owns the concept.

## Arrange, act, and assert stay in the test body

- Construct the system under test in the test body. Fixtures supply its collaborators and inputs. A test parameter that is the object the test acts on is a violation.
- A fixture supplies a thing. It must not perform arrange actions: starting a workflow or job, advancing a clock (`sleep`, `freeze_time` ticks, skips), or making the calls that drive the system into its precondition. It must never perform the act or hold assertions. This holds even when the fixture returns a real object.
- A setup fixture used by only one test hides that test's arrange. Inline it.
- A setup fixture is allowed only when it is shared by more than one test and sets up ambient environment (workers, queues, feature flags, registries), not one scenario.
- An arrange too large to read inline is a design problem in the code under test (a missing seam, an uninjected collaborator, too many responsibilities). Do not hide it in a fixture.

## Fixture shape

- A fixture returns one object, never a tuple.
- Keep setup-only fixtures (they establish a condition) apart from data fixtures (they return a value).
- Construct test data in fixtures, not in module-level constants. Flag a module-level `SCREAMING_SNAKE` value that constructs domain objects or stands in for an id a test asserts on. Plain opaque scalars (a token string) are exempt.
- A test that asserts on an identity value owns that value; it does not read it from a shared constant.

## Construction helper parameters

- Declare typed parameters. A `**kwargs` or `**overrides` parameter is allowed only when passed untouched to one typed target.
- Do not `.pop()` keys out of `**kwargs` or raise `TypeError` for unexpected keys by hand.
- No alternative-input branching: do not accept two parameters for the same value and pick between them.
- No test-only bundle types (`...Setup`, `...Resources`) and no setting attributes on an object after it is built.
- Do not give a test-only shape a production-sounding name.
- Remove unused parameters, and do not re-pass a value equal to the callee's default.

## Test isolation

- Revert global state and release resources after each test.
- Do not keep mutable state in class attributes shared across test methods.
- A session-scoped fixture must return an immutable resource.
- An `autouse` fixture's scope must match the cleanup it does.
- Delete empty or placeholder fixtures.

## Async coordination

Do not coordinate async tests with `asyncio.sleep()` or `time.sleep()`. Wait on an `asyncio.Event`, `Condition`, or similar primitive.
