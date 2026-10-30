---
name: workflow-state-in-own-module
description: A workflow's state model shares its module with nothing but its own declaration; a state model that a workflow, pipeline or graph threads through its steps, defined in a module that also holds workflow code or another public type, is a violation.
---

# Workflow State In Own Module

A workflow's state model shares its module with nothing but its own declaration.

A state model is a type that a workflow, pipeline or graph run threads through its
steps. Each step receives it, and the run passes it on to the next step in one of these
ways:

- the step returns an updated copy of it;
- the step changes it in place;
- the step returns a partial update, which the run merges into it through the reducers
  its fields name;
- the run saves it as a checkpoint between steps.

Find the steps in the file under review, or in the files that import the state model.

Workflow code is the steps, nodes, runner or graph builder that move the state.

The state model's declaration is the state model itself and:

- its methods;
- the reducers its fields name;
- a type used only in its fields;
- a private type it uses.

A function in the state model's module that takes the state model and returns or
changes it is a step, not one of its methods.

## Violation

A state model whose module also defines workflow code, or a public type that isn't part
of the state model's declaration.

The change must add the state model, change its declaration line or its fields, or add a
definition to its module. Report it on the first line of the state model the change adds
or changes; when the change leaves the state model as it was, on the first line of the
definition the change adds beside it.

## Not a violation

- A state model alone in its module with its declaration.
- A workflow module that imports the state model from the state model's module.
- A shape built and passed once rather than threaded through steps, defined beside the
  code that does so: a request sent and dropped, a result returned once, a config read
  at start-up.
- A type that steps read but never update or pass on as the run's state.

## Why

Every step depends on the state model. Kept apart, each step imports the state without
importing the other steps or the runner, and a change to the state is made in one place
that names it. Kept in the workflow module, every step that needs the state imports the
whole workflow, which imports the steps back.

Source: house convention, from the Common Closure Principle (Robert C. Martin, *Agile
Software Development*, 2002).
