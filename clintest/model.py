from abc import ABC, abstractmethod
from clingo.solving import ModelType
from clingo.symbol import Symbol
from typing import List, Sequence

class Model(ABC):
    @abstractmethod
    def cost(self) -> List[int]:
        pass

    @abstractmethod
    def number(self) -> int:
        pass

    @abstractmethod
    def optimality_proven(self) -> bool:
        pass

    @abstractmethod
    def type(self) -> ModelType:
        pass

    @abstractmethod
    def contains(self, atom: Symbol) -> bool:
        pass

    @abstractmethod
    def symbols(self) -> Sequence[Symbol]:
        pass

    @abstractmethod
    def persist(self):
        pass

class PersistentModel(Model):
    # TODO
    pass

class ClingoModel(Model):
    # TODO
    pass
