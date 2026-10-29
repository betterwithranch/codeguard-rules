# In TypeScript

Anonymous results are a returned array of parts that answer different questions, typed
as a tuple (`[Row[], string[]]`). An object literal is named: its type names each
property, and the type checker checks every read.

## Violation

- `function parseCsv(text: string): [Row[], string[]] { ... return [rows, warnings]; }`.

## Not a violation

- `return { rows, warnings }` typed as `{ rows: Row[]; warnings: string[] }`.
- A React hook returning `[value, setValue]`, as `useState` does.
