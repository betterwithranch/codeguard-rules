# In TypeScript

Bundles include a project's `Config`, `AppContext` or environment object, an Express
`Request` or a `NextRequest` taken by a helper, and a context object a module threads
through its calls.

## Violation

- `function retryDelay(config: AppConfig): number` reading only `config.retryBaseMs`,
  where `AppConfig` declares eight fields.

## Not a violation

- `function isOverdue(invoice: Invoice, today: Date)` reading only `invoice.dueOn`.
- An Express handler `(req, res) => ...` reading only `req.params.id`.
- A React component reading a few of its props.
