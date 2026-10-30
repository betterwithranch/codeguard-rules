# In TypeScript

Creation methods include `static` methods that return `new` instances of their class,
and functions named `create...`, `make...`, `build...` or `from...`.

Framework-chosen names include a Next.js route's `GET` and `POST`, a NestJS
controller's decorated handlers, and React lifecycle methods.

## Violation

- `function handleItems(orders: Order[])` that refunds each cancelled order.
- `static forCheckoutPage(...)` on `Order`.

## Not a violation

- `function refundCancelled(orders: Order[])`.
- `static fromCartItems(...)` on `Order`.
