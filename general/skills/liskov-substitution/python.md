# In Python

A base is a class named in another class's bases, an `ABC`, or a `Protocol` a class
names as a base. A method the base leaves for subclasses has `@abstractmethod`, is a
`Protocol` member, or has a body of `...`, `pass` or `raise NotImplementedError`.

## Violation

- `def refund(self, payment, amount): raise NotImplementedError("refunds not
  supported")` where the base's `refund` does the refund.
- `def export(self, rows, include_header=True):` whose body never reads
  `include_header`, where the base's `export` writes the header only when it's true.
- `def schedule(self, job, at):` that returns `None` for a past `at` the base runs at
  once, or that raises `ValueError` for it.
- `def find(self, key): return None` where the base's `find` looks the key up.
- `def close(self): pass` where the base's `close` releases its connection.

## Not a violation

- `def save(self, record): self._audit(record); super().save(record)`.
- An override typed `def parse(self, raw: str | bytes)` over a base's `parse(self, raw:
  str)`.
- A method implementing an `@abstractmethod`, a `Protocol` member, or a base method
  whose body is `raise NotImplementedError`.
- A subclass of a class imported from another module.
