# In Python

Module-level state is a name assigned at the top of a module: a `dict`, `list`, `set`,
`defaultdict`, `Counter` or `deque` that functions assign into or call a mutating method
on, or a name functions rebind with `global`. Another module writes it with
`module.name = ...` or `module.container[...] = ...`.

## Violation

- `_rates: dict[str, Decimal] = {}`, filled by `reload_rates()` and changed by
  `set_rate(code, rate)`.
- `global _maintenance` in both `start_maintenance()` and `apply_settings(settings)`.
- `config.RETRY_LIMIT = 10` in a function in another module.

## Not a violation

- `_cache: dict[str, User] = {}`, written only by `get_user(user_id)`, which memoizes.
- `@register("csv")` decorators filling `_exporters` at import.
- `_lock = threading.Lock()`, and `REQUESTS = Counter("requests_total", ...)`.
