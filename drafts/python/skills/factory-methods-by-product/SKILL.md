---
name: factory-methods-by-product
description: A factory method named for the caller or use case that calls it (`create_for_admin_dashboard`), rather than for what it creates, is a violation.
---

# Factory methods are named for their product

A factory's methods are named for the product variant they make or the input they make
it from, not for who calls them.

A factory is a class whose job is to create instances of a type: a class named
`...Factory`, `...Creator` or `...Maker`, or a class's own alternative constructors
(class methods that return `cls(...)`). A creation method is a method of a factory that
returns a new product. A caller or use case is a screen, endpoint, client app, team,
job or feature that calls the method (`admin_dashboard`, `checkout`, `mobile_app`,
`nightly_import`).

## The test

For each creation method in the file, ask: does its name state the caller or use case
that calls it, instead of a difference in the product (`create_draft`,
`create_recurring`) or in the input it is made from (`from_csv_row`, `from_order`)?

Yes is a violation, whether the method is on a `...Factory` class, a service, or the
product's own class method (`Invoice.for_checkout(...)`), and whether or not its body
matches a sibling's. No is not.

## Violation

A creation method in the file under review whose name states the caller or use case
that calls it rather than what it creates or what it creates it from.
