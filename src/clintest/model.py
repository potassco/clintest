from abc import abstractmethod
from typing import List, Protocol, Self, Sequence, override

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
        complement: bool = False
    ) -> Sequence[clingo.Symbol]:
        pass


class PersistedModel(Model):
    def __init__(
        self,
        cost: List[int] = [],
        number: int = 0,
        optimality_proven: bool = False,
        priority: List[int] = [],
        type: clingo.ModelType = clingo.ModelType.StableModel,
        symbols: dict[str, Sequence[clingo.Symbol]] = {
            "atoms": [],
            "terms": [],
            "shown": [],
            "theory": [],
        },
    ) -> None:
        self.__cost = cost
        self.__number = number
        self.__optimality_proven = optimality_proven
        self.__priority = priority
        self.__type = type
        self.__symbols = symbols

    def __str__(self) -> str:
        return " ".join(map(str, self.symbols(shown=True)))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"cost={self.cost!r}, "
            f"number={self.number!r}, "
            f"optimality_proven={self.optimality_proven!r}, "
            f"priority={self.priority!r}, "
            f"type={self.type!r}, "
            f"symbols={self.__symbols!r}"
            ")"
        )

    @classmethod
    def of(cls, model: Model) -> Self:
        return cls(
            cost=model.cost,
            number=model.number,
            optimality_proven=model.optimality_proven,
            priority=model.priority,
            type=model.type,
            symbols={
                "atoms": model.symbols(atoms=True),
                "terms": model.symbols(terms=True),
                "shown": model.symbols(shown=True),
                "theory": model.symbols(theory=True),
            },
        )

    @property
    @override
    def cost(self) -> List[int]:
        return self.__cost

    @property
    @override
    def number(self) -> int:
        return self.__number

    @property
    @override
    def optimality_proven(self) -> bool:
        return self.__optimality_proven

    @property
    @override
    def priority(self) -> List[int]:
        return self.__priority

    @property
    @override
    def type(self) -> clingo.ModelType:
        return self.__type

    @override
    def contains(self, atom: clingo.Symbol) -> bool:
        # return atom in self.__symbols["atoms"]
        raise NotImplementedError()

    @override
    def symbols(
        self,
        atoms: bool = False,
        terms: bool = False,
        shown: bool = False,
        theory: bool = False,
        complement: bool = False
    ) -> Sequence[clingo.Symbol]:
        if complement:
            raise NotImplementedError("Complement of symbols is not implemented for PersistedModel.")

        result = []
        if atoms:
            result.extend(self.__symbols["atoms"])
        if terms:
            result.extend(self.__symbols["terms"])
        if shown:
            result.extend(self.__symbols["shown"])
        if theory:
            result.extend(self.__symbols["theory"])
        return result
