# In Python

The import-boundary tool is import-linter, configured in `.importlinter`, `setup.cfg`
or `pyproject.toml` under `[tool.importlinter]`. A contract names packages in
`modules`, `layers`, `containers`, `source_modules` or `forbidden_modules`; a wildcard
such as `shop.*` covers every child package.

## Violation

- `shop/returns/policy.py` added, where the independence contract lists
  `shop.billing`, `shop.shipping` and `shop.catalog` but not `shop.returns`.

## Not a violation

- `shop/returns/policy.py` added, where the contract lists `modules = shop.*`.
