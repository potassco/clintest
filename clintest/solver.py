from abc import ABC, abstractmethod
from typing import Optional

from .evaluator import Evaluator
from .model import Model

class Solver(ABC):
    @abstractmethod
    def solve(self, evaluator: Evaluator) -> None:
        pass
