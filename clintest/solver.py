from abc import ABC, abstractmethod
from typing import Sequence
from clingo.control import Control

from .assessment import Assessment


class Solver(ABC):
    @abstractmethod
    def solve(self, assessment: Assessment) -> None:
        pass


class Clingo(Solver):
    def __init__(
        self,
        arguments: Sequence[str] = [],
        files: Sequence[str] = [],
        program: str = "",
    ):
        self.__arguments = arguments
        self.__files = files
        self.__program = program

    def __str__(self) -> str:
        pass # TODO

    def solve(self, assessment: Assessment) -> None:
        ctl = Control(self.__arguments)

        for file in self.__files:
            ctl.load(file)

        ctl.add("base", [], self.__program)

        ctl.ground([("base", [])])

        ctl.solve(
            on_model=assessment.assess_model,
            on_finish=assessment.assess_result,
            on_statistics=assessment.assess_statistics,
        )
