---
name: names-match-behavior
description: Names match what the code does
---

# Names match what the code does

State in one sentence what a symbol does, read from its body. The main verb and nouns of that sentence must appear in the name. Every word in the name must be true of the body. A mismatch in either direction is a defect.

- A misleading name is worse than a vague one. `reconcile` on code that only propagates a failure one way is wrong, not just unclear.
- Both the verb and the noun must carry domain meaning. A generic verb on a generic noun (`process_data`, `handle_items`, `manage_state`) says nothing.
- Name a symbol after what it produces, owns, or does. Do not name a type `Preparer` or `Processor` when it builds a specific output.
- Use one verb per concept across collaborating types. Do not mix `resolve`/`interpret` or `build`/`assemble` for the same operation.

Bad: `_reconcile_dependencies` whose body fails the tasks waiting on a file and wakes the jobs blocked on them.

Good: `_fail_dependent_tasks`.
