---
name: threaded-state-own-module
description: A workflow's threaded state has a module of its own; a state model that a workflow, pipeline or graph threads through its steps, defined in a module that also holds workflow code or unrelated public types, or named for something else, is a violation.
---

# Threaded State Own Module

A workflow's threaded state has a module of its own.

A state model is a type that a workflow, pipeline or graph run threads through its
steps. Each step receives it and then does one of these:

- returns an updated copy (`replace(state, ...)`, `state.model_copy(update=...)`,
  `state.with_step(...)`);
- mutates it in place;
- merges partial updates into it through a reducer, as a LangGraph `TypedDict` state does
  with `Annotated[list[str], operator.add]` fields;
- checkpoints it between steps.

A state model may have methods of its own. Find the steps in the file under review, or
in the files that import the state model.

Workflow code is the steps, nodes, runner or graph builder that move the state.

The state model's own module is one where:

- the public definitions are the state model and what belongs to its declaration: its
  methods, the reducers its fields name, and a type used only in its fields; and
- the name names the state: `checkout_state.py` for `CheckoutState`, or `state.py`
  inside `checkout/`.

## Violation

A state model in a module that:

- also defines workflow code;
- also defines another public type that isn't part of the state's declaration; or
- is named for something else (`checkout/models.py`, `checkout/workflow.py`).

The change must add or change the state model, or add a definition to its module. Report
it on the state model's class line when the change touches it, otherwise on the
definition the change adds beside it.

## Not a violation

- A state model alone in its own module, with its methods and reducers.
- A workflow module that imports the state model from its own module.
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
