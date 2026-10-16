---
name: state-model-own-module
description: Threaded state models get their own module
---

# Threaded state models get their own module

A type that is accumulated, reduced, merged, or checkpointed across a workflow or graph run gets its own module named after it, even with no methods. The test: does the system act on it over time (own module), or pass it once across a boundary (passive shape)?

This applies to the state model only. Place each field type by its own producer. A field type that only wraps an identity another type already owns should not exist; use the identity as a plain field.
