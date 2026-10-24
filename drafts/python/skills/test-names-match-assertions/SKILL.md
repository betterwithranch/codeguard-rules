---
name: test-names-match-assertions
description: A test's name claims only outcomes the test's assertions check
---

# Test names match their assertions

A test's name states only outcomes the test checks.

A test name's claim is what the name says the code does: an outcome
(`test_refund_restores_stock` claims stock is restored), a value
(`test_total_includes_tax`), an error (`test_rejects_negative_quantity`), or a
mechanism (`test_reads_rates_from_cache` claims the cache is read). Words that only
set the scene (`_for_guest_checkout`, `_when_cart_is_empty`) describe the input, not a
claim.

An assertion checks a claim when the test asserts the claimed outcome: an `assert`, a
`pytest.raises`, a `self.assert...` call, or a helper the test calls that asserts it.

## The test

For each claim in a test's name, ask: does an assertion in the test check it?

Not a violation:

- `test_cancel_sets_cancelled_status` asserting `order.status == OrderStatus.CANCELLED`;
- a name claiming one outcome, with assertions on that outcome and others;
- `test_rejects_negative_quantity` using `with pytest.raises(InvalidQuantity):`.

A violation:

- `test_refund_restores_stock` asserting only `refund.status == "refunded"`;
- `test_sends_confirmation_email` with no assertion on any email;
- `test_reads_rates_from_cache` asserting only the converted amount;
- `test_rejects_negative_quantity` asserting `line.quantity == 0`.

## Violation

A test in the file under review whose name claims an outcome, value, error or mechanism
that none of its assertions check.
