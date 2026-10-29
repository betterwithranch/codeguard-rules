# In Python

State changes include assigning `self.x` or a parameter's attribute, `.append`,
`.add`, `.update`, `.pop` and `del` on a collection that outlives the call, `.save()`,
`.delete()`, `.update()` and `session.add` on ORM objects, and writes to files, caches
and queues.

The idioms exempt as take-and-return operations include `pop`, `popitem`,
`setdefault`, `get_or_create`, and `next` on an iterator.

## Violation

- `def unread_count(self, user) -> int` that marks the user's messages as read and
  returns how many there were.

## Not a violation

- `def create_order(...) -> int` that saves an order and returns its id.
- `def with_header(self, name, value) -> "RequestBuilder"` that returns `self`.
