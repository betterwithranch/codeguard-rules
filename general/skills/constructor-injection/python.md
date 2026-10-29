# In Python

The constructor is `__init__`, or the fields of a dataclass, attrs class or pydantic
model. A factory method is a `@classmethod` that returns `cls(...)`.

## Violation

- `def total_with_tax(self, invoice_id: str, rates: TaxRateProvider) -> Decimal` that
  calls `rates.rate_for(...)`.
- `async def refresh(self, client: httpx.AsyncClient) -> None` that calls
  `client.get(...)`.

## Not a violation

- `def __init__(self, repository: OrderRepository, rates: TaxRateProvider)`.
- `def total_cents(self, order: Order) -> int` that calls `order.lines()`.
- `def get(self, request: HttpRequest)` on a Django view.
- `def handle(self, event: Event, bus: MessageBus)` on a class implementing a handler
  `Protocol` that declares it.
