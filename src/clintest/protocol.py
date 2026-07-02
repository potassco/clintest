"""Protocols for classes in `clingo`.

Many classes in clingo are neither designed to be created manually nor to be persisted.
The most notable example is `clingo.solving.Model`, which is only valid during the solve call that produced it.
Since a more hands-on approach is often desired for testing, this module provides placeholder
(aka [protocols](https://typing.python.org/en/latest/spec/protocol.html)) for these classes.
"""

from abc import ABC, abstractmethod
from typing import List, Protocol, Self, Sequence, override

import clingo


class Persisted(ABC):
    """An object that can be persisted beyond the lifetime the original was produced for."""

    @classmethod
    @abstractmethod
    def of(cls, original: Self) -> Self:
        """Create a persisted version of the given original.

        Parameters
        ----------
        original
            The original to persist.

        Returns:
        -------
        A persisted version of the given original.
        """
        pass

    @abstractmethod
    def modify(self, **kwargs) -> Self:
        """Create a new object with modified attributes.

        Parameters
        ----------
        kwargs
            The attributes to modify.

        Returns:
        -------
        A new object with the modified attributes.
        """
        pass


class Model(Protocol):
    """A protocol for the `clingo.solving.Model` class.

    This protocol allows tests to operate on models without being tied to the clingo
    implementation of a model. As a side effect, it enables users to persist models
    beyond the lifetime of the solve call that produced them using `PersistedModel`.
    """

    @property
    @abstractmethod
    def cost(self) -> List[int]:
        """Return the list of integer values of the cost vector."""

    @property
    @abstractmethod
    def number(self) -> int:
        """Return the running number of the model."""

    @property
    @abstractmethod
    def optimality_proven(self) -> bool:
        """Return whether the optimality of the model has been proven."""

    @property
    @abstractmethod
    def priority(self) -> List[int]:
        """Return the priority vector of the model."""

    @property
    @abstractmethod
    def type(self) -> clingo.ModelType:
        """Return the type of the model."""

    @abstractmethod
    def contains(self, atom: clingo.Symbol) -> bool:
        """Return whether the given atom is contained in the model.

        Parameters
        ----------
        atom
            The `clingo.Symbol` to check.
        """

    @abstractmethod
    def symbols(
        self,
        atoms: bool = False,
        terms: bool = False,
        shown: bool = False,
        theory: bool = False,
        complement: bool = False,
    ) -> Sequence[clingo.Symbol]:
        """Return the symbols in the model filtered by the given flags.

        Parameters
        ----------
        atoms
            Whether to include atoms.
        terms
            Whether to include terms.
        shown
            Whether to include shown atoms.
        theory
            Whether to include theory atoms.
        complement
            Whether to return the complement of the selected symbols.
        """


class PersistedModel(Model, Persisted):
    """A model that persists beyond the lifetime of the solve call that produced it.

    A `PersistedModel` can be created directly or from any `Model` using `PersistedModel.of`.

    Parameters
    ----------
    cost
        The list of integer values of the cost vector.
    number
        The running number of the model.
    optimality_proven
        Whether the optimality of the model has been proven.
    priority
        The priority vector of the model.
    type
        The type of the model.
    symbols
        A dictionary with keys ``"atoms"``, ``"terms"``, ``"shown"``, and ``"theory"``,
        each mapping to a sequence of `clingo.Symbol`s.
    """

    def __init__(  # noqa: PLR0913
        self,
        cost: List[int] | None = None,
        number: int = 0,
        optimality_proven: bool = False,
        priority: List[int] | None = None,
        type: clingo.ModelType = clingo.ModelType.StableModel,
        symbols: dict[str, Sequence[clingo.Symbol]] | None = None,
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
    @override
    def of(cls, model: Model) -> Self:
        """Create a `PersistedModel` from any `Model`.

        Parameters
        ----------
        model
            The `Model` to persist.

        Returns:
        -------
        A `PersistedModel` with the same data as `model`.
        """
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

    @classmethod
    def from_str(cls, repr: str) -> Self:
        """Create a `PersistedModel` from its string representation.

        Note that a conversion from a `PersistedModel` to its string representation is a lossy operation.
        Hence, this method does not guarantee that the resulting `PersistedModel` is equal to the original one.
        Instead, it will use sensible default to fill the gaps.

        Parameters
        ----------
        repr
            The string representation of the model.

        Returns:
        -------
        A `PersistedModel` with the same data as the string representation.
        """
        symbols = [clingo.parse_term(s) for s in repr.split()]
        return cls(
            symbols={
                "atoms": symbols,
                "terms": [],
                "shown": symbols,
                "theory": [],
            }
        )

    @override
    def modify(self, **kwargs) -> Self:
        """Create a new `PersistedModel` with modified attributes.

        Parameters
        ----------
        kwargs
            The attributes to modify. Valid keys are ``"cost"``, ``"number"``, ``"optimality_proven"``,
            ``"priority"``, ``"type"``, and ``"symbols"``.

        Returns:
        -------
        A new `PersistedModel` with the modified attributes.
        """
        return type(self)(
            cost=kwargs.get("cost", self.cost),
            number=kwargs.get("number", self.number),
            optimality_proven=kwargs.get("optimality_proven", self.optimality_proven),
            priority=kwargs.get("priority", self.priority),
            type=kwargs.get("type", self.type),
            symbols=kwargs.get("symbols", self.__symbols),
        )

    @property
    @override
    def cost(self) -> List[int]:  # noqa: D102
        return self.__cost

    @property
    @override
    def number(self) -> int:  # noqa: D102
        return self.__number

    @property
    @override
    def optimality_proven(self) -> bool:  # noqa: D102
        return self.__optimality_proven

    @property
    @override
    def priority(self) -> List[int]:  # noqa: D102
        return self.__priority

    @property
    @override
    def type(self) -> clingo.ModelType:  # noqa: D102
        return self.__type

    @override
    def contains(self, atom: clingo.Symbol) -> bool:  # noqa: D102
        return atom in self.__symbols["atoms"]

    @override
    def symbols(
        self,
        atoms: bool = False,
        terms: bool = False,
        shown: bool = False,
        theory: bool = False,
        complement: bool = False,
    ) -> Sequence[clingo.Symbol]:  # noqa: D102
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


class SolveResult(Protocol):
    """A protocol for the `clingo.solving.SolveResult` class.

    This protocol allows tests to operate on the result of a solve call without being tied
    to its clingo implementation.
    """

    @property
    @abstractmethod
    def exhausted(self) -> bool:
        """Determine if the search space was exhausted."""

    @property
    @abstractmethod
    def interrupted(self) -> bool:
        """Determine if the search space was interrupted."""

    @property
    @abstractmethod
    def satisfiable(self) -> bool:
        """`True` if the problem is satisfiable, `False` if the problem is unsatisfiable, `None` if the satisfiablity is not known."""  # noqa: E501

    @property
    def unknown(self) -> bool:
        """Determine if the satisfiablity is not known.

        This is equivalent to satisfiable is `None`.
        """
        return self.satisfiable is None

    @property
    @abstractmethod
    def unsatisfiable(self) -> bool:
        """`True` if the problem is unsatisfiable, `False` if the problem is satisfiable, `None` if the satisfiablity is not known."""  # noqa: E501
