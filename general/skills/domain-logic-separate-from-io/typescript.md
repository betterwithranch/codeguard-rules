# In TypeScript

A function is a function declaration, an arrow function or function expression bound to
a name, a class method, a getter, or an `async` function, including an Express or
NestJS handler and a React hook's callback.

I/O in TypeScript includes `fetch` and axios, an ORM or query builder (Prisma, TypeORM,
Drizzle, Knex), `fs`, `process.env`, `localStorage`, a queue or email client,
`Date.now()`, `new Date()` with no argument, `Math.random()` and
`crypto.randomUUID()`.

## Violation

- A request handler that awaits a query and works out inline from the rows whether an
  action is allowed, or what it costs, before responding.
- A service method that awaits a client of another system and decides from its answer.
- A function that reads `Date.now()` or `new Date()` to decide whether something has
  expired.
- A function that decides a status inline and writes or sends it.

## Not a violation

- A handler or service method that awaits its reads, calls an imported decision
  function with what it read, and writes or sends the answer.
- `if (!response.ok)`, a status-code check, and a `catch` that retries a timeout.
- zod or class-validator parsing a request body.
- `console.log` and a logger's calls.
- A class method or React render that decides from its own fields, props or state.
