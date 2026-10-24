---
name: equality-over-in
description: A test checks a string the code under test builds by comparing the whole string with ==, never by checking that a fragment is or isn't in it.
---

# Compare whole strings, not fragments

A test checks text the code under test produces by comparing all of it.

A fragment check is an assert that a substring is, or is not, inside a string:
`assert "42" in title`, `assert "draft" not in title`, `self.assertIn("42", title)`, or
`in` inside an expression the assert tests (`assert any("42" in line for line in lines)`).

Supplied content is text another component provides that the test passes to the code
under test without spelling it out: a template the test loads (`load_template(...)`), a
file it reads, a fixture document it opens.

## The test

For each fragment check on a string, ask two questions:

1. Does the searched string hold supplied content that the test passed in?
2. Is the fragment a whole line the code under test inserts into that content: it runs
   from a line start to a newline (`"Order number: ord-42\n"`)?

Two yeses: not a violation. Any no: a violation.

The searched string can be any text, however the test gets it: a return value, an
f-string the code builds, `str(exc.value)` from `pytest.raises`, a test client
response's `response.text` or `response.content.decode()`, `capsys.readouterr().out`,
`caplog.text`, a file the code writes. A code-built string stays code-built when the
code's own template, a module constant or another function of the program supplies
the words; only content the test passes in counts as supplied.

Not a fragment check on a string, so not a violation of this rule:

- `in` on a list, tuple, set or dict (`assert line in invoice.lines`);
- `in` outside an assert, such as an `if` in a helper;
- an `==` comparison of the whole string, whatever it contains.

## Violation

A fragment check on a string where either answer is no:

- a short value inside text the code builds on its own (`assert "7" in order_label(order)`,
  `assert "120" in receipt_total_line(order)`);
- a word in an exception message, response body, log or captured output;
- a `not in` check that a word is absent;
- a fragment of supplied content that is not a whole inserted line (`assert "ord-42" in body`
  where `body` rendered a loaded template).
