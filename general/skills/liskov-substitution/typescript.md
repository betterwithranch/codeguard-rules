# In TypeScript

A base is a class named in `extends`, an abstract class, or an interface named in
`implements`. A method the base leaves for subclasses is `abstract` or an interface
member.

## Violation

- `refund(payment: Payment, amount: number): never { throw new Error("not supported");
  }` where the base's `refund` does the refund, or in a class implementing an interface
  whose `refund` it must supply.
- `export(rows: Row[], includeHeader = true): string` whose body never reads
  `includeHeader`, where the base's `export` uses it.
- `find(key: string): Item | undefined { return undefined; }` where the base's `find`
  looks the key up.
- `close(): void {}` where the base's `close` releases its connection.

## Not a violation

- `save(record: Rec): void { this.audit(record); super.save(record); }`.
- A class implementing an interface's methods by doing the work each one names.
- An override of an `abstract` method.
- A class extending one imported from another module, or a framework class such as
  `Error`.
