"""The abstract class [`Solver`][clintest.solver.Solver] and off-the-shelf solver implementations."""

from abc import ABC, abstractmethod
from typing import Callable, Iterable, Optional, Sequence, cast, override

from clingo.control import Control
from clingo.solving import Model as ClingoModel
from clingo.solving import SolveResult as ClingoSolveResult

from .protocol import Model, PersistedSolveResult, SolveResult
from .test import Test


class Solver(ABC):
    """An initialized solver that may solve any test."""

    @abstractmethod
    def solve(self, test: Test) -> None:
        """Use this solver to solve a given `test`.

        `test` is updated in place, not reset.
        Use a fresh test for each independent solve, then inspect [`Test.outcome`][clintest.test.Test.outcome] or call [`Test.assert_`][clintest.test.Test.assert_].

        Args:
            test: The test to evaluate using this solver.
        """


def _adapt_on_model(cb: Callable[[Model], bool]) -> Callable[[ClingoModel], bool | None]:
    def inner(m: ClingoModel) -> bool | None:
        return cb(cast(Model, m))

    return inner


def _adapt_on_finish(cb: Callable[[SolveResult], None]) -> Callable[[ClingoSolveResult], None]:
    def inner(r: ClingoSolveResult) -> None:
        cb(cast(SolveResult, r))

    return inner


class Clingo(Solver):
    """A solver using clingo's control object.

    See `clingo.control.Control`.

    Each solve creates a new control object, adds `program`, loads `files`, and grounds the `base` part.
    If the test's outcome is already certain, the solve call and its callbacks are skipped.
    Otherwise, clingo's defaults apply unless overridden by `arguments`; pass `["0"]` to request all models.
    """

    def __init__(
        self,
        arguments: Optional[Sequence[str]] = None,
        program: Optional[str] = None,
        files: Optional[Sequence[str]] = None,
    ) -> None:
        """Initialize the solver with `arguments`, `program`, and `files`.

        Args:
            arguments: The command-line options passed to clingo.
                `None` supplies no options, leaving clingo's defaults.
            program: The program source to solve.
                `None` supplies an empty program.
            files: The paths from which to load additional program source.
                `None` loads no files.
        """
        self.__arguments = [] if arguments is None else arguments
        self.__program = "" if program is None else program
        self.__files = [] if files is None else files

    @override
    def solve(self, test: Test) -> None:  # noqa: D102
        ctl = Control(self.__arguments)

        ctl.add("base", [], self.__program)

        for file in self.__files:
            ctl.load(file)

        ctl.ground([("base", [])])

        if not test.outcome().is_certain():
            ctl.solve(
                on_model=_adapt_on_model(test.on_model),
                on_unsat=test.on_unsat,
                on_core=test.on_core,
                on_statistics=test.on_statistics,
                on_finish=_adapt_on_finish(test.on_finish),
            )

    def __repr__(self):
        name = self.__class__.__name__
        arguments = repr(self.__arguments)
        program = repr(self.__program)
        files = repr(self.__files)
        return f"{name}({arguments}, {program}, {files})"


class Iterate(Solver):
    """A solver iterating over an [`Iterable`](https://docs.python.org/3/library/typing.html#typing.Iterable) of models.

    Models implement the [`Model`][clintest.protocol.Model] protocol.

    The iterable is stored without copying it.
    A one-shot iterator remains consumed across solve calls; use a re-iterable collection, such as a list, to replay the models for fresh tests.
    Iteration stops when [`Test.on_model`][clintest.test.Test.on_model] returns `False` or the iterable is exhausted.
    In either case, [`Test.on_finish`][clintest.test.Test.on_finish] receives the final solve result.
    """

    def __init__(self, models: Iterable[Model]) -> None:
        """Initialize the solver with `models` to iterate over."""
        self.__models = models

    @override
    def solve(self, test: Test) -> None:  # noqa: D102
        exhausted = True
        satisfiable = False

        for model in self.__models:
            satisfiable = True
            if not test.on_model(model):
                exhausted = False
                break

        test.on_finish(
            PersistedSolveResult(
                exhausted=exhausted, interrupted=False, satisfiable=satisfiable, unsatisfiable=not satisfiable
            )
        )
