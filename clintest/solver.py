from abc import ABC, abstractmethod
from typing import Optional, Callable, List
from clingo import SolveResult, StatisticsMap,Control

from .model import Model

class Solver(ABC):
    @abstractmethod
    def run(self,
            on_model:Callable[[Model],None], 
            on_finish:Callable[[],None],
            ):
        pass
