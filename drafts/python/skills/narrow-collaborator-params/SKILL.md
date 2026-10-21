---
name: narrow-collaborator-params
description: Pass only what a collaborator needs
---

# Pass only what a collaborator needs

A violation is a parameter typed as a wide object (a context, request, config, or record) when the function reads only a few of its fields and calls none of its methods.

Not a violation:

- A parameter the function uses as a whole: it passes the object on, calls its methods, or reads most of its fields.
- A dataclass for values that travel together through more than one call (`DateRange`, `Money`).
