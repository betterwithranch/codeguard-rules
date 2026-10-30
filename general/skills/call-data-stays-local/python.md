# In Python

Module-level state is a name assigned at the top of a module: a `list`, `dict`, `set`,
`defaultdict`, `Counter` or `deque` a function changes, or a name a function rebinds
through `global`. A shared instance is one assigned at module level, as a class
attribute (a dataclass or pydantic field's default included), as a parameter default,
or returned by a function under `@cache`, `@lru_cache` or a singleton decorator. A
Django view module, a Celery task module and a FastAPI router module live for the
process and serve every request or job.

## Violation

- A function that calls `_rows.clear()` and then `_rows.append(...)` on a module-level
  list, and returns the list.
- `global _current_order` set at the start of a function and read by helpers it calls.
- `checker = InvoiceChecker()` at module level, where `check()` does
  `self.problems.append(...)`.
- An `@lru_cache` factory returning an object whose methods add each call's results to
  an attribute.

## Not a violation

- `router = APIRouter()` with `@router.get(...)` routes, and a `REGISTRY` filled by
  decorators at import.
- `@functools.cache` on a pure function, and a module dict memoizing by its inputs that
  one function owns.
- `logger = logging.getLogger(__name__)`, `client = httpx.Client()`,
  `PATTERN = re.compile(...)`, `settings = Settings()` on a frozen pydantic model.
- `threading.Lock()` and `itertools.count()` at module level.
