# In TypeScript

A switch is a `switch` or an `if`/`else if` chain on a discriminated union's tag
(`switch (x.kind)`) or on an `enum`'s members; an `if`/`else if` chain of `instanceof`
checks; and an object or `Map` keyed by tags, enum members or classes that a function
indexes with the value's kind.

A `switch` or chain is checked complete when its last branch passes the value to a
`never` check (`default: return assertNever(x)`, or
`const unreachable: never = x`), which the compiler rejects if any kind can reach it. An
object typed `Record<Kind, T>` for the union's tag or enum is checked complete: the
compiler demands every key. A `default:` or final `else` that returns, throws or logs for
whatever is left, a `switch` that falls out after its last `case`, and an object typed
`Partial<Record<Kind, T>>` or `Record<string, T>` are not.

## Violation

- A function gaining a `switch` on a union's tag with a `default:` that returns a
  fallback, beside another such `switch` on the same union.
- An `instanceof` chain over the same classes as another chain in the module, ending in
  a final `return`.
- An `if`/`else if` chain on an `enum`'s members repeating the members another chain in
  the module chooses among.

## Not a violation

- Classes that each implement the interface's method the code calls.
- Several `switch` statements on one union's tag, each ending in a `never` check.
- Tables typed `Record<Kind, T>`, one per behaviour.
- A parser or zod schema (`z.discriminatedUnion`) that reads a payload's tag and builds
  the matching variant.
