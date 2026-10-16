---
name: enum-usage
description: Enum usage
---

# Enum usage

- Do not call `.value` on a `StrEnum` or `IntEnum` member.
- Where a parameter, field, dict key, or argument is typed as an enum, pass the member (`OrderStatus.CANCELLED`), never a bare literal (`"cancelled"`). This holds in tests too.
