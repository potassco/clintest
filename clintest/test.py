from abc import ABC, abstractmethod
from typing import Sequence

from clingo.solving import Model, SolveResult
from clingo.statistics import StatisticsMap

from .outcome import Outcome
from .quantifier import Quantifier, Finished
from .assertion import Assertion


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
    def outcome(self) -> Outcome:
        pass


class Inspect(Test):
    def __init__(self):
        self.artifacts = []
        self.__outcome = True, True

    def on_model(self, model: Model) -> bool:
        self.artifacts.append({
            "__f": "on_model",
            "str(model)": str(model),
        })
        return True

    def on_unsat(self, lower_bound: Sequence[int]) -> None:
        self.artifacts.append({
            "__f": "on_unsat",
            "lower_bound": lower_bound,
        })

    def on_core(self, core: Sequence[int]) -> None:
        self.artifacts.append({
            "__f": "on_core",
            "core": core,
        })

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        self.artifacts.append({
            "__f": "on_statistics",
            "step": step,
            "accumulated": accumulated,
        })

    def on_finish(self, result: SolveResult) -> None:
        self.artifacts.append({
            "__f": "on_finish",
            "result": result,
        })
        self.__outcome = Outcome(True, False)

    def outcome(self) -> Outcome:
        return self.__outcome


class Assert(Test):
    def __init__(self, quantifier: Quantifier, assertion: Assertion) -> None:
        self.__quantifier = quantifier
        self.__assertion = assertion

    def on_model(self, model: Model) -> bool:
        if not self.__quantifier.outcome().is_certain():
            self.__quantifier.consume(self.__assertion.holds_for(model))

        return not self.__quantifier.outcome().is_certain()

    def on_finish(self, result: SolveResult) -> None:
        self.__quantifier = Finished(self.__quantifier)

    def outcome(self) -> Outcome:
        return self.__quantifier.outcome()


class True_(Test):
    def __init__(self, lazy_evaluation: bool = True) -> None:
        self.__outcome = Outcome(True, lazy_evaluation)

    def on_model(self, _model: Model) -> bool:
        return not self.__outcome.is_certain()

    def on_finish(self, result: SolveResult) -> None:
        self.__outcome = Outcome(True, True)

    def outcome(self) -> Outcome:
        return self.__outcome


class False_(Test):
    def __init__(self, lazy_evaluation: bool = True) -> None:
        self.__outcome = Outcome(False, lazy_evaluation)

    def on_model(self, _model: Model) -> bool:
        return not self.__outcome.is_certain()

    def on_finish(self, result: SolveResult) -> None:
        self.__outcome = Outcome(False, True)

    def outcome(self) -> Outcome:
        return self.__outcome
