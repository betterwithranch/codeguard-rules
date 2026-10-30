# In Python

Public classes are top-level classes whose names don't start with `_`, including
`Enum`, `TypedDict` and `NamedTuple` types, whether declared with `class` or by calling
`Enum(...)`, `TypedDict(...)` or `NamedTuple(...)`.

Exempt modules: Django's `models.py`, `admin.py`, `forms.py` and `serializers.py`,
FastAPI's `schemas.py`, and a package's `__init__.py` that re-exports.

## Violation

- `class RetryBackoffPolicy` with a `delay()` method in `notifications/dispatcher.py`
  beside `NotificationDispatcher`.
- `enums.py` holding `CarrierCode`, `RefundReason` and `InvoiceStatus`.

## Not a violation

- `errors.py` holding `PaymentError` and its subclasses.
- `class ExportResult` returned by `Exporter.run()`, in the exporter's module.
