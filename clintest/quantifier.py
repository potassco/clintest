from abc import ABC, abstractmethod

from .outcome import Outcome


class Quantifier(ABC):
    @abstractmethod
    def outcome(self) -> Outcome:
        pass

    @abstractmethod
    def consume(self, value: bool) -> Outcome:
        pass


class All(Quantifier):
    def __init__(self) -> None:
        self.__state = Outcome(True, True)

    def outcome(self) -> Outcome:
        return self.__state

    def consume(self, value: bool) -> Outcome:
        if not value:
            self.__state = Outcome(False, False)
        return self.__state


class Any(Quantifier):
    def __init__(self) -> None:
        self.__state = Outcome(False, True)

    def outcome(self) -> Outcome:
        return self.__state

    def consume(self, value: bool) -> Outcome:
        if value:
            self.__state = Outcome(True, False)
        return self.__state


class Exact(Quantifier):
    def __init__(self, target: int) -> None:
        self.__target = target
        self.__state = 0

    def outcome(self) -> Outcome:
        return Outcome(self.__state == self.__target, self.__state <= self.__target)

    def consume(self, value: bool) -> Outcome:
        self.__state += value
        return self.outcome()
