# In TypeScript

Framework-chosen names include a Next.js route's `GET` and `POST`, a NestJS
controller's decorated handlers, and React lifecycle methods.

## Violation

- `function handleItems(orders: Order[])` that refunds each cancelled order.

## Not a violation

- `function refundCancelled(orders: Order[])`.
