---
name: parameterized-helper
description: One parameterized helper, not one method per variant
---

# One parameterized helper, not one method per variant

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
