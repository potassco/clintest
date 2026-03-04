from abc import abstractmethod
from typing import List, Protocol, Sequence

import clingo


class Model(Protocol):
    @property
    @abstractmethod
    def cost(self) -> List[int]:
        pass

    @property
    @abstractmethod
    def number(self) -> int:
        pass

    @property
    @abstractmethod
    def optimality_proven(self) -> bool:
        pass

    @property
    @abstractmethod
    def priority(self) -> List[int]:
        pass

    @property
    @abstractmethod
    def type(self) -> clingo.ModelType:
        pass

    @abstractmethod
    def contains(self, atom: clingo.Symbol) -> bool:
        pass

    @abstractmethod
    def symbols(
        self,
        atoms: bool = False,
        terms: bool = False,
        shown: bool = False,
        theory: bool = False,
        # complement: bool = False
    ) -> Sequence[clingo.Symbol]:
        pass
