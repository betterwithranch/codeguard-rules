---
name: no-internal-call-assertions
description: A test never asserts on the calls one of the program's components makes to another
---

# No assertions on internal calls

A test checks what the code under test produces, never which calls it makes to
another part of the same program.

A recorded call is what a mocking tool records about the calls a test double
receives, read through `assert_called`, `assert_called_with`,
`assert_called_once_with`, `assert_any_call`, `assert_has_calls`, `assert_not_called`,
the `assert_awaited` family, `call_args`, `call_args_list`, `mock_calls`,
`method_calls`, `call_count`, `called`, or a `mocker.spy`. A hand-written fake's state
(the messages a `FakeQueue` holds, a fake mailer's outbox) is not a recorded call.

The callee is the function, method or object the double stands in for. It is internal
when it is the program's own code: a function, class, method or object defined in the
program's packages, including its own wrapper around an outside service. It is outside
when it leaves the process: an HTTP client, a third-party or cloud SDK, the clock.

## The test

For each assertion on a recorded call, ask: is the callee internal or outside?

Outside, so not a violation:

- `session.post.assert_called_once_with("https://api.example.com/charges", json=body)`
  where `session` stands in for a `requests.Session`;
- `s3_client.put_object.assert_called_once_with(Bucket="reports", Key="2026-03.csv",
  Body=ANY)` where `s3_client` stands in for a `boto3` client.

Not a recorded call, so not a violation: `assert invoice.total == Decimal("108.00")`,
`assert queue.messages == [{"order_id": "A-1"}]`, `assert mailer.outbox == [...]`.

Internal, so a violation:

- `calculate_tax.assert_called_once_with(Decimal("100.00"), "CA")` after patching
  `billing.invoices.calculate_tax`;
- `assert repository.save.call_args == call(invoice)` where `repository` stands in for
  the program's `InvoiceRepository`;
- `spy = mocker.spy(OrderService, "_reserve_stock")` then `assert spy.call_count == 1`;
- `notifier.notify.assert_not_called()` where `notifier` stands in for the program's
  `Notifier`.

## Violation

An assertion on a recorded call to one of the program's own functions, methods or
objects: whether it was called, how often, or with which arguments.
