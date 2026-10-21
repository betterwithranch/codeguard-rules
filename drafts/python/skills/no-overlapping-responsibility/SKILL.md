---
name: no-overlapping-responsibility
description: No overlapping responsibility
---

# No overlapping responsibility

Two differently named types must not both own the same concept, such as a `Service` and a `Factory` with the same `create_*` surface, or two views computing the same projection. The bodies need not match. Search for sibling types with the same role and domain noun.

Two passive shapes with identical fields are not overlap when they sit at different boundaries, are mapped explicitly at a seam, and change for independent reasons. Flag only when they share one reason to change.
