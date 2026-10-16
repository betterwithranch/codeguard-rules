---
name: no-sleep-in-async-tests
description: Async coordination
---

# Async coordination

Do not coordinate async tests with `asyncio.sleep()` or `time.sleep()`. Wait on an `asyncio.Event`, `Condition`, or similar primitive.
