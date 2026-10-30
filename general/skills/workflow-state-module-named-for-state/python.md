# In Python

## State models

- A frozen dataclass whose steps return `replace(state, ...)`, or a pydantic model whose
  steps return `state.model_copy(update=...)`.
- A mutable dataclass or model whose steps assign to its fields.
- A LangGraph `TypedDict` state whose nodes return partial dicts.

## Named for the state

- `checkout_state.py` holding `CheckoutState`.
- `checkout/state.py` holding `CheckoutState`.

## Violation

- `checkout/models.py` holding only `CheckoutState`, imported by the steps in
  `checkout/workflow.py`.
