from abc import ABC, abstractmethod

from .test import Test

class Solver(ABC):
    @abstractmethod
    def solve(self, test: Test) -> None:
        pass
