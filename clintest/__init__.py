"""
A test framework for `clingo` programs.

`clintest` is a test framework written in Python that makes it easy to write efficient tests for `clingo` programs.
It provides you with numerous off-the-shelf components that allow you to assemble the most commonly used tests quickly, saving you the time to write them yourself.
However, should you require a hand-crafted test, it will work along the others just fine.

In order to avoid time wasted on unnecessary computations, `clintest` will monitor the outcome of your test while steering the solving process.
Once the outcome of your test is certain, it will automatically tell the solver to abort the search for further solutions.

As `clintest` is focussed on the specifics of `clingo` programs, it works best if you combine it with a general purpose frameworks like `pytest`.

## Installation
This framework is guaranteed to work with Python 3.8 or greater.
You have several options to install it:

### Using conda
TODO

### Using pip
TOOD

### From source
TODO

## Quick start
This section is meant to guide you through the most important features of `clintest` using simple examples.

### Simple assertions
Imagine you have written the program `a. {b}.` and want to ensure that all its models contains the atom `a`.
In order to do so, you first need to create a `test.Test`.

```
from clintest.test import Assert
from clintest.quantifier import All
from clintest.assertion import Contains

test = Assert(All(), Contains("a"))
```

The test `test.Assert` inspects the models of a program.
It needs to be initialized with an `assertion.Assertion` and a `quantifier.Quantifier`.
An assertion (here: `assertion.Contains`) is a statement that may or may not hold for a certain model.
A quantifier (here: `quantifier.All`) specifies how many assertions must hold in order to pass the test.

Tests retain their own outcome which may be either

  - `F?` (possibly false),
  - `T?` (possibly true),
  - `F!` (certainly false), or
  - `T!` (certainly true).

Having an uncertain outcome means that a test has not (yet) been completed.
Once the outcome is certain, it must no longer change in order for `clintest` to function properly.
The outcome of a test can be queried as follows.

>>> print(test.outcome())
T?

Due to the fact this test was never run, its outcome is still uncertain.
In order to run the test, we need to create a `solver.Solver` first.

```
from clintest.solver import Clingo
solver = Clingo("0", "a. {b}.")
```

The solver `solver.Clingo` is a facade around `clingo.control.Control`.
The constructor expects the program (here: `"a. {b}."`) and a list of arguments for the solver (here: `"0"`, meaning that the solver should compute all models).
Once a solver is set up, it may solve your test as follows.

>>> solver.solve(test)
>>> print(test.outcome())
T!

As you realize from the output, any model of `a. {b}.` does indeed contain the atom `a`.
If you want to ensure this within a framework like `pytest`, use `clintest.test.Test.assert_` to raise an `AssertionError` with a proper message if the test's outcome is not certainly true (`T!`).

```
test.assert_()
```

### Compound tests
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
>>> test.assert_()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "clintest/clintest/test.py", line 42, in assert_
    raise AssertionError(msg)
AssertionError: The following test has failed.
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

Because the test has failed, `clintest.test.Test.assert_` produces a rather detailed exception which may be used to explain the cause of the failure:
Test #1 did fail, probably because there was a model that did not contain the atom `b`.

But if you watch carefully, there is something else to discover.
Test #2 was never completed.
This is due to a deliberate optimization as the outcome of test #2 was irrelevant once the outcome of test #1 was certainly false (`F!`).

### Debugging
TODO

### Hand-crafted tests
TODO
"""
