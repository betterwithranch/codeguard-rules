# In TypeScript

Parsed unions are zod, valibot and io-ts unions of object schemas. The discriminator is
named with `z.discriminatedUnion("kind", [...])` or `v.variant("kind", [...])`. A tag
is declared `kind: z.literal("card")`.

## Violation

- `z.union([cardSchema, bankSchema])`, where both are `z.object`s.
- A variant of `z.discriminatedUnion` whose tag is `z.string()`.

## Not a violation

- `z.discriminatedUnion("kind", [cardSchema, bankSchema])`, each variant with its own
  `z.literal` tag.
- `z.union([z.string(), z.number()])`.
- A TypeScript union type of classes the program builds and narrows with `instanceof`.
