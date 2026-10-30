---
name: discriminated-unions
description: A parsed union's parser picks each variant from one unique tag; a union of schema types a parser builds from data with no discriminator named, a variant with no literal tag, or two variants sharing a tag value is a violation.
---

# Discriminated Unions

A parsed union's parser picks each variant from one unique tag.

A parsed union is a union of schema types that a parser builds from outside data: a
field, alias or schema whose value may be any one of several models, records or object
schemas, each read from a request, a message, a file or a row.

A tag is a field every variant has, whose type in each variant is one literal value,
and the discriminator is that field named to the parser as the one that picks the
variant. The parser picks each variant from one unique tag when:

- the union names its discriminator to the parser;
- every variant declares the tag field, as one literal value;
- no two variants share a tag value.

## Violation

A parsed union the change adds or edits, or a variant of one it edits, that breaks any
of these.

Report a missing discriminator, and a variant with no tag field, on the union. Report a
variant's tag that isn't one literal value, or that repeats another variant's value, on
that variant's tag field.

## Not a violation

- A union of types the program builds itself and tells apart by type, such as a check
  of the class.
- A union of one type with an empty value, and a union of plain values: numbers,
  strings, dates.
- A union with one variant per possible input shape that the parser can't confuse,
  such as an object or a list of objects, or an object or a string.
- A form the parser itself refuses when the schema is built or first used, and a form a
  pattern rule reports. The language's supplement names both.

## Why

Without a tag the parser tries each variant in turn: parsing is slower, a payload that
fits two variants becomes whichever is tried first, and a payload that fits none fails
with an error per variant instead of one naming the tag. With the tag named, the parser
reads one field, picks the variant, and reports errors against that variant alone.

Source: schema libraries' documentation of discriminated unions.
