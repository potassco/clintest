# clintest

A test framework for clingo programs, written in Python.

- **Ready-made components:** Assemble the most common tests from built-in assertions, quantifiers, and combinators.
- **Efficient:** clintest monitors your test while clingo is solving and stops the solver as soon as the outcome is certain.
- **Extensible:** Custom components work alongside the built-in ones.

## Installation

clintest requires Python 3.12 or later and can be installed with pip:

```
$ pip install clintest
```

## Example

<!-- --8<-- [start:example] -->
```python
from clintest.test import Assert, And
from clintest.quantifier import All, Any
from clintest.assertion import Contains
from clintest.solver import Clingo

solver = Clingo(["0"], "a. {b}.")
test = And(
    Assert(Any(), Contains("a")),
    Assert(All(), Contains("b")),
    Assert(Any(), Contains("c")),
)

solver.solve(test)
test.assert_()
```
<!-- --8<-- [end:example] -->

This test checks that some model contains `a`, all models contain `b`, and some model contains `c`.
It fails, because the model `{a}` does not contain `b`, and `test.assert_()` raises an `AssertionError` explaining why.

## Documentation

The [documentation](https://docs.potassco.org/clintest/) contains a guide and an API reference.

## License

clintest is released under the [MIT License](LICENSE).
