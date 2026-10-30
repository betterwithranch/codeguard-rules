# In Python

Data models are pydantic models and pydantic-settings settings, dataclasses and attrs
classes with validation, msgspec structs, and Django models. Validators are
`@field_validator`, `@model_validator`, `@validator`, `@root_validator`,
`model_post_init`, the function in an `Annotated[..., AfterValidator(f)]` (or
`BeforeValidator`, `WrapValidator`, `PlainValidator`), `__post_init__`,
`__attrs_post_init__`, attrs `@<field>.validator` and the function passed as
`validator=`, and a Django model's `clean()` and `clean_fields()`.

Request validation is a Django `Form` or DRF `Serializer`, and the view or service that
handles the request.

## Violation

- `info.context["catalog"].has(sku)` in a pydantic `field_validator`.
- `if value not in settings.SUPPORTED_CURRENCIES: raise ValueError(...)`.
- `Product.objects.filter(sku=self.sku).exists()` in a dataclass `__post_init__`.

## Not a violation

- `if value <= 0: raise ValueError(...)`, and `if self.ends_at <= self.starts_at`.
- `if value not in CURRENCIES`, where `CURRENCIES` is a constant in the module.
- A Django `Form.clean_email` or DRF serializer `validate` that queries the database.
