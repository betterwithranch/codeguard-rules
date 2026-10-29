# In TypeScript

A program type is a class, or an interface or type alias for an object, that the program
declares. Its homes are the class's constructor or a static method on it, a function in
the module that declares it, a factory class, or a mapper module or class named for its
source. A class declares a default with a parameter or property initializer; an
interface has no defaults, so a function in its module that fills them is their home.

An object literal typed by an interface and built where it's used, from the function's
own values, is how TypeScript builds data, and is not a violation.

## Violation

- `new Account(user.id, user.signupPlan, user.country)` in a controller method that then
  saves and emails.
- `{ ...input, tier: input.tier ?? "free" }` or `tier: input.tier || "free"` for an
  `Account` field.
- `function register(email: string, tier = "free"): Account { return { email, tier }; }`.
- `id: crypto.randomUUID()` or `openedAt: new Date()` in a literal for a type built
  elsewhere.

## Not a violation

- `Account.forUser(user)` or `this.accounts.open(user)` called from a service.
- `throw new AccountLocked(account.id)`.
- `{ ...account, tier: "pro" }` copying an account.
- A literal of the function's own computed values returned as its result.
