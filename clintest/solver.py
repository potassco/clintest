from abc import ABC, abstractmethod
from typing import Optional

from .model import Model

class Solver(ABC):
    @abstractmethod
    def model(self) -> Optional[Model]:
        pass
