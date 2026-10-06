---
icon: lucide/wrench
---

# Custom Tests

Sooner or later, you may need a check that the built-in components cannot express.
In that case, you can write your own component, and it will work alongside the built-in ones just fine.

Before writing a whole test, check whether a custom assertion or quantifier is enough.
They are less work and plug right into [`Assert`][clintest.test.Assert].

## Custom assertions

An assertion extends [`Assertion`][clintest.assertion.Assertion] and implements a single method, [`holds_for`][clintest.assertion.Assertion.holds_for].
It receives a model and returns whether the assertion holds for it.

For example, the following assertion holds if a model shows at most `n` symbols:

```python
from typing import override

from clintest.assertion import Assertion
from clintest.protocol import Model


class AtMost(Assertion):
    def __init__(self, n: int) -> None:
        self.__n = n

    def __repr__(self):
        return f"AtMost({self.__n})"

    @override
    def holds_for(self, model: Model) -> bool:
        return len(model.symbols(shown=True)) <= self.__n
```

The `__repr__` method is optional, but it makes the error message readable.
You can use the new assertion like any other:

```python
from clintest.quantifier import All
from clintest.solver import Clingo
from clintest.test import Assert

solver = Clingo(["0"], "a. {b}.")
test = Assert(All(), AtMost(1))
solver.solve(test)
```

```pycon
>>> print(test)
[F!] Assert
    quantifier: Finished
    assertion:  AtMost(1)
```

The test fails because the model `{a, b}` shows two symbols.

## Custom quantifiers

A quantifier extends [`Quantifier`][clintest.quantifier.Quantifier] and implements two methods:

1. [`consume`][clintest.quantifier.Quantifier.consume] receives whether the assertion holds for the next model and returns the updated outcome.
2. [`outcome`][clintest.quantifier.Quantifier.outcome] returns the current outcome.

Make the outcome certain as soon as further models cannot change it.
This allows clintest to stop the solver early.
Once the outcome is certain, it must not change anymore.

You do not need to handle the end of solving yourself.
`Assert` takes care of that by making the quantifier's current outcome certain.

For inspiration, have a look at the built-in quantifiers in [`clintest.quantifier`][clintest.quantifier].

## Custom tests

If neither a custom assertion nor a custom quantifier is enough, you can write a whole test.
A test extends [`Test`][clintest.test.Test] and implements two methods, though a third one is often needed:

1. [`outcome`][clintest.test.Test.outcome] may be called at any time and returns the current outcome of the test.
   Once the outcome is certain, it must not change anymore.
2. [`on_finish`][clintest.test.Test.on_finish] is called once solving comes to an end.
   This is your last chance to change the outcome.
   Afterwards, the outcome must be certain.
3. [`on_model`][clintest.test.Test.on_model] is optional and called for each model.
   It returns whether the test needs further models.
   If it returns `False`, the outcome must be certain.

For example, the following test checks that a program has no models:

```python
from typing import override

from clintest.outcome import Outcome
from clintest.protocol import Model, SolveResult
from clintest.test import Test


class Unsatisfiable(Test):
    def __init__(self) -> None:
        self.__outcome = Outcome(True, False)

    def __str__(self):
        return f"[{self.outcome()}] Unsatisfiable"

    @override
    def on_model(self, model: Model) -> bool:
        self.__outcome = Outcome(False, True)
        return False

    @override
    def on_finish(self, result: SolveResult) -> None:
        self.__outcome = Outcome(self.__outcome.current_value(), True)

    @override
    def outcome(self) -> Outcome:
        return self.__outcome
```

An [`Outcome`][clintest.outcome.Outcome] is created from its current value and whether it is certain.
The test starts out possibly true.
The first model makes it certainly false, so it no longer needs further models.
If solving ends without a model, `on_finish` makes the outcome certain, and the test passes.

```python
solver = Clingo(["0"], "a. :- a.")
test = Unsatisfiable()
solver.solve(test)
test.assert_()
```

There are further `on_*` methods you may override, for example to inspect statistics.
See [`Test`][clintest.test.Test] for details, and the built-in tests in [`clintest.test`][clintest.test] for inspiration.

!!! tip "Use built-in components where possible"

    The example in this section is meant to show how a custom test works.
    In practice, you do not need it, because the same check can be composed from built-in components:

    ```python
    from clintest.assertion import True_
    from clintest.quantifier import Exact

    test = Assert(Exact(0), True_())
    ```

    The assertion [`True_`][clintest.assertion.True_] holds for every model, so this test demands that there are exactly zero models.

## Contributing

If you have built something that could benefit other users as well, we encourage you to open an issue or submit a pull request on [GitHub](https://github.com/potassco/clintest).
We are happy to consider including your idea in clintest.
