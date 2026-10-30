# In TypeScript

Data models are zod schemas, class-validator classes, and io-ts or valibot codecs.
Validators are zod's `refine`, `superRefine` and `transform` checks, valibot's `check`,
and class-validator decorators and custom constraints.

Request validation is the route handler, controller or service that handles a request
after its body is parsed.

## Violation

- `z.string().refine(async (sku) => (await prisma.product.count({ where: { sku } })) > 0)`.
- A class-validator custom constraint that reads `process.env` or a service.

## Not a violation

- `z.object({ start: z.date(), end: z.date() }).refine((v) => v.end > v.start)`.
- `z.enum(CURRENCIES)`, where `CURRENCIES` is a constant.
