# In TypeScript

The import-boundary tool is dependency-cruiser, configured in `.dependency-cruiser.js`
or `.cjs`, or `eslint-plugin-boundaries`, configured with `boundaries/elements` in the
ESLint configuration. Rules name folders by path pattern; a pattern with a capture group
such as `^src/features/([^/]+)/` covers every child folder.

## Violation

- `src/features/returns/policy.ts` added, where the boundaries elements list
  `src/features/billing` and `src/features/shipping` but not `src/features/returns`.

## Not a violation

- `src/features/returns/policy.ts` added, where the element pattern is
  `src/features/*`.
