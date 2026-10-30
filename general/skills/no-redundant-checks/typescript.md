# In TypeScript

Checks are `if` statements that throw or return early or `continue` or `break` a loop,
`assert` calls, and calls to assertion functions (`asserts condition`), such as
`invariant`. Their condition may be a comparison or an `instanceof` or `typeof` test. A
type assertion (`value as T`) and a ternary stop nothing, so they aren't checks.
Guarantees from a type include zod refinements such as `positive()` and `min()`, and
class-validator decorators on a class instance that `validate` or `validateOrReject`
has passed.

`@typescript-eslint/no-unnecessary-condition` covers conditions the static types
guarantee; this rule covers guarantees from earlier code and validators.

## Violation

- `if (order.amount <= 0) throw new Error(...)`, where `order` came from
  `orderSchema.parse(...)` and the schema has `amount: z.number().positive()`.

## Not a violation

- `if (!user) throw new NotFound()` after `const user = users.get(id)`.
