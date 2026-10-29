# In TypeScript

A field is a property of a class, interface or object type, or a piece of React
component state held with `useState` or `useReducer`.

## Violation

- `shippedAt?: Date` and `isShipped: boolean` on one class.
- `const [items, setItems] = useState<Item[]>([])` and `const [count, setCount] =
  useState(0)` in one component, where `count` is always `items.length`.

## Not a violation

- `get isShipped(): boolean { return this.shippedAt !== undefined; }`.
- `const count = items.length` computed while rendering, or with `useMemo`.
- `isGift: boolean` beside `shippedAt`.
