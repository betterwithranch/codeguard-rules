---
name: python-generics
description: Rules for Python classes that use TypeVar, Generic, or type parameters.
---

# Python Generics

These rules apply to Python code that defines or subclasses generic classes, ABCs, or Protocols with type parameters, or that annotates attributes with generic types.

## Every TypeVar in an annotation is bound by the class

A TypeVar used in a class attribute annotation must appear in that class's `Generic[...]` parameters. If the class does not need the parameter, use a concrete type or `Any` in that position.

Bad:

```python
class OrderHolder(Generic[TOrder]):
    pricer: Pricer[TOrder, TCurrency]
```

Good:

```python
class OrderHolder(Generic[TOrder, TCurrency]):
    pricer: Pricer[TOrder, TCurrency]
```

## Parameterize generic annotations

Do not leave a generic type bare on a class attribute. A bare `Pricer` is silently `Pricer[Any, Any]`.

Bad:

```python
class Checkout:
    pricer: Pricer
```

Good:

```python
class Checkout(Generic[TOrder]):
    pricer: Pricer[TOrder, Any]
```

## Pass type arguments through subclasses

A subclass of a generic class either binds concrete type arguments or keeps them generic by re-declaring `Generic` with the same parameters. It never drops them.

```python
class Ledger(Generic[TEntry, TAccount]): ...

class InvoiceLedger(Ledger[InvoiceEntry, CustomerAccount]): ...

class AuditedLedger(Ledger[TEntry, TAccount], Generic[TEntry, TAccount]): ...
```

## Variance matches use

- Leave a TypeVar invariant (the default) when the class both reads and writes values of that type.
- Use a covariant TypeVar (`T_co = TypeVar("T_co", covariant=True)`) only for a type that appears in return positions.
- Use a contravariant TypeVar (`T_contra = TypeVar("T_contra", contravariant=True)`) only for a type that appears in parameter positions.

## One parameterized helper, not one method per variant

When helper methods on a generic class or ABC differ only by an enum or literal value, write one method that takes the value as a parameter.

Bad:

```python
class Validator(ABC, Generic[TRecord]):
    def _missing(self, field: str) -> None: ...
    def _invalid(self, field: str) -> None: ...
    def _ambiguous(self, field: str) -> None: ...
```

Good:

```python
class Validator(ABC, Generic[TRecord]):
    def _add_issue(self, field: str, issue_type: IssueType) -> None: ...
```

## Read type arguments in `__init_subclass__`

When a generic base needs the concrete type argument a subclass binds, capture it once in `__init_subclass__` with `get_origin` and `get_args` over `__orig_bases__`. Do not require each subclass to restate the type as a separate attribute.

```python
class Repository(Generic[TRecord]):
    record_type: type[TRecord]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in cls.__orig_bases__:
            if get_origin(base) is Repository and get_args(base):
                cls.record_type = get_args(base)[0]
                return
```

## No shared instances of stateful generic classes

If a generic class accumulates state during method calls (for example, collecting issues), do not share one module-level instance. Create a fresh instance per use, such as through a factory function.

Bad:

```python
validator = OrderValidator(region="eu")
```

Good:

```python
def create_order_validator() -> OrderValidator:
    return OrderValidator(region="eu")
```
