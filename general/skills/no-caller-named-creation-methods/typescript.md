# In TypeScript

Creation methods include `static` methods that return `new` instances of their class,
methods of a `...Factory` class, and exported or module functions named `create...`,
`make...`, `build...`, `new...`, `for...` or `from...`.

## Violation

- `static forCheckoutPage(...)` on `Order`.

## Not a violation

- `static fromCartItems(...)` on `Order`.
