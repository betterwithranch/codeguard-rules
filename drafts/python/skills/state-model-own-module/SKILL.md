---
name: state-model-own-module
description: A state model that a workflow or graph threads through its steps is defined in a module of its own, named after it, with no workflow code beside it.
---

# Threaded state models get their own module

A state the system acts on over time is a concept of its own and has its own module.

A state model is a type that a workflow, pipeline or graph run threads through its
steps: each step receives it and returns an updated copy (`replace(state, ...)`,
`state.model_copy(update=...)`, `state.with_step(...)`), mutates it in place, merges
partial updates into it with a reducer (a LangGraph `TypedDict` state with
`Annotated[list[str], operator.add]` fields), or checkpoints it between steps. It is a
state model whether or not it has methods, and in any form: dataclass, pydantic model,
attrs class, `TypedDict`.

A passive shape passed once across a boundary is not a state model: a request built,
sent and dropped, a result returned once, a config read at start-up.

Its own module is one whose public definitions are the state model and the code that
is part of its declaration (its methods, the reducers its field annotations name, a
type used only in its fields), and whose name names it (`checkout_state.py` for
`CheckoutState`, or `state.py` inside `checkout/`).

## The test

For each class in the file, ask: does a workflow or graph act on it over time, as
above? Find the steps in this file or in the files that import it. If it is a state
model, ask: is this file its own module?

A violation when the file also defines workflow code (steps, nodes, the runner, the
graph builder), or other public types that are not part of the state's declaration,
or is named for something else (`checkout/models.py`, `checkout/workflow.py`).

Not a violation:

- a state model alone in its own module, with its methods and its reducers;
- a passive shape defined beside the code that builds and passes it once;
- the workflow module importing the state model.

## Violation

A state model defined in a module that is not its own: `CheckoutState`, threaded
through `record_step` and `run_checkout` by `replace`, defined in `checkout/workflow.py`
beside them; a LangGraph `ReviewState` defined in `review/graph.py` beside the node
functions; a threaded state in `orders/models.py` beside unrelated models.
