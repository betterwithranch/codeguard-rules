# In TypeScript

## Violation

- `checkout/pipeline.ts` declaring `interface CheckoutState` and the steps
  `price(state: CheckoutState): CheckoutState` that return `{ ...state, total }`.
- A LangGraph.js `Annotation.Root({...})` state declared in the module that builds the
  `StateGraph`.

## Not a violation

- `checkout/state.ts` exporting only `CheckoutState` and a `withTotal` helper, imported
  by `checkout/pipeline.ts`.
- A props or options interface a function takes once.
