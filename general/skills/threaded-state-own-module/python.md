# In Python

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
