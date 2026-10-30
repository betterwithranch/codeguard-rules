# In TypeScript

State changes include assigning `this.x` or a parameter's property, `push`, `splice`,
`delete`, `Map.set` and `Set.add` on a collection that outlives the call, and writes to
a database, storage or queue.

The idioms exempt as take-and-return or chaining operations include `push` returning
the length, `shift`, `pop`, and `Map.set` returning the map.

## Violation

- `function takeUnreadCount(inbox: Inbox): number` that marks every message read and
  returns how many were unread.

## Not a violation

- `async function createOrder(...): Promise<string>` that inserts an order and returns
  its id.
