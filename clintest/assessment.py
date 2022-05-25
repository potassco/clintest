from abc import ABC, abstractmethod
from clingo.solving import Model, SolveResult
from clingo.statistics import StatisticsMap
from typing import List

class Assessment(ABC):
    def __init__(self, description: str):
        self.__description = description
        self.__conclusion = None

    def __str__(self, number: List[int] = []) -> str:
        number = ".".join((str(i) for i in number)) + " " * bool(number)
        conclusion = { True: "Yes", False: "No", None: "Unknown" }[self.conclusion]
        return f"{number}{self.description} {conclusion}"

    @property
    def description(self):
        return self.__description

    @property
    def conclusion(self):
        return self.__conclusion

    @conclusion.setter
    def conclusion(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("conclusion must be True or False")

        if self.__conclusion is None:
            self.__conclusion = value
        else:
            raise Exception("conclusion may not be set twice")

    def assess_model(self, model: Model) -> bool:
        return True

    def assess_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        pass

    def assess_result(self, result: SolveResult) -> None:
        pass

    @abstractmethod
    def conclude(self) -> None:
        pass

class Sat(Assessment):
    def __init__(self, description: str = "Is there any model?"):
        super().__init__(description)

    def assess_model(self, model: Model) -> bool:
        if self.conclusion is None:
            self.conclusion = True
        return False

    def assess_result(self, result: SolveResult) -> None:
        self.conclude()

    def conclude(self) -> None:
        if self.conclusion is None:
             self.conclusion = False
