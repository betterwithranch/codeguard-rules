# In TypeScript

Exempt fluent and pipeline APIs include array chains (`filter`, `map`, `reduce`),
promise chains, query builders (Prisma, Knex, Drizzle) and RxJS pipes. Optional-chained
reads of plain data (`config?.retry?.delayMs`) are not reaching through.

## Violation

- `order.customer.account.charge(order.totalCents)`.

## Not a violation

- `order.chargeCustomer()`.
- `items.filter((item) => item.active).map((item) => item.id)`.
- `response?.data?.items` on a parsed JSON payload.
