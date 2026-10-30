# In TypeScript

## State models

- An interface or type whose steps return a spread copy, `{ ...state, total }`, or a
  class whose steps return a new instance or call its own `withTotal(...)`.
- An interface whose steps assign to its fields or push to its arrays.
- A LangGraph.js `Annotation.Root({...})` state whose nodes return partial objects,
  merged through the `reducer` each field's `Annotation` names.
- A state a runner saves to a checkpoint store, or a LangGraph.js checkpointer saves,
  after each step.

A declaration the module doesn't export is private.

## Violation

- `checkout/pipeline.ts` declaring `interface CheckoutState` and the steps
  `price(state: CheckoutState): CheckoutState` that return `{ ...state, total }`.
- A LangGraph.js `Annotation.Root({...})` state declared in the module that builds the
  `StateGraph`.

## Not a violation

- `checkout/state.ts` exporting only `class CheckoutState` with its `withTotal` method,
  imported by `checkout/pipeline.ts`.
- A props or options interface a function takes once.
