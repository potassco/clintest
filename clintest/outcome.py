from typing import Tuple

class Outcome:
    def __init__(self, current_value: bool, is_certain: bool) -> None:
        self.__current_value = current_value
        self.__is_certain = is_certain

    def __repr__(self):
        name = self.__class__.__module__ + "." +  self.__class__.__name__
        return f"{name}({self.__current_value}, {self.__is_certain})"

    def __str__(self):
        return str(self.__current_value) + ["?", "!"][self.__is_certain]

    def __eq__(self, other):
        return self.__current_value == other.__current_value and self.__is_certain == other.__is_certain

    def current_value(self) -> bool:
        return self.__current_value

    def is_certain(self) -> bool:
        return self.__is_certain

    def as_tuple(self) -> Tuple[bool, bool]:
        return (self.__current_value, self.__is_certain)

    def is_certainly_true(self) -> bool:
        return self.__is_certain and self.__current_value

    def is_certainly_false(self) -> bool:
        return self.__is_certain and not self.__current_value
