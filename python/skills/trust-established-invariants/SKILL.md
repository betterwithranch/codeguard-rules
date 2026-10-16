---
name: trust-established-invariants
description: Trust established invariants
---

# Trust established invariants

Do not re-check a fact already guaranteed upstream. Such a guard can never fire. The guarantee may come from:

- Dispatch routing: a registry already chose this handler by the value's tag.
- An enclosing branch: an outer check already narrowed the value.
- A collaborator's return contract: a result that is non-empty only for one variant.

Narrow at the contract instead. Make the handler generic over its variant so its type carries the guarantee, or move the dependent branch inside the check that establishes it. Put the one `Any` at the registry dict, not in handler bodies.

Bad:

```python
class RefundHandler:
    def handle(self, request: PaymentRequest) -> PaymentResult:
        if not isinstance(request.payload, RefundPayload):
            raise TypeError("RefundHandler requires a refund payload")
        ...
```

Good:

```python
class RefundHandler:
    def handle(self, request: PaymentRequest[RefundPayload]) -> PaymentResult:
        ...
```

Validation of input the code received (an unknown key or id) is not covered by this rule.
