# In TypeScript

Module-level state is a top-level `let` that functions reassign, a top-level `Map`,
`Set`, array or object that functions change, or a field of an exported object. Another
module can't reassign an exported `let`, but it can change an exported object or
container: `settings.maintenance = true`, `registry.clear()`.

## Violation

- `let currentLocale = "en"`, reassigned by `setLocale(locale)` and by
  `loadPreferences(user)`.
- `settings.maintenance = true` in a handler in another module, where `settings` is
  exported from `config.ts`.

## Not a violation

- `const cache = new Map<string, User>()`, written only by `getUser(id)`.
- An exported `Object.freeze`d object, and a constant.
- A store whose own methods are the only code that changes its state.
