# In TypeScript

Boundaries are a BullMQ or Bee queue's `add`, a broker client's `publish` or `send`, and
starting a Temporal workflow or activity. Stored records are ORM entities (Prisma,
TypeORM, Sequelize, Mongoose) and objects a repository loads, and spreads or JSON copies
of all their fields.

## Violation

- `await receipts.add("send-receipt", { order })`, where `order` came from
  `prisma.order.findUniqueOrThrow(...)`.
- `await queue.add("reindex", { ...product })`.

## Not a violation

- `await receipts.add("send-receipt", { orderId: order.id })`, with the worker loading
  the order.
- `await broker.publish("order.placed", { orderId: order.id, totalCents: order.totalCents })`.
