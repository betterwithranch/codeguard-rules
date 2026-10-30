# In Python

A handler is an `except` or `except*` clause, or `contextlib.suppress`. A fallback is
the second argument of `dict.get`, `os.environ.get`, `os.getenv` or `.pop`, the third of
`getattr`, a literal after `or`, or a value chosen in a conditional expression or an
`if` statement when another `is None`. A clamp is `max` or `min` forcing a computed value
into a range. A skipping condition is a comprehension's `if`, a loop's `continue`, an
`if` in a loop that appends, adds or yields only some items, or `filter`.

Required data in Python includes a dataclass or pydantic field with no default, a Django
model field without `null=True` or `blank=True`, and a setting the module reads at start
up to reach a service.

## Violation

- `except Exception:` or a bare `except:` whose body is `pass`, `continue`, a
  `return None`, `return []` or `return 0`, or a `logger.exception(...)` followed by
  carrying on.
- `contextlib.suppress(Exception)` around work the caller relies on.
- `os.environ.get("...", "")` for a secret or a service URL, and `settings.get(...)` with
  a default for a value the program can't run without.
- `or 0`, `or ""` or `or []` on a field the model declares required.
- `max(0, ...)` or `min(..., limit)` on an amount computed from the program's own
  records.
- A list comprehension or loop that drops the rows that failed to parse or have a
  `None` in a required field, and returns the rest.

## Not a violation

- `except SomeError as err: raise OtherError(...) from err`, and `except ...: cleanup();
  raise`.
- `except` of a specific error around a retry loop.
- A Django view's or FastAPI handler's exception handler returning an error response,
  and a Click or argparse `main` exiting non-zero.
- `suppress(FileNotFoundError)` around `os.remove` of a temporary file.
- `request.GET.get("page", 1)`, `os.environ.get("LOG_LEVEL", "INFO")`.
- `config["database_url"]`, which raises `KeyError` when it's missing.
