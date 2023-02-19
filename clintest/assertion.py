from abc import ABC, abstractmethod
from clingo.solving import Model


class Assertion(ABC):
    @abstractmethod
    def holds_for(self, model: Model) -> bool:
        pass
