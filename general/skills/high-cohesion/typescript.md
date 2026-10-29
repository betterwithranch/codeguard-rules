# In TypeScript

Public classes are exported classes, interfaces, type aliases and enums.

Exempt modules: barrel `index.ts` files that re-export, and framework route files such
as Next.js `page.tsx` and `route.ts`.

## Violation

- An exported `RetryBackoffPolicy` class with a `delay()` method in
  `notifications/dispatcher.ts` beside `NotificationDispatcher`.

## Not a violation

- `payment.ts` exporting `CardPayment`, `BankPayment` and `type Payment = CardPayment |
  BankPayment`.
