---
name: no-duplicate-logic
description: No duplicate logic
---

# No duplicate logic

Two function or method bodies that are near-identical copies are one concept. Keep one implementation with one parameter order and point both callers at it. Copies with different signatures (for example, the first two parameters swapped) are the worst case.
