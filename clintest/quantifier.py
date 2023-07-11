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
        self.__state = Outcome(True, False)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def outcome(self) -> Outcome:
        return self.__state

    def consume(self, value: bool) -> Outcome:
        if not value:
            self.__state = Outcome(False, True)
        return self.__state


class Any(Quantifier):
    def __init__(self) -> None:
        self.__state = Outcome(False, False)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def outcome(self) -> Outcome:
        return self.__state

    def consume(self, value: bool) -> Outcome:
        if value:
            self.__state = Outcome(True, True)
        return self.__state


class Exact(Quantifier):
    def __init__(self, target: int) -> None:
        self.__target = target
        self.__state = 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__target}, __state={self.__state})"

    def outcome(self) -> Outcome:
        return Outcome(self.__state == self.__target, self.__state > self.__target)

    def consume(self, value: bool) -> Outcome:
        self.__state += value
        return self.outcome()


class Finished(Quantifier):
    def __init__(self, inner: Quantifier) -> None:
        self.__state = Outcome(inner.outcome().current_value(), True)

    def __repr__(self):
        name = self.__class__.__name__
        state = repr(self.__state)
        return f"{name}(__state={state})"

    def outcome(self) -> Outcome:
        return self.__state

    def consume(self, value: bool) -> Outcome:
        return self.__state
