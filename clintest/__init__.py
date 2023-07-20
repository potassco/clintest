"""
A test framework for `clingo` programs.

`clintest` enables you to write efficient unit tests for `clingo` programs.
In order to archive this, it will monitor the outcome of your test while running the solver to obtain solutions to your program.
Once the outcome of the test becomes certain, it will automatically abort the solving process to not waste any time with unnecessary computations.

This framework also enables you to write unit tests quickly.
It provides you with the necessary building blocks to assemble the most commonly used tests from predefined parts.
Thus, it saves you the hassle of writing boilerplate yourself that would otherwise drain your time.

`clintest` is a library written in Python that focusses on the specifics of `clingo` programs.
If you are looking after functionalities that are more general to unit testing, you may want to combine `clintest` with a framework like `pytest`.

There is currently no application called `clintest` but we may provide one in the future.

## Installation
This framework is guaranteed to work with Python 3.8 or greater. You have several options to install it:

### Using conda
TODO

### Using pip
TODO

### From source
TODO

## Quickstart
This section is meant to introduce you to the most important features of `clintest` using a simple example.
Imagine you have written the program `a. {b}.` and want to ensure that all its models contain the atom `a`.
In order to do so, you first need to create a test.

```
from clintest.test import Assert
from clintest.quantifier import All
from clintest.assertion import Contains

test = Assert(All(), Contains("a"))
```

The test `test.Assert` reviews the models of a program.
It needs to be initialized with an assertion (here: `assertion.Contains`) that may or may not hold for a certain model and a quantifier (here: `quantifier.All`) that specifies how often the assertion must hold to pass the test.

Tests retain their own outcome which can be queried as follows.

>>> print(test.outcome())
T?

The outcome of a test may either be

  - possibly false (`F?`),
  - possibly true (`T?`),
  - certainly false (`F!`), or
  - certainly true (`T!`).

Here, the outcome is possibly true (`T?`) as the test did not yet run but would succeed if no (further) model would be given.
In order to run the test, we need to create a solver.

```
from clintest.solver import Clingo
solver = Clingo("0", "a. {b}.")
```

The solver `solver.Clingo` is a facade around `clingo.control.Control` which is initialized with list of arguments (here: `"0"`, meaning that the solver should compute all models) and the program (here: `"a. {b}."`).
Once a solver is set up, it may solve your test as follows.

>>> solver.solve(test)
>>> print(test.outcome())
T!

As you realize from the output, any model of `a. {b}.` does indeed contain the atom `a`.
In case you want to check this within a framework like `pytest`, use the functions `outcome.Outcome` provides and the keyword `assert`.

```
assert test.outcome().is_certainly_true()
```

## Assembling compound tests
Testing real-world programs would still require a lot of boilerplate, if `clintest` had no support for combining simple tests into more complex ones.
The following example illustrates how to build a test that simultaneously ensures

  - any model contains the atom `a`,
  - all models contain the atom `b`, and
  - any model contains the atom `c`.

```
from clintest.test import Assert, And
from clintest.quantifier import All, Any
from clintest.assertion import Contains

test = And(
    Assert(Any(), Contains("a")),
    Assert(All(), Contains("b")),
    Assert(Any(), Contains("c")),
)
```

Solving this test with our previous solver leads to the following result.

>>> solver.solve(test)
>>> print(test)
[F!] And
    operands:
         0: [T!] Assert
            quantifier: Any
            assertion:  Contains("a")
         1: [F!] Assert
            quantifier: All
            assertion:  Contains("b")
         2: [F?] Assert
            quantifier: Any
            assertion:  Contains("c")
    short_circuit:  True
    ignore_certain: True

Printing the whole test (instead of merely the outcome) provides you with a more detailed report revealing some details about the inner workings of your tests.
For a start, you may discover that test #2 did not run to completion as its outcome is still possibly false (`F?`).
This is an intensional optimization as the outcome of test #2 was irrelevant for the whole test once test #1 was certainly false (`F!`).

## Inner workings of clintest
TODO
"""
