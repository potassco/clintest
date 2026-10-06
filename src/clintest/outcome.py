"""The [`Outcome`][clintest.outcome.Outcome] of a test, accessible via [`Test.outcome()`][clintest.test.Test.outcome].

The outcome of a test may be either

- `F?` (possibly false),
- `T?` (possibly true),
- `F!` (certainly false), or
- `T!` (certainly true).

These four options are represented using two booleans within [`Outcome`][clintest.outcome.Outcome]:

- [`current_value`][clintest.outcome.Outcome.current_value] stores the actual result of the test.
- [`is_certain`][clintest.outcome.Outcome.is_certain] indicates whether the result is certain.
"""

from typing import Tuple


class Outcome:
    """The outcome of a test."""

    def __init__(self, current_value: bool, is_certain: bool) -> None:
        """Initialize the outcome with current value and certainty.

        Args:
            current_value: The actual result of the test.
            is_certain: Whether `current_value` is certain.
        """
        self.__current_value = current_value
        self.__is_certain = is_certain

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__current_value}, {self.__is_certain})"

    def __str__(self):
        return str(self.__current_value)[:1] + ["?", "!"][self.__is_certain]

    def __eq__(self, other):
        # pylint: disable=protected-access
        return self.__current_value == other.__current_value and self.__is_certain == other.__is_certain

    def __hash__(self):
        return hash((self.__current_value, self.__is_certain))

    def current_value(self) -> bool:
        """Return the current value of this outcome."""
        return self.__current_value

    def is_certain(self) -> bool:
        """Return whether this outcome is certain."""
        return self.__is_certain

    def as_tuple(self) -> Tuple[bool, bool]:
        """Return this outcome as a tuple `(self.current_value(), self.is_certain())`."""
        return (self.__current_value, self.__is_certain)

    def is_certainly_true(self) -> bool:
        """Return whether this outcome is certainly true, i.e., both certain and currently true."""
        return self.__is_certain and self.__current_value

    def is_certainly_false(self) -> bool:
        """Return whether this outcome is certainly false, i.e., both certain and currently false."""
        return self.__is_certain and not self.__current_value
