---
name: map-models-field-by-field
description: Map between models field by field
---

# Map between models field by field

When converting one typed model into another, assign each field explicitly. Do not round-trip through a dict: `Target(**dataclasses.asdict(source))`, `Target.from_dict(source.to_dict())`, or a list of dumped dicts fed into another model's field. Serializing to a dict is fine only when the dict is the destination (JSON, a database column, a wire payload).

When one source type is mapped into more than one target, give it one dedicated mapper class that does the explicit field mapping, and have every target delegate to it. A single-target mapping stays inline.
