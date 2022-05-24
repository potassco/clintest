from abc import ABC, abstractmethod
from clingo.solving import SolveResult
from clingo.statistics import StatisticsMap
from enum import Enum
from typing import Any, List, Optional, Sequence

from .model import Model

class Result:
    def __init__(self, errors: List[Any]):
        self.errors = errors

    def is_success(self) -> bool:
        return bool(self.errors)

    def is_failure(self) -> bool:
        return not self.is_success()

class Evaluator(ABC):
    def on_model(self, model: Model) -> bool:
        pass

    def on_unsat(self, bounds: Sequence[int]) -> None:
        pass

    def on_statistics(self, statistics: StatisticsMap) -> None:
        pass

    def on_finish(self, result: SolveResult) -> None:
        pass

    def on_core(self, core: Sequence[int]) -> None:
        pass

    @abstractmethod
    def conclude(self) -> Result:
        pass
