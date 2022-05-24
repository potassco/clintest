from abc import ABC, abstractmethod
from typing import Optional, Callable, List
from clingo import SolveResult, StatisticsMap,Control

from .check import Check

class Solver(ABC):
    @abstractmethod
    def run(self,check:Check)->None:
        pass

    def __str__(self)->str:
        return self.__class__.__name__