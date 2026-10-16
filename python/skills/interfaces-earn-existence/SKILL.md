---
name: interfaces-earn-existence
description: Interfaces must earn their existence
---

# Interfaces must earn their existence

A `Protocol` or `ABC` is justified when it inverts a real dependency, or when two or more implementers exist today. Either alone is enough.

- A lower-level package that defines a narrow `Protocol` for what it needs, instead of importing a higher-level concrete type, is correct even with one implementer.
- Test: would retyping the consumers against the concrete type create an import cycle? Yes: keep. No: delete the interface.
- A planned second implementer does not justify an interface.
- An interface belongs in the package that depends on it.
- A `Protocol` must be designed from the consumer's needs. Do not write a `Protocol` whose members are just the attributes the consumer happens to read off one wide object. Sign: its members match a slice of one concrete class one-for-one and no other type was built to satisfy it. Pass a parameter object with exactly what the consumer needs instead.
