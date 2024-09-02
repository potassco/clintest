"""
The abstract class `clintest.quantifier.Quantifier` and classes extending it.
"""

from abc import ABC, abstractmethod

from .outcome import Outcome


class Quantifier(ABC):
    """
    A quantifier specifies how many assertions must hold in order to pass the test.
    As such, one is necessary to assemble the `clintest.test.Assert` test.

    Quantifiers are stateful.
    They consume the return values of `clintest.assertion.Assertion.holds_for` and store all the
    information necessary to determine the current outcome of the test.
    """

    @abstractmethod
    def outcome(self) -> Outcome:
        """
        Returns the current outcome of this quantifier.
        """

    @abstractmethod
    def consume(self, value: bool) -> Outcome:
        """
        Consume the return value of `clintest.assertion.Assertion.holds_for` and possibly alter the
        current outcome of this quantifier.

        Parameters
        ----------
        value
            The return value of `clintest.assertion.Assertion.holds_for`.

        Returns
        -------
        The outcome of this quantifier after `value` was consumed.
        """


class All(Quantifier):
    """
    A quantifier demanding that an assertion holds for all models.
    """

    def __init__(self) -> None:
        self.__state = Outcome(True, False)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def __str__(self):
        return self.__class__.__name__

    def outcome(self) -> Outcome:
        return self.__state

    def consume(self, value: bool) -> Outcome:
        if not value:
            self.__state = Outcome(False, True)
        return self.__state


class Any(Quantifier):
    """
    A quantifier demanding that an assertion holds for any model.
    """

    def __init__(self) -> None:
        self.__state = Outcome(False, False)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def __str__(self):
        return self.__class__.__name__

    def outcome(self) -> Outcome:
        return self.__state

    def consume(self, value: bool) -> Outcome:
        if value:
            self.__state = Outcome(True, True)
        return self.__state


class Exact(Quantifier):
    """
    A quantifier demanding that an assertion holds for an exact number of models.

    Parameters
    ----------
    target
        The number of models the assertion should hold for
    """

    def __init__(self, target: int) -> None:
        self.__target = target
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__target}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__target}"

    def outcome(self) -> Outcome:
        return Outcome(self.__state == self.__target, self.__state > self.__target)

    def consume(self, value: bool) -> Outcome:
        self.__state += value
        return self.outcome()


class Less(Quantifier):
    """
    A quantifier demanding that an assertion holds for a number of models less than a given supremum.

    Parameters
    ----------
    supremum
        The supremum
    """

    def __init__(self, supremum: int) -> None:
        self.__supremum = supremum
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__supremum}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__supremum}"

    def outcome(self) -> Outcome:
        return Outcome(self.__state < self.__supremum, self.__state >= self.__supremum)

    def consume(self, value: bool) -> Outcome:
        self.__state += value
        return self.outcome()


class LessEqual(Quantifier):
    """
    A quantifier demanding that an assertion holds for a number of models less than or equal to a given maximum.

    Parameters
    ----------
    maximum
        The maximum
    """

    def __init__(self, maximum: int) -> None:
        self.__maximum = maximum
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__maximum}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__maximum}"

    def outcome(self) -> Outcome:
        return Outcome(self.__state <= self.__maximum, self.__state > self.__maximum)

    def consume(self, value: bool) -> Outcome:
        self.__state += value
        return self.outcome()


class Greater(Quantifier):
    """
    A quantifier demanding that an assertion holds for a number of models greater than a given infimum.

    Parameters
    ----------
    supremum
        The infimum
    """

    def __init__(self, infimum: int) -> None:
        self.__infimum = infimum
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__infimum}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__infimum}"

    def outcome(self) -> Outcome:
        return Outcome(self.__state > self.__infimum, self.__state > self.__infimum)

    def consume(self, value: bool) -> Outcome:
        self.__state += value
        return self.outcome()


class GreaterEqual(Quantifier):
    """
    A quantifier demanding that an assertion holds for a number of models than or equal to a given minimum.

    Parameters
    ----------
    supremum
        The minimum
    """

    def __init__(self, minimum: int) -> None:
        self.__minimum = minimum
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__minimum}, __state={self.__state})"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__state}/{self.__minimum}"

    def outcome(self) -> Outcome:
        return Outcome(self.__state >= self.__minimum, self.__state >= self.__minimum)

    def consume(self, value: bool) -> Outcome:
        self.__state += value
        return self.outcome()


class Finished(Quantifier):
    """
    A wrapper around an `inner` quantifier indicating that computation has finished.
    The outcome of this quantifier is the outcome of `inner` beside that it is always certain.
    Calling `Finished.consume` will not alter outcome of this or the `inner` quantifier.

    Parameters
    ---------
    inner
        The quantifier that should be finished.
    """

    def __init__(self, inner: Quantifier) -> None:
        self.__state = Outcome(inner.outcome().current_value(), True)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def __str__(self):
        return self.__class__.__name__

    def outcome(self) -> Outcome:
        return self.__state

    def consume(self, value: bool) -> Outcome:
        return self.__state
