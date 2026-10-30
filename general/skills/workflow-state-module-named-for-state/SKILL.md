---
name: workflow-state-module-named-for-state
description: A module that holds only a workflow's state model is named for the state; a module holding nothing but a state model a workflow, pipeline or graph threads through its steps, named for something else, is a violation.
---

# Workflow State Module Named For State

A module that holds only a workflow's state model is named for the state.

A state model is a type that a workflow, pipeline or graph run threads through its
steps: each step receives it and the run passes it on, updated, to the next step. Find
the steps in the files that import the state model.

A module holds only the state model when it defines nothing but the state model and
its declaration: its methods, the reducers its fields name, the types used only in its
fields, and private types it uses.

A module is named for the state when its name is the state model's name (`checkout_state`
for `CheckoutState`), or when it is named `state` inside a package or directory named for
the workflow (`checkout/state`).

## Violation

A module that holds only a state model and is named for something else: a kind of code
(`checkout/models`, `checkout/types`), or a different concept.

The change must add the state model, or change its declaration line or its fields. A
change to the state model's fields in a module that was already misnamed is a violation
too: every change to the state is a change to the module that holds it, and is the time
to give that module the state's name. Report it on the first line of the state model the
change adds or changes.

## Not a violation

- A type, alone in a module named for something else, that is built and passed once, or
  that steps read but never update or pass on as the run's state.

## Why

A workflow's steps all import its state. Named for the state, its module is the one a
reader opens to find what the run carries, and the one an import names; named `models`
or `types`, it reads as a place for any shape, and the next unrelated type lands beside
the state.

Source: house convention.
