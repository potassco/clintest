"""Protocols for classes in clingo.

Many classes in clingo are neither designed to be created manually nor to be persisted.
The most notable example is `clingo.solving.Model`, which is only valid during the solve call that produced it.
Since a more hands-on approach is often desired for testing, this module provides placeholders (aka [protocols](https://typing.python.org/en/latest/spec/protocol.html)) for these classes.
"""

from abc import abstractmethod
from typing import Any, List, Optional, Protocol, Self, Sequence, override

import clingo


class Model(Protocol):
    """A protocol for clingo's model class.

    See `clingo.solving.Model`.

    This protocol allows tests to operate on models without being tied to the clingo implementation of a model.
    As a side effect, it enables users to persist models beyond the lifetime of the solve call that produced them using [`PersistedModel`][clintest.protocol.PersistedModel].
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
        """Return whether `atom` is contained in the model.

        Args:
            atom: The atom to check for membership in the model.

        Returns:
            Whether `atom` is contained in the model.
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

        Args:
            atoms: Whether to include atoms.
            terms: Whether to include terms.
            shown: Whether to include shown atoms.
            theory: Whether to include theory atoms.
            complement: Whether to return the complement of the selected symbols.

        Returns:
            The symbols selected by the given flags.
        """


class PersistedModel(Model):
    """A model that persists beyond the lifetime of the solve call that produced it.

    Instances can be created directly or from any [`Model`][clintest.protocol.Model] using [`PersistedModel.of`][clintest.protocol.PersistedModel.of].

    Unlike clingo models, [`PersistedModel.symbols`][clintest.protocol.PersistedModel.symbols] does not support `complement=True`.
    """

    def __init__(  # noqa: PLR0913, PLR0917
        self,
        cost: List[int] | None = None,
        number: int = 0,
        optimality_proven: bool = False,
        priority: List[int] | None = None,
        type: clingo.ModelType = clingo.ModelType.StableModel,
        symbols: dict[str, Sequence[clingo.Symbol]] | None = None,
    ) -> None:
        """Initialize the persisted model with its properties and symbols.

        Args:
            cost: The optimization cost vector.
            number: The running number of the model.
            optimality_proven: Whether the optimality of the model has been proven.
            priority: The priority vector of the model.
            type: The type of the model.
            symbols: The symbols grouped under the keys `"atoms"`, `"terms"`, `"shown"`, and `"theory"`.
        """
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
        """Create a `PersistedModel` from `model`.

        Args:
            model: The model whose data should be persisted.

        Returns:
            A persisted copy of `model`'s data.
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
        """Create a `PersistedModel` from the string representation `repr`.

        Note that a conversion from a persisted model to its string representation is a lossy operation.
        Hence, this method does not guarantee that the resulting model is equal to the original one.
        Instead, it uses sensible defaults to fill the gaps.

        Args:
            repr: The string representation of the model.

        Returns:
            A model containing the represented symbols, with defaults for the remaining properties.
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

    def modify(self, **kwargs: Any) -> Self:
        """Create a new `PersistedModel` with modified attributes.

        Args:
            **kwargs: The attributes to modify.
                Valid keys are `"cost"`, `"number"`, `"optimality_proven"`, `"priority"`, `"type"`, and `"symbols"`.

        Returns:
            A new model with the requested changes and all other attributes preserved.
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
    ) -> Sequence[clingo.Symbol]:
        """Return the persisted symbols selected by the given flags.

        Args:
            atoms: Whether to include atoms.
            terms: Whether to include terms.
            shown: Whether to include shown atoms.
            theory: Whether to include theory atoms.
            complement: Must be `False`; complements are not supported for persisted models.

        Returns:
            The symbols selected by the given flags.

        Raises:
            NotImplementedError: If `complement` is `True`.
        """
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
    """A protocol for clingo's solve result class.

    See `clingo.solving.SolveResult`.

    This protocol allows tests to operate on the result of a solve call without being tied to its clingo implementation.
    """

    @property
    @abstractmethod
    def exhausted(self) -> bool:
        """Return whether the search space was exhausted."""

    @property
    @abstractmethod
    def interrupted(self) -> bool:
        """Return whether solving was interrupted."""

    @property
    @abstractmethod
    def satisfiable(self) -> Optional[bool]:
        """Return the satisfiability status of the problem.

        The value is `True` if satisfiable, `False` if unsatisfiable, and `None` if satisfiability is unknown.
        """

    @property
    def unknown(self) -> bool:
        """Return whether satisfiability is unknown.

        This is equivalent to `self.satisfiable is None`.
        """
        return self.satisfiable is None

    @property
    @abstractmethod
    def unsatisfiable(self) -> Optional[bool]:
        """Return the unsatisfiability status of the problem.

        The value is `True` if unsatisfiable, `False` if satisfiable, and `None` if satisfiability is unknown.
        """


