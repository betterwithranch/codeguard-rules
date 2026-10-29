# In TypeScript

## Violation

- `decode(text: string): Order[]` on `JsonOrderReader`, beside
  `CsvOrderReader.parse(text: string): Order[]`.

## Not a violation

- `parseOrders` and `renderOrders` in one module.
