from abc import ABC, abstractmethod
from typing import Sequence, Tuple

from clingo.solving import Model, SolveResult
from clingo.statistics import StatisticsMap

class Test(ABC):
    def on_model(self, _model: Model) -> bool:
        return True

    def on_unsat(self, lower_bound: Sequence[int]) -> None:
        pass

    def on_core(self, core: Sequence[int]) -> None:
        pass

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        pass

    @abstractmethod
    def on_finish(self, result: SolveResult) -> None:
        pass

    @abstractmethod
    def outcome(self) -> Tuple[bool, bool]:
        pass


class Inspect(Test):
    def __init__(self):
        self.artifacts = []
        self.__outcome = True, True

    def on_model(self, model: Model) -> bool:
        self.artifacts.append({
            "__f": "on_model",
            "str(model)": str(model),
        })
        return True

    def on_unsat(self, lower_bound: Sequence[int]) -> None:
        self.artifacts.append({
            "__f": "on_unsat",
            "lower_bound": lower_bound,
        })

    def on_core(self, core: Sequence[int]) -> None:
        self.artifacts.append({
            "__f": "on_core",
            "core": core,
        })

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        self.artifacts.append({
            "__f": "on_statistics",
            "step": step,
            "accumulated": accumulated,
        })

    def on_finish(self, result: SolveResult) -> None:
        self.artifacts.append({
            "__f": "on_finish",
            "result": result,
        })
        self.__outcome = True, False

    def outcome(self) -> Tuple[bool, bool]:
        return self.__outcome
