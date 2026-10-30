# In Python

Context and settings objects include a project's `Settings`, `AppConfig` or pydantic
`BaseSettings`, `django.conf.settings`, `HttpRequest`, a FastAPI or Starlette `Request`,
and context classes such as `RequestContext`.

## Violation

- `def tax_cents(context: RequestContext, subtotal_cents: int) -> int` that reads only
  `context.region`, where `RequestContext` declares the user, a database session, a
  logger, the region, the locale and a clock.
- `def make_client(settings: Settings)` that reads only `settings.http_timeout`.

## Not a violation

- `def is_overdue(invoice: Invoice, today: date)` reading only `invoice.due_on`.
- `def get(self, request)` in a Django view, reading only `request.user`.
- A helper that passes `settings` on to `build_engine(settings)`.
