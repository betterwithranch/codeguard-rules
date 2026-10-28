# In Python

A function is a module function, a method, a `@staticmethod`, `@classmethod` or
`@property`, a nested function, or an `async def`, including a Django view, a DRF
action, a Celery task and a CLI command.

I/O in Python includes a Django queryset or manager (`Model.objects`, a related
manager's `.filter()` or `.count()`, `.save()`, `.delete()`), a SQLAlchemy session,
`requests` and `httpx`, `open()` and `pathlib` reads and writes, `boto3`, a Celery
`.delay()`, `send_mail`, `os.environ`, `date.today()`, `datetime.now()`, `time.time()`,
`random` and `uuid4()`.

## Violation

- A view or service function that loads a row through the ORM or a repository and works
  out inline from its fields whether an action is allowed: a `renew_loan` view that
  fetches the loan and compares its renewal count and due date before saving.
- A Django or SQLAlchemy model method that runs a query and decides from what it
  returns.
- A function that calls `date.today()` or `datetime.now()` to decide whether something
  has expired.
- A Celery task or management command that computes a domain amount or status inline
  and saves it.

## Not a violation

- A Django or SQLAlchemy model method or property that decides from the model's own
  fields, already loaded.
- A view, task or service method that reads, calls a decision function with what it
  read, and saves or sends its answer.
- `get_object_or_404`, `response.raise_for_status()`, a status-code check, and an
  `except` that retries a timeout.
- A pydantic model or DRF serializer validating a request's fields.
- `logger.info(...)` and metrics calls.
