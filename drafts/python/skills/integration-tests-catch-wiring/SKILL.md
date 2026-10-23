---
name: integration-tests-catch-wiring
description: A test in an integration or end-to-end suite runs two or more of the program's components together, so a disagreement between them fails it
---

# Integration tests cross a seam

A test in an integration or end-to-end suite runs at least two of the program's
components together, so a disagreement between them fails it.

A component is a part of the program with its own job that a unit test could cover
alone: a view or route handler, a serializer, a service, a repository, a model and its
table, a queue producer or consumer, a pipeline step, a registry, the app's settings.

A seam is where one component hands data or control to another: a URL route to its
view, a view to its serializer, a service to the repository that stores what it built,
a producer to the consumer reading the same queue, a registration to the lookup that
finds it, one pipeline step to the next, a setting to the code that reads it. A
disagreement at a seam is a key, route, name, registration, setting or step order the
two sides don't share.

## The test

For each test, ask: does it observe a result that depends on one component receiving
what another passed, so a disagreement at that seam would fail it?

Crosses a seam, so not a violation:

- `client.post("/orders/", data)` through the app's test client, then reading the
  stored `Order`;
- publishing an event to the app's queue and asserting the consumer's side effect;
- running a pipeline's steps end to end and comparing the final output;
- a service that saves through a real repository, then reading the row back from the
  database.

Calls one component and stops there, so a violation:

- calling a pure function and asserting its return (`parse_amount("1,000.50")`);
- validating data with one serializer or pydantic model and asserting its errors;
- calling one model method or one class's method on objects the test built, with no
  other component of the program in the path.

## Violation

A test in an integration or end-to-end file whose result depends on one component of
the program alone.
