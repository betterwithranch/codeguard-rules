# In TypeScript

A type is a class, interface or type alias the program defines. Types are often
interfaces with functions beside them, so a type's module is the `.ts` file that
declares it, and a function exported from that file is in the type's module. A field
is a property read through the value (`invoice.dueOn`), including through destructuring.

## Violation

- An exported or local function in another file that reads two or more properties of
  one parameter of a program type and returns an answer from them.
- A class method in another file that works out an answer from the properties of a
  value it takes or holds, reading none of its own class's fields.
- An inline condition or calculation in a handler or component over two or more
  properties of one value.

## Not a violation

- A method of the class, or a function exported from the file that declares the
  interface or type.
- A call to such a function or method.
- An object literal, a DTO mapper or a JSX element that copies properties to show or
  send them.
