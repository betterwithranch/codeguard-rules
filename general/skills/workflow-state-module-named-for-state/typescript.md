# In TypeScript

## State models

- An interface or type whose steps return a spread copy, `{ ...state, total }`, or a
  class whose steps call its own `withTotal(...)`.
- An interface whose steps assign to its fields or push to its arrays.
- A LangGraph.js `Annotation.Root({...})` state whose nodes return partial objects.

## Named for the state

- `checkoutState.ts` or `checkout-state.ts` holding `CheckoutState`.
- `checkout/state.ts` holding `CheckoutState`.

## Violation

- `checkout/types.ts` holding only `CheckoutState`, imported by the steps in
  `checkout/pipeline.ts`.
