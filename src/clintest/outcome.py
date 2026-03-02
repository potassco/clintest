"""
The `clintest.outcome.Outcome` of a test, accessible via `clintest.test.Test.outcome()`.

The outcome of a test may be either

- `F?` (possibly false),
- `T?` (possibly true),
- `F!` (certainly false), or
- `T!` (certainly true).

These four options are represented using two booleans within `Outcome`:

- `current_value` stores the actual result of the test.
- `is_certain` indicates whether the result is certain.
"""

from typing import Tuple

class Outcome:
    """
    The outcome of a test.

    Parameters
    ----------
    current_value
        The actual result of the test.
    is_certain
        Whether the `current_value` is certain.
    """

    def __init__(self, current_value: bool, is_certain: bool) -> None:
        self.__current_value = current_value
        self.__is_certain = is_certain

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__current_value}, {self.__is_certain})"

    def __str__(self):
        return str(self.__current_value)[:1] + ["?", "!"][self.__is_certain]

    def __eq__(self, other):
        # pylint: disable=protected-access
        return self.__current_value == other.__current_value \
            and self.__is_certain == other.__is_certain

    def current_value(self) -> bool:
        """
        Returns the `current_value` of this outcome.
        """

        return self.__current_value

    def is_certain(self) -> bool:
        """
        Returns whether this outcome `is_certain`.
        """

        return self.__is_certain

    def as_tuple(self) -> Tuple[bool, bool]:
        """
        Returns this outcome as a tuple `(current_value, is_certain)`.
        """

        return (self.__current_value, self.__is_certain)

    def is_certainly_true(self) -> bool:
        """
        Returns whether this outcome is certainly true, i.e., if `is_certain and current_value` holds.
        """

        return self.__is_certain and self.__current_value

    def is_certainly_false(self) -> bool:
        """
        Returns whether this outcome is certainly false, i.e., if `is_certain and not current_value` holds.
        """

        return self.__is_certain and not self.__current_value
