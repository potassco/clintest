from typing import Tuple

class Outcome:
    def __init__(self, current_value: bool, is_mutable: bool) -> None:
        self.__current_value = current_value
        self.__is_mutable = is_mutable

    def current_value(self) -> bool:
        return self.__current_value

    def is_mutable(self) -> bool:
        return self.__is_mutable

    def as_tuple(self) -> Tuple[bool, bool]:
        return (self.__current_value, self.__is_mutable)

    def is_immutably_true(self) -> bool:
        return not self.__is_mutable and self.__current_value

    def is_immutably_false(self) -> bool:
        return not self.__is_mutable and not self.__current_value
