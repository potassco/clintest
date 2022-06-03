from abc import ABC, abstractmethod
from clingo.solving import Model, SolveResult
from clingo.statistics import StatisticsMap
from colorama import Fore, Style
from typing import List, Optional

from .assertion import Assertion, True_, False_

class Assessment(ABC):
    def __init__(self, description: str):
        self._description: str =  description
        self._conclusion: Optional[bool] = None

    def __str__(self, number: List[int] = [], identation: int = 4) -> str:
        result  = " " * identation * len(number)
        result += Style.DIM + ".".join((str(i) for i in number)) + ". " * bool(number) + Style.RESET_ALL
        result += self._description + " "
        result += {
            True: Fore.GREEN + "Yes" + Fore.RESET,
            False: Fore.RED + "No" + Fore.RESET,
            None: Fore.YELLOW + "Unknown" + Fore.RESET
        }[self.conclusion]
        return result

    @property
    def description(self) -> str:
        return self._description

    @property
    def conclusion(self) -> Optional[bool]:
        return self._conclusion

    def assess_model(self, model: Model) -> bool:
        return True

    def assess_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        pass

    @abstractmethod
    def assess_result(self, result: SolveResult) -> None:
        pass

class Quantifier(Assessment):
    def __init__(self, assertion: Assertion, description: str):
        super().__init__(description)
        self._assertion = assertion

    @property
    def assertion(self) -> Assertion:
        return self._assertion

class ForAny(Quantifier):
    def __init__(self, assertion: Assertion, description: Optional[str] = None):
        if description is None:
            description = f"Does the following hold for any model: {str(assertion)}?"
        super().__init__(assertion, description)

    def assess_model(self, model: Model) -> bool:
        if self._conclusion is not None:
            return False

        if self._assertion.holds_for(model):
            self._conclusion = True
            return False
        else:
            return True

    def assess_result(self, result: SolveResult) -> None:
        if self._conclusion is None:
            self._conclusion = False

class ForAll(Quantifier):
    def __init__(self, assertion: Assertion, description: Optional[str] = None):
        if description is None:
            description = f"Does the following hold for all models: {str(assertion)}?"
        super().__init__(assertion, description)

    def assess_model(self, model: Model) -> bool:
        if self._conclusion is not None:
            return False

        if self._assertion.holds_for(model):
            return True
        else:
            self._conclusion = False
            return False

    def assess_result(self, result: SolveResult) -> None:
        if self._conclusion is None:
            self._conclusion = True

class Combinator(Assessment):
    def __init__(self, components: List[Assessment], description: str):
        super().__init__(description)
        self._components = components
        self._ongoing = components

    def __str__(self, number: List[int] = [], identation: int = 4) -> str:
        result = super().__str__(number, identation)
        for i, component in enumerate(self._components):
            result += "\n" + component.__str__(number + [i + 1], identation)
        return result

    @property
    def components(self) -> List[Assessment]:
        return self._components

    @property
    def ongoing(self) -> List[Assessment]:
        return self._ongoing

class Any(Combinator):
    def __init__(
        self,
        components: List[Assessment],
        description: str = "Is any of the following assessments true?"
    ):
        super().__init__(components, description)

    def assess_model(self, model: Model) -> bool:
        if self._conclusion is not None:
            return False

        still_ongoing = []
        for component in self._ongoing:
            component.assess_model(model)
            if   component.conclusion is None:
                still_ongoing.append(component)
            elif component.conclusion is True:
                self._conclusion = True
                self._ongoing = []
                return False

        self._ongoing = still_ongoing

        if still_ongoing:
            return True
        else:
            self._conclusion = False
            return False

    def assess_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        if self._conclusion is not None:
            return

        still_ongoing = []
        for component in self._ongoing:
            component.assess_statistics(step, accumulated)
            if   component.conclusion is None:
                still_ongoing.append(component)
            elif component.conclusion is True:
                self._conclusion = True
                self._ongoing = []
                return

        self._ongoing = still_ongoing

        if not still_ongoing:
            self._conclusion = False

    def assess_result(self, result: SolveResult) -> None:
        if self._conclusion is not None:
            return

        for component in self._ongoing:
            component.assess_result(result)
            if component.conclusion:
                self._conclusion = True
                self._ongoing = []
                return
        self._conclusion = False
        self._ongoing = []

def Sat() -> Assessment:
    return ForAny(True_(), description="Is the program satisfiable?")

def Unsat() -> Assessment:
    return ForAll(False_(), description="Is the program unsatisfiable?")
