# In TypeScript

## Violation

- `decode(text: string): Order[]` on `JsonOrderReader`, beside
  `CsvOrderReader.parse(text: string): Order[]`.
- `export function fetchRefunds()` in a module that imports `loadOrders` and
  `loadInvoices`, each reading records from the same store.

## Not a violation

- `parseOrders` and `renderOrders` in one module.
- `parse(text: string)` on a class that `implements` an imported interface declaring
  `parse`.
