# In Python

Data models are pydantic models and settings, dataclasses and attrs classes with
validation, msgspec structs, and Django models. Validators are `@field_validator`,
`@model_validator`, `@validator`, `@root_validator`, `model_post_init`,
`__post_init__`, `__attrs_post_init__`, attrs `validator=`, and a Django model's
`clean()` and `clean_fields()`.

## Violation

- `info.context["catalog"].has(sku)` in a pydantic `field_validator`.
- `if value not in settings.SUPPORTED_CURRENCIES: raise ValueError(...)`.
- `Product.objects.filter(sku=self.sku).exists()` in a dataclass `__post_init__`.

## Not a violation

- `if value <= 0: raise ValueError(...)`, and `if self.ends_at <= self.starts_at`.
- `if value not in CURRENCIES`, where `CURRENCIES` is a constant in the module.
- A Django `Form.clean_email` or DRF serializer `validate` that queries the database.
- A Django model's `clean()` checking no other row has the same slug.
