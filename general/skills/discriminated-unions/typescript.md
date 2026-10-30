# In TypeScript

Parsed unions are zod, valibot and io-ts unions of object schemas. The discriminator is
named with `z.discriminatedUnion("kind", [...])` or `v.variant("kind", [...])`. A tag
is declared `kind: z.literal("card")` or `kind: v.literal("card")`.

## Violation

- `z.union([cardSchema, bankSchema])` or `v.union([cardSchema, bankSchema])`, where
  both are object schemas.
- A variant of `v.variant("kind", [...])` with no `kind` field, a `kind` of
  `v.string()`, or the same `v.literal` as another variant.

## Not a violation

- `z.discriminatedUnion("kind", [cardSchema, bankSchema])`, each variant with its own
  `z.literal` tag.
- `z.union([z.string(), z.number()])`, and `cardSchema.nullable()`.
- A TypeScript union type of classes the program builds and narrows with `instanceof`.
- Forms zod refuses when the schema is built or first parses: a `z.discriminatedUnion`
  variant whose tag isn't a `z.literal` or that has no tag field, and two variants with
  the same tag value. valibot's `v.variant` refuses none of these.
