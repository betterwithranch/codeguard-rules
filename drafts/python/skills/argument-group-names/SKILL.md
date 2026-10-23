---
name: argument-group-names
description: A type named as a request or as an action (`...Request`, `...Create`, `...Update`, `Create...`) that only groups the arguments of a call inside the program, rather than modelling a request that crosses the process boundary, is a violation.
---

# Argument groups aren't named as requests or actions

A type's name says what it is: a group of arguments passed between parts of the program
is not named as a request, nor as the act it is passed to.

An argument group is a type whose instances carry the inputs of one call to a function,
method or constructor of the program itself: the caller builds it to make that call,
and the callee reads its fields. A boundary request is data that crosses the process
boundary as a request: a request or response body bound by a web framework (a FastAPI
route parameter, a DRF serializer, a Django form, a Flask view's parsed body), a message
read from or written to a queue or broker, or a payload sent to or returned by an
outside API client. A request or action name ends in `Request`, `Create`, `Update` or
`Delete` after another word (`QuoteRequest`, `OrderCreate`), or starts with `Create`,
`Update` or `Delete` before another word (`CreateOrder`).

## The test

For each type in the file with a request or action name, whether a class, dataclass,
pydantic model, `TypedDict`, `NamedTuple` or one built with `TypedDict(...)` or
`namedtuple(...)`, find where it is built and read, in the file or by searching the
repository for its name. Then ask: is it a boundary request?

Yes is not a violation. No, it only groups the arguments of a call inside the program,
is a violation.

- `PriceCalculationRequest` built by a view and read only by `PriceCalculator.calculate`:
  a violation.
- `OrderCreate`, a pydantic model a FastAPI route takes as its body: not a violation.
- `ShipmentQuoteRequest`, the payload a carrier API client sends: not a violation.
- `CreateInvoice`, a dataclass passed from one service method to another in the same
  process: a violation.

## Violation

A type in the file under review with a request or action name whose instances only
carry the arguments of a call inside the program, and never cross the process boundary
as a request.
