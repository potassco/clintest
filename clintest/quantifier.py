from abc import ABC, abstractmethod
from typing import Tuple


class Quantifier(ABC):
    @abstractmethod
    def consume(self, value: bool) -> Tuple[bool, bool]:
        pass
