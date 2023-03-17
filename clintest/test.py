from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Sequence

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


class Inspect(Test):
    def __init__(self, test: Test = True_(lazy_evaluation = False)):
        self.artifacts: List[Dict[str, Any]] = []
        self.test: Test = test

    def on_model(self, model: Model) -> bool:
        self.artifacts.append({
            "__f": "on_model",
            "str(model)": str(model),
        })
        return self.test.on_model(model)

    def on_unsat(self, lower_bound: Sequence[int]) -> None:
        self.artifacts.append({
            "__f": "on_unsat",
            "lower_bound": lower_bound,
        })
        self.test.on_unsat(lower_bound)

    def on_core(self, core: Sequence[int]) -> None:
        self.artifacts.append({
            "__f": "on_core",
            "core": core,
        })
        self.test.on_core(core)

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        self.artifacts.append({
            "__f": "on_statistics",
            "step": step,
            "accumulated": accumulated,
        })
        self.test.on_statistics(step, accumulated)

    def on_finish(self, result: SolveResult) -> None:
        self.artifacts.append({
            "__f": "on_finish",
            "result": result,
        })
        self.test.on_finish(result)

    def outcome(self) -> Outcome:
        return self.test.outcome()


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


class Not(Test):
    def __init__(self, operand: Test) -> None:
        self.__operand = operand

    def on_model(self, model: Model) -> bool:
        return self.__operand.on_model(model)

    def on_unsat(self, lower_bound: Sequence[int]) -> None:
        self.__operand.on_unsat(lower_bound)

    def on_core(self, core: Sequence[int]) -> None:
        self.__operand.on_core(core)

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        self.__operand.on_statistics(step, accumulated)

    def on_finish(self, result: SolveResult) -> None:
        self.__operand.on_finish(result)

    def outcome(self) -> Outcome:
        outcome = self.__operand.outcome()
        return Outcome(not outcome.current_value(), outcome.is_certain())


class And(Test):
    def __init__(
        self,
        *args: Test,
        short_circuit: bool = True,
        ignore_certain: bool = True
    ) -> None:
        # self.__operands = list(args)
        self.__ongoing = list(args)
        self.__short_circuit = short_circuit
        self.__ignore_certain = ignore_certain
        self.__outcome = Outcome(True, False)

    def __on_whatever(self, call_operand: Callable[[Test], None]) -> bool:
        still_ongoing = []

        for operand in self.__ongoing:
            call_operand(operand)

            if operand.outcome().is_certainly_false():
                if self.__short_circuit:
                    self.__ongoing = []
                    self.__outcome = Outcome(False, True)
                    return False
                else:
                    self.__outcome = Outcome(False, False)

            if not (self.__ignore_certain and operand.outcome().is_certain()):
                still_ongoing.append(operand)

        self.__ongoing = still_ongoing
        self.__outcome = Outcome(self.__outcome.current_value(), bool(still_ongoing))

        return not self.__outcome.is_certain()


    def on_model(self, model: Model) -> bool:
        def call_operand(operand: Test) -> None:
            operand.on_model(model)

        return self.__on_whatever(call_operand)


    def on_unsat(self, lower_bound: Sequence[int]) -> None:
        def call_operand(operand: Test) -> None:
            operand.on_unsat(lower_bound)

        self.__on_whatever(call_operand)

    def on_core(self, core: Sequence[int]) -> None:
        def call_operand(operand: Test) -> None:
            operand.on_core(core)

        self.__on_whatever(call_operand)

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        def call_operand(operand: Test) -> None:
            operand.on_statistics(step, accumulated)

        self.__on_whatever(call_operand)

    def on_finish(self, result: SolveResult) -> None:
        def call_operand(operand: Test) -> None:
            operand.on_finish(result)

        self.__on_whatever(call_operand)

        assert not self.__ongoing
        assert self.__outcome.is_certain()

    def outcome(self) -> Outcome:
        return self.__outcome


class Or(Test):
    def __init__(
        self,
        *args: Test,
        short_circuit: bool = True,
        ignore_certain: bool = True
    ) -> None:
        # self.__operands = list(args)
        self.__ongoing = list(args)
        self.__short_circuit = short_circuit
        self.__ignore_certain = ignore_certain
        self.__outcome = Outcome(False, False)

    def __on_whatever(self, call_operand: Callable[[Test], None]) -> bool:
        still_ongoing = []

        for operand in self.__ongoing:
            call_operand(operand)

            if operand.outcome().is_certainly_true():
                if self.__short_circuit:
                    self.__ongoing = []
                    self.__outcome = Outcome(False, True)
                    return False
                else:
                    self.__outcome = Outcome(False, False)

            if not (self.__ignore_certain and operand.outcome().is_certain()):
                still_ongoing.append(operand)

        self.__ongoing = still_ongoing
        self.__outcome = Outcome(self.__outcome.current_value(), bool(still_ongoing))

        return not self.__outcome.is_certain()


    def on_model(self, model: Model) -> bool:
        def call_operand(operand: Test) -> None:
            operand.on_model(model)

        return self.__on_whatever(call_operand)


    def on_unsat(self, lower_bound: Sequence[int]) -> None:
        def call_operand(operand: Test) -> None:
            operand.on_unsat(lower_bound)

        self.__on_whatever(call_operand)

    def on_core(self, core: Sequence[int]) -> None:
        def call_operand(operand: Test) -> None:
            operand.on_core(core)

        self.__on_whatever(call_operand)

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        def call_operand(operand: Test) -> None:
            operand.on_statistics(step, accumulated)

        self.__on_whatever(call_operand)

    def on_finish(self, result: SolveResult) -> None:
        def call_operand(operand: Test) -> None:
            operand.on_finish(result)

        self.__on_whatever(call_operand)

        assert not self.__ongoing
        assert self.__outcome.is_certain()

    def outcome(self) -> Outcome:
        return self.__outcome
