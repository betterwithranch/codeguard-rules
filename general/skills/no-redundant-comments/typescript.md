# In TypeScript

Comments are `//` and `/* */` comments. `// eslint-disable`, `// @ts-expect-error`
and `// prettier-ignore` are directives. A doc comment is a `/** */` comment.
sonarjs's `no-commented-code` and ESLint's `no-warning-comments` check commented-out
code and TODOs.

## Violation

- `count++; // increment the count`.
- `/** Gets the user. */` on `function getUser(id: string): User`.

## Not a violation

- `const BATCH = 50; // the carrier API rejects more than 50 parcels per request`.
