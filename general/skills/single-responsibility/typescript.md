# In TypeScript

A function is a function declaration, an arrow function or function expression bound to
a name, a class method, a getter, or an `async` function, including an Express or NestJS
handler, a React component and a hook. A class includes a NestJS service or controller,
an ORM entity and a plain class.

## Violation

- A React component that renders a list and works out the business's pricing or
  eligibility rules inline in its body.
- A handler that reads its request and applies a fee schedule or tiering rules inline
  before responding.
- A function that unpacks a vendor's response shape (its field names, its encoded
  values) and applies the business's rules to what it unpacked.
- A service class for one domain that gains a method writing another system's file
  layout, or calling an outside API that none of its other methods use.

## Not a violation

- A handler that parses its request with zod or class-validator, calls a service and
  sends the result.
- A component that calls an imported function or hook for its data and renders it.
- A parser that reads every field of one format and builds typed records.
- A value class with arithmetic, comparison and `toString()` over its own fields.
- A NestJS controller whose routes all serve one resource.
