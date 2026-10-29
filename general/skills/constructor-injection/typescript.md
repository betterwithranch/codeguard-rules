# In TypeScript

The constructor is `constructor`, including parameter properties such as `private
readonly mailer: Mailer`, and NestJS and Angular injection through it.

## Violation

- `async notify(userId: string, mailer: Mailer): Promise<void>` on a class, calling
  `mailer.send(...)`.

## Not a violation

- `constructor(private readonly mailer: Mailer) {}` and `async notify(userId: string)`.
- A method whose signature an implemented interface declares with the collaborator.
