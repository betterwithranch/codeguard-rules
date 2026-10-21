---
name: mock-only-at-boundary
description: Mock only at the process boundary
---

# Mock only at the process boundary

`Mock`, `MagicMock`, and `patch()` are allowed only where code leaves the process: HTTP calls to third-party APIs, cloud SDK calls, services that need external credentials. Controlling time or randomness, and forcing hard-to-trigger error paths (network failure, full disk), are also allowed.

- The database is not a boundary. Use a real test database. Never mock queries, query results, or record objects.
- Never mock or patch collaborating classes, internal functions, factories, module-level callables, or private methods. Inject the dependency or use a real object.
- `monkeypatch.setattr` is `patch()` by another name. Reassigning a module function, constant, or attribute of the code under test so its real work does not run is not allowed. Example: `monkeypatch.setattr(report_module, "load_catalog", lambda: {...})`. Pass in a value the test builds instead.
- Patching settings, feature flags, or environment variables is allowed only when varying that value is what the test is about.
- Do not assert on the arguments one internal component passes to another.

Preference order: real object, then shared fake, then an inline stub implementing a protocol (only for framework contract tests), then a mock (only at the process boundary).
