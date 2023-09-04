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
