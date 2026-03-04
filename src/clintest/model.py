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
        complement: bool = False,
    ) -> Sequence[clingo.Symbol]:
        pass


class PersistedModel(Model):
    def __init__(  # noqa: PLR0913
        self,
        cost: List[int] = None,
        number: int = 0,
        optimality_proven: bool = False,
        priority: List[int] = None,
        type: clingo.ModelType = clingo.ModelType.StableModel,
        symbols: dict[str, Sequence[clingo.Symbol]] = None,
    ) -> None:
        self.__cost = cost if cost is not None else []
        self.__number = number
        self.__optimality_proven = optimality_proven
        self.__priority = priority if priority is not None else []
        self.__type = type
        self.__symbols = {
            "atoms": list(symbols["atoms"]) if symbols is not None and "atoms" in symbols else [],
            "terms": list(symbols["terms"]) if symbols is not None and "terms" in symbols else [],
            "shown": list(symbols["shown"]) if symbols is not None and "shown" in symbols else [],
            "theory": list(symbols["theory"]) if symbols is not None and "theory" in symbols else [],
        }

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

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, PersistedModel)
            and self.cost == other.cost
            and self.number == other.number
            and self.optimality_proven == other.optimality_proven
            and self.priority == other.priority
            and self.type == other.type
            and self.__symbols == other.__symbols
        )

    def __hash__(self) -> int:
        return hash(
            (
                tuple(self.cost),
                self.number,
                self.optimality_proven,
                tuple(self.priority),
                self.type,
                frozenset((key, tuple(value)) for key, value in self.__symbols.items()),
            )
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
        return atom in self.__symbols["atoms"]

    @override
    def symbols(
        self,
        atoms: bool = False,
        terms: bool = False,
        shown: bool = False,
        theory: bool = False,
        complement: bool = False,
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
