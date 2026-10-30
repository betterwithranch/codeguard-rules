# In Python

## Violation

- `send_receipt(order.email, order)`, or `send_receipt(order, email=order["email"])`,
  where `send_receipt` is a function the program declares.
- `self._render(self._totals(invoice), invoice)`: a method on `self` that takes both.
- `Summary(total=total_of(lines), lines=lines)`, building a dataclass, pydantic model,
  attrs class or other class the program declares.
- `notify(*recipients_of(order), order)` or `notify({"to": order.email}, order)`: the
  derivation sits inside an unpacked argument or a dict, list or tuple literal.

## Not a violation

- A builtin, or a method of a builtin type: `dict.get(key, default_for(key))`,
  `getattr`, `min`, `max`, `print`, `str.format`.
- A standard-library or third-party function or class: `os.path.join`, `re.sub`,
  `json.dumps`.
- A method of a library object: a `logging` logger, an `httpx` or `boto3` client.
- `Service(repo=OrderRepository(session), session=session)`: the repository is a
  collaborator the service calls methods on.
