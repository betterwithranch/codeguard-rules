# In TypeScript

## Violation

- `notify(order.email, order)` or `notify(order["email"], order)`, where `notify` is a
  function the program declares.
- `this.render(this.totals(invoice), invoice)`: a method on `this` that takes both.
- `new Summary(totalOf(lines), lines)` for a class the program declares.
- `notify({ to: order.email }, order)` or `notify(...recipientsOf(order), order)`: the
  derivation sits inside an object or array literal or a spread argument.

## Not a violation

- The runtime's functions and methods: `map.get(key) ?? defaultFor(key)`,
  `Math.max`, `JSON.stringify`, `console.log`.
- A function or class from an npm package: lodash, date-fns, zod.
- A method of a library object: a pino or winston logger, an AWS SDK or Prisma client.
- `new Service(new OrderRepository(db), db)`: the repository is a collaborator the
  service calls methods on.
