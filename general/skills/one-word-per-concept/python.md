# In Python

## Violation

- `def interpret(self, text: str) -> list[Order]` on `JsonOrderReader`, beside
  `CsvOrderReader.parse(self, text: str) -> list[Order]`.
- `def fetch_refunds()` in a module that imports `load_orders` and `load_invoices`, each
  reading records from the same store.

## Not a violation

- `parse_orders` and `render_orders` in one module.
- `def parse(self, text)` on a class implementing an imported `Protocol` that declares
  `parse`.
