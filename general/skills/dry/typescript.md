# In TypeScript

A function is a function declaration, an arrow function or function expression bound to
a name, a class method, a getter, or an `async` function. A module of the program is one
the file imports by a relative path or the project's own path alias; packages from
`node_modules` are not the program.

## Violation

- A function whose body repeats another's steps: `renewalPenalty(rate, days)` doing
  what `lateFee(days, rate)` does, line for line.
- A function outside a class that repeats the steps of a method the class already has.
- Calls that chain a process's stages outside it: `store(clean(readRows(path)))` beside
  an `ingest(path)` that runs those three stages in that order.
- A union of string literals, an array, an object's keys or an `enum` that lists
  exactly another set's members: `type FormatName = "csv" | "json"` written out beside
  `const FORMATS = { csv: writeCsv, json: writeJson }`.
- A second `interface`, `type` or schema (zod, valibot, io-ts) with the fields of one
  already modelling the same message, file or response, such as an `interface` written
  out beside a zod schema of the same response.

## Not a violation

- A call to the representation, with or without steps around it.
- A type or collection derived from another: `keyof typeof FORMATS`,
  `(typeof NAMES)[number]` from an `as const` array, `z.infer<typeof Schema>`,
  `Object.keys(FORMATS)`, `Pick<>` and `Omit<>` of an existing type.
- Overload signatures, an `interface`'s members implemented by a class, and `abstract`
  method declarations.
- What a framework asks each component or class to declare: an Angular `@Component`
  decorator's settings, a NestJS module's providers, a React component's props type.
- A database entity type and an API response type with the same fields, mapped where
  they meet.
