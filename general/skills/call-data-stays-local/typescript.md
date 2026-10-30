# In TypeScript

Module-level state is a `let` or a container (`Array`, `Map`, `Set`, object) declared
at the top of a module, which every importer shares. A shared instance is one created
at module level and exported or used by the module's functions, held in a `static`
field, or returned by a memoized factory. A Node server process runs every request in
one module instance, at the same time.

## Violation

- A request handler that sets a module-level `let currentUser` and helpers that read it.
- A function that empties a module-level array, pushes each call's results into it and
  returns it.
- `export const cart = new Cart()` at module level, where `add()` pushes the item onto
  `this.items`.
- A `static` field on a service class that a method writes each request's data into.

## Not a violation

- `const app = express()` with routes added at start-up, and a registry filled at
  import.
- A `Map` cache keyed by its inputs that one function owns.
- `export const db = new PrismaClient()`, `const logger = pino()`, an axios instance.
- React state, a store library's store, and AsyncLocalStorage, which keep each use's
  data apart by design.
