# In TypeScript

Checks are `if` statements that throw or return early, `assert` calls, `instanceof`
and `typeof` tests, and type assertions. Guarantees from a type include zod
refinements such as `positive()` and `min()`, and class-validator decorators on a
validated class.

`@typescript-eslint/no-unnecessary-condition` covers conditions the static types
guarantee; this rule covers guarantees from earlier code and validators.

## Violation

- `if (order.amount <= 0) throw new Error(...)`, where `order` came from
  `orderSchema.parse(...)` and the schema has `amount: z.number().positive()`.

## Not a violation

- `if (!user) throw new NotFound()` after `const user = users.get(id)`.
