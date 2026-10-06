---
icon: lucide/blocks
---

# Building Tests

Every test in clintest is assembled from a few building blocks.
Here, you will learn what they are and how to combine them, building on the example from [Getting Started](getting_started.md).

## Tests and outcomes

A test is an instance of [`Test`][clintest.test.Test].
The simplest one is [`Assert`][clintest.test.Assert], which checks a property of the models of a program.

```python
from clintest.test import Assert
from clintest.quantifier import All
from clintest.assertion import Contains

test = Assert(All(), Contains("a"))
```

This test checks that all models contain the atom `a`.

Every test keeps track of its own outcome, which is one of the following:

- `F?`: possibly false
- `T?`: possibly true
- `F!`: certainly false
- `T!`: certainly true

An uncertain outcome means that the test is not complete yet.
Once the outcome is certain, it never changes again.
You can query the outcome at any time:

```pycon
>>> print(test.outcome())
T?
```

The test has not been run yet, so its outcome is still uncertain.
Since no model so far lacks the atom `a`, it is possibly true.

`Assert` combines an assertion (here: `Contains("a")`) with a quantifier (here: `All()`) into a test.
The next two sections introduce both in turn.

## Assertions

An [`Assertion`][clintest.assertion.Assertion] is a statement about a single model.
clintest provides the following assertions:

| Assertion | Holds if the model … |
|---|---|
| [`Contains(symbol)`][clintest.assertion.Contains] | contains the atom `symbol` |
| [`Equals(symbols)`][clintest.assertion.Equals] | shows exactly the symbols in `symbols` |
| [`SubsetOf(symbols)`][clintest.assertion.SubsetOf] | shows only symbols in `symbols` |
| [`SupersetOf(symbols)`][clintest.assertion.SupersetOf] | shows all symbols in `symbols` |
| [`Optimal()`][clintest.assertion.Optimal] | is proven to be optimal |

`Contains` checks all atoms of a model, while `Equals`, `SubsetOf`, and `SupersetOf` only look at the shown symbols.
This matters as soon as your program uses `#show`.

Symbols can be given as strings, such as `"p(1)"`, or as `clingo.Symbol` objects.

Assertions can be combined with [`Not`][clintest.assertion.Not], [`And`][clintest.assertion.And], [`Or`][clintest.assertion.Or], [`Implies`][clintest.assertion.Implies], and [`Equivalent`][clintest.assertion.Equivalent].
For example, the following assertion holds for every model that either lacks `b` or contains `a`:

```python
from clintest.assertion import Contains, Implies

assertion = Implies(Contains("b"), Contains("a"))
```

## Quantifiers

A [`Quantifier`][clintest.quantifier.Quantifier] decides for how many models the assertion must hold.
clintest provides the following quantifiers:

| Quantifier | The assertion must hold for … |
|---|---|
| [`All()`][clintest.quantifier.All] | all models |
| [`Any()`][clintest.quantifier.Any] | at least one model |
| [`First()`][clintest.quantifier.First] | the first model |
| [`Last()`][clintest.quantifier.Last] | the last model |
| [`Exact(target)`][clintest.quantifier.Exact] | exactly `target` models |
| [`Less(supremum)`][clintest.quantifier.Less] | fewer than `supremum` models |
| [`LessEqual(maximum)`][clintest.quantifier.LessEqual] | at most `maximum` models |
| [`Greater(infimum)`][clintest.quantifier.Greater] | more than `infimum` models |
| [`GreaterEqual(minimum)`][clintest.quantifier.GreaterEqual] | at least `minimum` models |

The quantifier also determines when the outcome becomes certain.
For example, `All` is certainly false as soon as one model violates the assertion, and `Any` is certainly true as soon as one model satisfies it.
Otherwise, the outcome only becomes certain once the solver has finished.

Quantifiers are stateful, so each test needs its own instance.

## Solvers

A [`Solver`][clintest.solver.Solver] runs a test.
Most of the time, you will use [`Clingo`][clintest.solver.Clingo]:

```python
from clintest.solver import Clingo

solver = Clingo(["0"], "a. {b}.")
```

Its constructor takes three optional arguments:

1. `arguments`: a list of command-line options for clingo.
   Here, `"0"` asks clingo for all models.
   Without it, clingo stops after the first model.
2. `program`: the program as a string.
3. `files`: a list of paths to files with additional program parts.

Calling `solve` runs the test and updates its outcome:

```pycon
>>> solver.solve(test)
>>> print(test.outcome())
T!
```

A test is updated in place and cannot be reset.
To run the same check again, create a new test.

If you want to test against a fixed list of models instead of running clingo, use [`Iterate`][clintest.solver.Iterate].

## Combining tests

Real-world programs need more than one check.
Instead of running each check separately, you can combine tests with [`And`][clintest.test.And], [`Or`][clintest.test.Or], and [`Not`][clintest.test.Not]:

```python
from clintest.test import Assert, And, Not
from clintest.quantifier import All, Any
from clintest.assertion import Contains

test = And(
    Assert(All(), Contains("a")),
    Not(Assert(Any(), Contains("c"))),
)
```

This test checks that all models contain `a` and that no model contains `c`.
All operands see the same models, so clingo only has to solve the program once.

Compound tests also decide when to stop.
`And` is certainly false as soon as one operand is certainly false, and `Or` is certainly true as soon as one operand is certainly true.
From then on, the remaining operands no longer matter, so clintest stops the solver.
This is why, in [Getting Started](getting_started.md#your-first-test), the last assertion was never completed.

You can turn this behavior off with `short_circuit=False`.
The remaining operands then keep running until their own outcomes are certain.
