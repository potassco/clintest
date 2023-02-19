from abc import ABC, abstractmethod
from typing import Optional, Sequence

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
    def outcome(self) -> Optional[bool]:
        pass
