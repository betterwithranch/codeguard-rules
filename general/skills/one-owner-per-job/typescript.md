# In TypeScript

A type is a class, including a NestJS service or controller, or an Angular service. Its
public methods are those not marked `private` or `protected` and not named with `#`.

## Violation

- A `CartService.total(cart)` that sums line prices and tax, where `CartPricing.total`
  in `cart/pricing.ts` already does.
- A `ReminderService.dueDate(invoice)` working out the due date `InvoiceTerms.dueDate`
  already works out.

## Not a violation

- `CartService.total(cart)` calling `this.pricing.total(cart)` and adding a fee.
- Classes that implement one interface, each its own way.
- A `private` or `#` method, called by its own class's public methods.
