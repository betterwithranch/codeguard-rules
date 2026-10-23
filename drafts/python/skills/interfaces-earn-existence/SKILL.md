---
name: interfaces-earn-existence
description: A Protocol or abstract base class with fewer than two implementers, whose one implementer its consumers could import without an import cycle, is a violation.
---

# Interfaces must earn their existence

An interface exists only when two or more classes implement it, or when it keeps a
module from importing a module that imports it back.

An interface is a class whose bases include `Protocol` (`typing.Protocol`,
`Protocol[T]`) or `ABC` (`abc.ABC`, `metaclass=ABCMeta`), with members left for others to
supply: `...` bodies or `@abstractmethod`. An implementer is a class outside test files
that subclasses the interface or, for a `Protocol`, defines all of its members with
the same signatures. A test double (a class under `tests/` or in
`conftest.py`, or named `Fake`, `Stub`, `Mock` or `Dummy`) is not an implementer. A
consumer is code that annotates a parameter, attribute or return value with the
interface. An implementer someone plans to write is not an implementer: only code in
the repository counts.

## The test

For each interface defined in the file, find its implementers: in the file, and in the
rest of the repository by searching for the interface's name and, for a `Protocol`, its
method names. Then ask:

1. Are there two or more implementers? Yes is not a violation.
2. Otherwise, would retyping each consumer against the one implementer make the
   consumer's module import the implementer's module, when the implementer's module
   already imports the consumer's module, directly or through the modules it imports?
   Yes, the interface prevents an import cycle, so it is not a violation. No is a
   violation.

An interface with no implementer at all is a violation by the same test.

Not a violation:

- a `Protocol` in a lower-level package, for what that package needs from a
  higher-level one that imports it, even with one implementer;
- a `Protocol` or `ABC` with two or more implementers in the repository, wherever they
  are;
- an abstract Django model (`class Meta: abstract = True`), a pydantic `BaseModel`, or a
  base class with no members left for others to supply, which are not interfaces.

## Violation

An interface defined in the file under review with fewer than two implementers in the
repository, where its consumers could be typed against the one implementer without an
import cycle.
