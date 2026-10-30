# In TypeScript

A class's base is the class after `extends`; the interfaces after `implements` are not
inheritance of code.

## Violation

- `class InvoiceNotifier extends EmailClient` whose methods call `this.send(...)` to mail
  invoices.
- `class CheckoutController extends RetryHelper` that inherits only to call
  `this.withRetries(...)`.

## Not a violation

- `class SavingsAccount extends Account` that overrides how interest is earned.
- `class PaymentDeclinedError extends Error`, and framework bases such as NestJS or
  Angular classes the framework requires.
- `class FileStore implements Storage`.
