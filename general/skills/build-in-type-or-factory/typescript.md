# In TypeScript

A program type is a class, or an interface or type alias for an object, that the program
declares. Its homes are the class's constructor or a static method on it, a function in
the module that declares it, a factory class, or a mapper module or class named for its
source. An entity class a TypeORM, MikroORM or Sequelize model maps to a table is the
persistence library's to build.

An object literal typed by an interface, built from the function's own parameters or
from values it computed as its answer, is how TypeScript builds data, and is not
building.

## Violation

- `new Account(user.id, user.signupPlan, user.country)` in a controller method that then
  saves and emails.
- `const account: Account = { ownerId: user.id, plan: user.signupPlan }` in a handler
  among its other work.
- An `Invoice` method that returns `new Account(this.customerId, ...)`.

## Not a violation

- `Account.forUser(user)` or `this.accounts.open(user)` called from a service.
- `new Account(ownerId, plan)` from the function's own parameters, or with
  `status: "pending"`.
- `this.repository.create({ ... })` on an ORM repository.
- `throw new AccountLocked(account.id)`.
- `{ ...account, tier: "pro" }` copying an account.
- `new Date(...)`, `new URL(...)`, `new Map(...)`.
