# In Python

Bundles include a project's `Settings`, `AppConfig` or pydantic `BaseSettings`,
`django.conf.settings`, `HttpRequest`, a FastAPI or Starlette `Request`, and context
classes such as `CheckoutContext` or `RequestContext`.

## Violation

- `def tax_cents(context: CheckoutContext) -> int` that reads only
  `context.subtotal_cents` and `context.region`, where `CheckoutContext` declares six
  fields.
- `def make_client(settings: Settings)` that reads only `settings.http_timeout`.

## Not a violation

- `def is_overdue(invoice: Invoice, today: date)` reading only `invoice.due_on`.
- `def get(self, request)` in a Django view, reading only `request.user`.
- A helper that passes `settings` on to `build_engine(settings)`.
