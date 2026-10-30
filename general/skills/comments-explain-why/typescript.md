# In TypeScript

Comments are `//` and `/* */` comments. `// eslint-disable`, `// @ts-expect-error`
and `// prettier-ignore` are directives. A project that requires TSDoc on every
exported item keeps it as a convention; then judge only its inline comments and the
doc comments of items that aren't exported.

## Violation

- `count++; // increment the count`.
- `/** Gets the user. */` on `function getUser(id: string): User`.

## Not a violation

- `const BATCH = 50; // the carrier API rejects more than 50 parcels per request`.
