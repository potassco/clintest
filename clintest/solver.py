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
        arguments: Sequence[str] = None,
        files: Sequence[str] = None,
        program: str = "",
    ):
        self.__arguments = [] if arguments is None else arguments
        self.__files = [] if files is None else files
        self.__program = program

    def __str__(self) -> str:
        parts = self.__arguments + self.__files + ["-"] * bool(self.__program)
        result = "clingo"
        result += " " * bool(parts) + " ".join(parts)
        if self.__program:
            result += "\n" + self.__program
        return result

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
