---
name: no-reimplemented-orchestration
description: Code does not call a pipeline's stages in sequence, each feeding the next, when a component of the program already runs those same stages as one call.
---

# Don't re-implement orchestration

When a component of the program runs a sequence of stages as one call, other code gets
that sequence's result by calling the component, not by calling the stages itself.

A pipeline is a method or function that calls two or more stages in order, passing one
stage's output into the next: `run()` calling `planner.plan(order_id)` and then
`packer.pack(plan)`; a resolver calling `capture`, then `resolve`; a service calling
`extract`, then `validate`. A stage is a call to a collaborator's method or a function.
The pipeline is in the file under review or a file of the program it imports or
receives as a type (a constructor parameter typed `FulfillmentPipeline`); read that file
to see the stages its method calls.

## The test

For each piece of code that calls two or more stages in sequence, feeding each one's
output into the next, ask: is there a pipeline, other than this code, that calls the
same stages — the same methods of the same collaborator types, or the same functions —
in the same order with the same flow of outputs?

Forms of the sequence, all answered by the same question:

- through locals: `plan = planner.plan(order_id)` then `return packer.pack(plan)`;
- nested: `packer.pack(planner.plan(order_id))`;
- reached through the pipeline's own collaborators: `self._pipeline.planner.plan(...)`;
- with `await`: `plan = await planner.plan(order_id)`;
- with the collaborators taken in this class's own constructor, or imported functions
  called in order (`validate(extract(document))`).

The answer is no when:

- this code is the pipeline itself, the one place that sequence is defined;
- no visible component calls those stages in that order;
- the code calls the pipeline's entry point (`pipeline.run(order_id)`), or one stage
  alone (`planner.plan(order_id)` to show a preview);
- the code runs a different sequence: other stages, another order, or a stage between
  them that the pipeline doesn't have.

## Violation

Code outside a pipeline that calls that pipeline's stages in the pipeline's order,
feeding each output into the next stage.
