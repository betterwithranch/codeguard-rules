# In TypeScript

A handler is a `catch` block or a promise's `.catch(...)`. A fallback is a value after
`??` or `||`, a default in destructuring, or a value chosen when another is `undefined`
or `null`. A clamp is `Math.max` or `Math.min` forcing a computed value into a range. A
skipping condition is a `filter` callback, a `continue`, or a `flatMap` returning `[]`.

Required data in TypeScript includes a property the type declares without `?`, a zod
schema's required field, and an environment variable the program needs to reach a
service.

## Violation

- A `catch` that is empty, returns `undefined`, `null`, `[]` or a default, or only calls
  `console.error` and carries on.
- `.catch(() => undefined)` or `.catch(() => [])` on a call the caller relies on.
- `process.env.API_KEY ?? ""` or `|| ""` for a secret or a service URL.
- `?? 0` or `|| 0` on a property the type declares required.
- `Math.max(0, ...)` on an amount computed from the program's own records.
- `.filter(Boolean)` or `.filter((x) => x !== undefined)` dropping the results of a
  parse or lookup that failed, and returning the rest as if complete.

## Not a violation

- `catch (err) { throw new OtherError(..., { cause: err }); }`, and a `catch` that cleans
  up and rethrows.
- An Express or NestJS error handler sending an error response, and a CLI's top level
  setting `process.exitCode`.
- `searchParams.get("page") ?? "1"`, and `?? ` on a property the type declares optional.
