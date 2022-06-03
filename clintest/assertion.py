from abc import ABC, abstractmethod
from clingo.solving import Model
from clingo.symbol import Symbol

class Assertion(ABC):
    def __init__(self, description: str):
        self._description: str = description

    def __str__(self) -> str:
        return self._description

    @abstractmethod
    def holds_for(self, model: Model) -> bool:
        pass

class True_(Assertion):
    def __init__(self, description: str = "True"):
        super().__init__(description)

    def holds_for(self, model: Model) -> bool:
        return True

class False_(Assertion):
    def __init__(self, description: str = "False"):
        super().__init__(description)

    def holds_for(self, model: Model) -> bool:
        return False
