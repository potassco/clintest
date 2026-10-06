---
icon: lucide/rocket
---

# Getting Started

This chapter introduces clintest, shows you how to install it, and walks you through your first test.

## Why clintest?

clintest is a Python test framework that makes it easy to write efficient tests for clingo programs.
It comes with a wide range of ready-made components, so you can quickly assemble the most common tests instead of writing them from scratch.
If you need something more specific, you can write your own test, and it will work alongside the built-in ones just fine.

To avoid wasting time on unnecessary computation, clintest monitors the outcome of your test while it steers the solving process.
As soon as the outcome is certain, it tells the solver to stop searching for further solutions.

Since clintest focuses on the specifics of clingo programs, it works best in combination with a general-purpose test framework such as pytest.

## Installation

clintest requires Python 3.12 or later.
There are two ways to install it.

### Using pip

clintest is available on [PyPI](https://pypi.org/project/clintest) and can be installed with pip:

```
$ pip install clintest
```

### From source

The source code is hosted on [GitHub](https://github.com/potassco/clintest).
We recommend installing from source only if you plan to work on clintest itself.

```
$ git clone https://github.com/potassco/clintest
$ cd clintest
$ pip install -e ".[dev,doc]"
```

The features `dev` and `doc` install the dependencies for development and for building this documentation, respectively.

## Your first test

Let's test the program `a. {b}.`, which has two models: `{a}` and `{a, b}`.

--8<-- "README.md:example"

First, we create a solver that runs clingo on the program.
The argument `"0"` tells clingo to compute all models.
Next, we create the test.
It combines three assertions with `And`:

1. Some model contains `a`.
2. Every model contains `b`.
3. Some model contains `c`.

Then, the solver runs the test.
Finally, `test.assert_()` raises an `AssertionError` if the test has failed or is incomplete.

In this case, the test fails:

```
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
```

Each test is marked with its outcome.
`T` and `F` stand for true and false.
`!` means the outcome is certain, while `?` means it could still change if the solver found more models.

The first assertion is certainly true, because the first model already contains `a`.
The second one is certainly false, because the model `{a}` does not contain `b`.
At that point, the outcome of `And` is certain, so clintest stops the solver.
This is why the third assertion is only marked `F?`: no model seen so far contains `c`, but clintest never needed to look at all of them.
