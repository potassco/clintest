from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from .model import Model

class Result(Enum):
    SUCCESS = 0
    FAILURE = 1

class Evaluator(ABC):
    @abstractmethod
    def on_model(self, model: Model) -> Optional[Result]:
        pass

    @abstractmethod
    def on_finish(self) -> Result:
        pass
