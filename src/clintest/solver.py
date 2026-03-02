"""
The abstract class `clintest.solver.Solver` and off-the-shelf solver implementations.
"""

from abc import ABC, abstractmethod
from typing import Optional, Sequence

from clingo.control import Control

from .test import Test


class Solver(ABC):
    """
    An initialized solver that may solve any test.
    """

    @abstractmethod
    def solve(self, test: Test) -> None:
        """
        Use this solver to solve a given `test`.

        Parameters
        ----------
        test
            The `clintest.test.Test` to be solved by this solver.
        """


class Clingo(Solver):
    """
    A solver using `clingo.control.Control`.

    Parameters
    ----------
    arguments
        A list of arguments.

    program
        The program as a `str`.

    files
        A list of files to read the program from.
    """

    def __init__(
        self,
        arguments: Optional[Sequence[str]] = None,
        program: Optional[str] = None,
        files: Optional[Sequence[str]] = None,
    ) -> None:
        self.__arguments = [] if arguments is None else arguments
        self.__program = "" if program is None else program
        self.__files = [] if files is None else files

    def solve(self, test: Test) -> None:
        ctl = Control(self.__arguments)

        ctl.add("base", [], self.__program)

        for file in self.__files:
            ctl.load(file)

        ctl.ground([("base", [])])

        if not test.outcome().is_certain():
            ctl.solve(
                on_model=test.on_model,
                on_unsat=test.on_unsat,
                on_core=test.on_core,
                on_statistics=test.on_statistics,
                on_finish=test.on_finish,
            )

    def __repr__(self):
        name = self.__class__.__name__
        arguments = repr(self.__arguments)
        program = repr(self.__program)
        files = repr(self.__files)
        return f"{name}({arguments}, {program}, {files})"
