from abc import ABC, abstractmethod
from typing import Iterable, Tuple


class Quantifier(ABC):
    @abstractmethod
    def consume(self, value: bool) -> Tuple[bool, bool]:
        pass

    def consume_all(self, values: Iterable[bool]) -> Iterable[Tuple[bool, bool]]:
        return (self.consume(value) for value in values)


class All(Quantifier):
    def __init__(self) -> None:
        self.__state = (True, True)

    def consume(self, value: bool) -> Tuple[bool, bool]:
        if not value:
            self.__state = (False, False)
        return self.__state


class Any(Quantifier):
    def __init__(self) -> None:
        self.__state = (False, True)

    def consume(self, value: bool) -> Tuple[bool, bool]:
        if value:
            self.__state = (True, False)
        return self.__state


class Exact(Quantifier):
    def __init__(self, n: int) -> None:
        self.__target = n
        self.__state = 0

    def consume(self, value: bool) -> Tuple[bool, bool]:
        self.__state += value
        return (self.__state == self.__target, self.__state <= self.__target)
