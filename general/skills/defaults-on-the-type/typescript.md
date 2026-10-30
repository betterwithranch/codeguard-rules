# In TypeScript

A program type is a class, or an interface or type alias for an object, that the program
declares. A class declares a default with a property initializer or a constructor
parameter default. An interface or type alias holds no defaults, so they are declared
once in its module, as a constant of defaults or a function that fills them.

## Violation

- `{ ...input, tier: input.tier ?? "free" }` or `tier: input.tier || "free"` for an
  `Account` field.
- `function register(email: string, tier = "free"): Account { return { email, tier }; }`.
- `id: crypto.randomUUID()` or `openedAt: new Date()` for an `Account` field the type
  leaves required, in a service or in a static method on the class.

## Not a violation

- `new Account(email)` where the class declares `tier = "free"`.
- `tier: requestedTier ?? user.signupTier`, a fallback to other data.
- `openedAt: this.clock.now()` in an account factory.
- `{ email, tier: "trial" }` in a function that opens trial accounts.
- `function recentAccounts(limit = 20)`, or `fetch(url, { cache: "no-store" })`.
