# In Python

## State models

- A frozen dataclass whose steps return `replace(state, ...)`, or a pydantic model whose
  steps return `state.model_copy(update=...)` or call its own `state.with_step(...)`.
- A mutable dataclass or model whose steps assign to its fields or append to its lists.
- A LangGraph `TypedDict` state whose nodes return partial dicts, merged through the
  reducers its `Annotated[list[str], operator.add]` fields name.
- A model a runner saves to a checkpoint store, or a LangGraph checkpointer saves, after
  each step.

A name starting with `_` is private.

## Violation

- `checkout/workflow.py` defining `@dataclass(frozen=True) class CheckoutState` and the
  steps `price(state) -> CheckoutState` and `charge(state) -> CheckoutState` that each
  return `replace(state, ...)`.
- A LangGraph `class ReviewState(TypedDict)` with `findings: Annotated[list[str],
  operator.add]` defined in `review/graph.py` beside the `StateGraph(ReviewState)`
  builder.

## Not a violation

- `checkout/state.py` holding only `CheckoutState` and its `with_total()` method,
  imported by `checkout/workflow.py`.
- A `ReportRequest` dataclass built once and passed to `render(request)`.