class PersistedSolveResult(SolveResult):
    """A solve result that persists beyond the lifetime of the solve call that produced it.

    Instances can be created directly or from any [`SolveResult`][clintest.protocol.SolveResult] using [`PersistedSolveResult.of`][clintest.protocol.PersistedSolveResult.of].
    """

    def __init__(
        self,
        exhausted: bool = False,
        interrupted: bool = False,
        satisfiable: bool | None = None,
        unsatisfiable: bool | None = None,
    ) -> None:
        """Initialize the `PersistedSolveResult` with its search status.

        Args:
            exhausted: Whether the search space was exhausted.
            interrupted: Whether the search space was interrupted.
            satisfiable: Whether the problem is satisfiable, unsatisfiable, or unknown.
            unsatisfiable: Whether the problem is unsatisfiable, satisfiable, or unknown.
        """
        self.__exhausted = exhausted
        self.__interrupted = interrupted
        self.__satisfiable = satisfiable
        self.__unsatisfiable = unsatisfiable

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"exhausted={self.__exhausted!r}, "
            f"interrupted={self.__interrupted!r}, "
            f"satisfiable={self.__satisfiable!r}, "
            f"unsatisfiable={self.__unsatisfiable!r}"
            ")"
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, PersistedSolveResult)
            and self.__exhausted == other.__exhausted
            and self.__interrupted == other.__interrupted
            and self.__satisfiable == other.__satisfiable
            and self.__unsatisfiable == other.__unsatisfiable
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.__exhausted,
                self.__interrupted,
                self.__satisfiable,
                self.__unsatisfiable,
            )
        )

    @property
    @override
    def exhausted(self) -> bool:  # noqa: D102
        return self.__exhausted

    @property
    @override
    def interrupted(self) -> bool:  # noqa: D102
        return self.__interrupted

    @property
    @override
    def satisfiable(self) -> bool | None:  # noqa: D102
        return self.__satisfiable

    @property
    @override
    def unsatisfiable(self) -> bool | None:  # noqa: D102
        return self.__unsatisfiable

    @classmethod
    def of(cls, result: SolveResult) -> Self:
        """Persist the data of `result`.

        The result is a `PersistedSolveResult`.

        Args:
            result: The solve result whose data should be persisted.

        Returns:
            A persisted copy of `result`'s data.
        """
        return cls(
            exhausted=result.exhausted,
            interrupted=result.interrupted,
            satisfiable=result.satisfiable,
            unsatisfiable=result.unsatisfiable,
        )

    def modify(self, **kwargs: Any) -> Self:
        """Create a new `PersistedSolveResult` with modified attributes.

        Args:
            **kwargs: The attributes to modify.
                Valid keys are `"exhausted"`, `"interrupted"`, `"satisfiable"`, and `"unsatisfiable"`.

        Returns:
            A new solve result with the requested changes and all other attributes preserved.
        """
        return type(self)(
            exhausted=kwargs.get("exhausted", self.exhausted),
            interrupted=kwargs.get("interrupted", self.interrupted),
            satisfiable=kwargs.get("satisfiable", self.satisfiable),
            unsatisfiable=kwargs.get("unsatisfiable", self.unsatisfiable),
        )
