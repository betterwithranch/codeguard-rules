# In TypeScript

Names are read from function declarations, functions assigned to a `const`, methods and
classes, split on capitals.

## Violation

- `async function deleteUser(id: string)` whose body sets `user.disabled = true` and
  saves the user.
- `function sortedByDate(events: Event[])` that returns `events.filter(...)` without
  sorting.

## Not a violation

- `function parseAmount(text: string): number` that parses the text.
- `constructor`, and framework hooks such as `ngOnInit` or `componentDidMount`.
