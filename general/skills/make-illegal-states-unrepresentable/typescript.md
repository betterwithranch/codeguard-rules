# In TypeScript

A type is an interface, an object type alias or a class. An optional field is marked
`?` or typed `X | undefined` or `X | null`. A status or kind field is a string literal
union or an enum.

## Violation

- `interface Invoice { state: "draft" | "sent" | "paid"; sentAt?: Date; paidAmount?:
  number }`, where only a sent invoice has `sentAt` and only a paid one has
  `paidAmount`.
- A class with `kind: "card" | "bank"`, `cardNumber: string | null` and `iban: string |
  null`.
- An interface with a `kind` typed by an enum, and optional fields only some of its
  members have.
- An interface with `email?: string` and `phone?: string`, where exactly one of them is
  set.

## Not a violation

- `type Invoice = { state: "draft" } | { state: "sent"; sentAt: Date } | { state:
  "paid"; sentAt: Date; paidAmount: number }`.
- A Prisma model or an ORM entity with a status column and nullable columns.
- An interface that mirrors an outside API's payload as it arrives, before it's parsed
  into the program's own types.
- `interface Contact { name: string; middleName?: string; phone?: string }`.
