---
name: liskov-substitution
description: A subclass keeps every promise its base class makes; an override that raises where the base doesn't, ignores an argument, accepts less, returns less, or stubs out an inherited method is a violation.
---

# Liskov Substitution

A subclass keeps every promise its base class makes.

A base is a class another class inherits from, or an interface a class implements. Its
promises are what a caller written against the base can rely on: the arguments each
method accepts and uses, what it returns, the errors it raises, and the work it does.
A promise is read from the base's code in the file under review: its signature, its
body, and its docstring or comment. A method the base leaves for subclasses to supply,
with no body of its own (abstract, a protocol or interface member, or a body that only
raises "not implemented"), promises its signature and docstring and nothing more.

An override is a method of the subclass with the same name as a method of the base.

## Violation

An override, in a class whose base is in the file under review, that breaks a promise
of the base's method:

- it raises an error the base's method doesn't raise or document, for input the base
  accepts, such as an "unsupported" or "not allowed" error;
- it ignores an argument the base's method uses, so a caller's argument has no effect;
- it accepts less: it rejects, or does nothing for, input the base's method handles;
- it returns less: nothing, or a looser or emptier value, where the base's method
  returns a value;
- it stubs the inherited method out: a body that only passes, returns nothing or a
  constant, where the base's method does work.

Report it at the override.

## Not a violation

- An override that keeps the base's promises and adds to them: it calls the base's
  method and does more, or does the same work another way.
- An override that accepts more or returns a narrower value than the base.
- An implementation of a method the base leaves for subclasses to supply.
- An override that raises an error the base's method raises or documents.
- A class whose base is not in the file under review: its promises can't be read here.
- A test double: a fake, stub or mock class standing in for the base in tests.

## Why

Code written against the base calls the subclass without knowing it. When the subclass
breaks a promise, that caller fails far from the override that broke it, and the bug
shows up only for the one subclass, so every caller has to learn which subclasses it
can trust and check for them.

Source: the Liskov substitution principle (Barbara Liskov, "Data Abstraction and
Hierarchy", 1987; Robert C. Martin, *Agile Software Development*, 2002), and Refused
Bequest (Martin Fowler, *Refactoring*, 1999).
