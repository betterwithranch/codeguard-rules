---
name: no-shotgun-surgery
description: One type owns each job on a concept; a type the change adds or edits whose public method does a job another type of the program already does to the same concept is a violation.
---

# No Shotgun Surgery

One type owns each job on a concept.

A concept is a domain thing the program models: an order, a parcel, a subscription, a
password. A job is what a public method does to a concept: price it, validate it,
schedule it, send it, or work out a figure about it such as a total, a due date or a
summary. Two types own the same job when each has a public method doing that job to the
same concept, whatever the types, the methods or their bodies are called, and even when
their bodies differ: two methods that each work out a parcel's shipping cost own one
job, though one of them also rounds the result.

The other type is in the file under review or in another module of the program. Search
the program for the concept's name and the job's verb and its synonyms to find it, and
read its module to compare.

## Violation

A type the change adds or edits whose public method does a job that another type of the
program already does to the same concept, without calling that type to do it.

Report it at the second type's method, the one the change adds or edits.

## Not a violation

- A method that calls the owning type to do the job, with steps of its own around the
  call.
- Two types doing different jobs on one concept: one prices orders, the other ships
  them.
- The same job on different concepts: validating a password and validating an email
  address.
- Implementations of one interface or subclasses of one base, each doing the job the
  interface or base declares in its own way.
- A method that builds an instance of the concept: a separate rule judges where
  construction lives.
- Two passive shapes with the same fields: a separate rule judges copies.
- A private method or helper.

## Why

When two types own one job, a fix or a new requirement lands in the one the developer
finds, and the other keeps the old behaviour: each owner gets half the fixes, and the
program gives two answers to one question.

Source: Martin Fowler, *Refactoring* (1999), Shotgun Surgery; Craig Larman, *Applying UML
and Patterns* (1997), Information Expert.
