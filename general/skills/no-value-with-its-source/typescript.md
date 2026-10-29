# In TypeScript

## Violation

- `notify(order.email, order)` where `notify` is a function the program declares.
- `new Summary({ total: totalOf(lines), lines })` for a class the program declares.

## Not a violation

- `map.get(key) ?? defaultFor(key)`: `Map.get` is the runtime's.
- `new Service(new OrderRepository(db), db)`: the repository is a collaborator.
