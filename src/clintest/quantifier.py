"""The abstract class [`Quantifier`][clintest.quantifier.Quantifier] and classes extending it."""

from abc import ABC, abstractmethod
from typing import override

from .outcome import Outcome


class Quantifier(ABC):
    """A quantifier specifies which assertions must hold in order to pass the test.

    It is necessary to assemble the [`Assert`][clintest.test.Assert] test.

    Quantifiers are stateful.
    They consume the return values of [`Assertion.holds_for`][clintest.assertion.Assertion.holds_for] and store all the information necessary to determine the current outcome of the test.

    The current outcome describes whether the results consumed so far satisfy the quantifier.
    A certain outcome means that further results cannot change that value.
    When computation finishes, [`Assert`][clintest.test.Assert] wraps the quantifier in [`Finished`][clintest.quantifier.Finished] to make its current outcome certain.
    """

    @abstractmethod
    def outcome(self) -> Outcome:
        """Return the current outcome of this quantifier."""

    @abstractmethod
    def consume(self, value: bool) -> Outcome:
        """Consume `value`, a return value of [`Assertion.holds_for`][clintest.assertion.Assertion.holds_for].

        Possibly alters the current outcome of this quantifier.

        Args:
            value: The return value of [`Assertion.holds_for`][clintest.assertion.Assertion.holds_for].

        Returns:
            The outcome of this quantifier after `value` was consumed.
        """


class All(Quantifier):
    """A quantifier demanding that an assertion holds for all models.

    With no models, the current value is true.
    The outcome becomes certainly false as soon as the assertion fails for a model; otherwise it remains uncertain until computation finishes.
    """

    def __init__(self) -> None:
        """Initialize the quantifier before any models have been consumed."""
        self.__state = Outcome(True, False)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def __str__(self):
        return self.__class__.__name__

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__state

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        if not value:
            self.__state = Outcome(False, True)
        return self.__state


class Any(Quantifier):
    """A quantifier demanding that an assertion holds for at least one model.

    With no models, the current value is false.
    The outcome becomes certainly true as soon as the assertion holds for a model; otherwise it remains uncertain until computation finishes.
    """

    def __init__(self) -> None:
        """Initialize the quantifier before any models have been consumed."""
        self.__state = Outcome(False, False)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def __str__(self):
        return self.__class__.__name__

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__state

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        if value:
            self.__state = Outcome(True, True)
        return self.__state


class First(Quantifier):
    """A quantifier demanding that an assertion holds for the first model.

    With no models, the current value is false and uncertain.
    The first consumed result determines the certain outcome; subsequent results are ignored.
    """

    def __init__(self) -> None:
        """Initialize the quantifier before any models have been consumed."""
        self.__state = Outcome(False, False)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def __str__(self):
        return self.__class__.__name__

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__state

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        if not self.__state.is_certain():
            self.__state = Outcome(value, True)
        return self.__state


class Last(Quantifier):
    """A quantifier demanding that an assertion holds for the last model.

    With no models, the current value is false.
    Each consumed result replaces the current value, which remains uncertain until computation finishes.
    """

    def __init__(self) -> None:
        """Initialize the quantifier before any models have been consumed."""
        self.__state = Outcome(False, False)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def __str__(self):
        return self.__class__.__name__

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__state

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        self.__state = Outcome(value, False)
        return self.__state


class Exact(Quantifier):
    """A quantifier demanding that an assertion holds for an exact number of models.

    The current value is true when the count equals `target`.
    Reaching `target` does not make the outcome certain: another matching model can make it false.
    The outcome becomes certainly false when the count exceeds `target`.
    With no models, the current value is true only for `target` zero.
    """

    def __init__(self, target: int) -> None:
        """Initialize the quantifier with the target number of models `target`.

        Args:
            target: The exact number of models the assertion should hold for.
        """
        self.__target = target
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__target}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__target}"

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return Outcome(self.__state == self.__target, self.__state > self.__target)

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        self.__state += value
        return self.outcome()


class Less(Quantifier):
    """A quantifier demanding that an assertion holds for a number of models less than `supremum`.

    The bound is exclusive: the current value is true when the count is less than `supremum`.
    The outcome becomes certainly false when the count reaches or exceeds `supremum`.
    With no models, the current value is true only for a positive `supremum`.
    """

    def __init__(self, supremum: int) -> None:
        """Initialize the quantifier with `supremum`.

        Args:
            supremum: The exclusive upper bound on the number of models the assertion holds for.
        """
        self.__supremum = supremum
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__supremum}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__supremum}"

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return Outcome(self.__state < self.__supremum, self.__state >= self.__supremum)

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        self.__state += value
        return self.outcome()


class LessEqual(Quantifier):
    """A quantifier demanding that an assertion holds for a number of models less than or equal to `maximum`.

    The bound is inclusive: the current value is true when the count is at most `maximum`.
    The outcome becomes certainly false when the count exceeds `maximum`.
    With no models, the current value is true for a nonnegative `maximum`.
    """

    def __init__(self, maximum: int) -> None:
        """Initialize the quantifier with `maximum`.

        Args:
            maximum: The inclusive upper bound on the number of models the assertion holds for.
        """
        self.__maximum = maximum
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__maximum}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__maximum}"

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return Outcome(self.__state <= self.__maximum, self.__state > self.__maximum)

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        self.__state += value
        return self.outcome()


class Greater(Quantifier):
    """A quantifier demanding that an assertion holds for a number of models greater than `infimum`.

    The bound is exclusive: the outcome becomes certainly true when the count exceeds `infimum`.
    Below or at the bound, the current value is false and uncertain.
    With no models, the outcome is certainly true only for a negative `infimum`.
    """

    def __init__(self, infimum: int) -> None:
        """Initialize the quantifier with `infimum`.

        Args:
            infimum: The exclusive lower bound on the number of models the assertion holds for.
        """
        self.__infimum = infimum
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__infimum}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__infimum}"

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return Outcome(self.__state > self.__infimum, self.__state > self.__infimum)

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        self.__state += value
        return self.outcome()


class GreaterEqual(Quantifier):
    """A quantifier demanding that an assertion holds for a number of models greater than or equal to `minimum`.

    The bound is inclusive: the outcome becomes certainly true when the count reaches or exceeds `minimum`.
    Below the bound, the current value is false and uncertain.
    With no models, the outcome is certainly true for a nonpositive `minimum`.
    """

    def __init__(self, minimum: int) -> None:
        """Initialize the quantifier with `minimum`.

        Args:
            minimum: The inclusive lower bound on the number of models the assertion holds for.
        """
        self.__minimum = minimum
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__minimum}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__minimum}"

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return Outcome(self.__state >= self.__minimum, self.__state >= self.__minimum)

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        self.__state += value
        return self.outcome()


class Finished(Quantifier):
    """A wrapper around the quantifier `inner` indicating that computation has finished.

    The wrapper captures the current value of `inner` at construction and makes it certain, even if no models have been consumed.
    Calling [`Finished.consume`][clintest.quantifier.Finished.consume] will not alter the outcome of this or the `inner` quantifier.
    """

    def __init__(self, inner: Quantifier) -> None:
        """Initialize the wrapper with `inner`.

        Args:
            inner: The quantifier that should be finished.
        """
        self.__state = Outcome(inner.outcome().current_value(), True)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def __str__(self):
        return self.__class__.__name__

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__state

    @override
    def consume(self, value: bool) -> Outcome:  # noqa: D102
        """Return the finished outcome without consuming `value`."""
        return self.__state
