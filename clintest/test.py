"""
The abstract class `clintest.test.Test` and off-the-shelf test implementations.
"""

from abc import ABC, abstractmethod
import os
from textwrap import indent
from typing import Any, Callable, Dict, Optional, Sequence

from clingo.solving import Model, SolveResult
from clingo.statistics import StatisticsMap

from .outcome import Outcome
from .quantifier import Quantifier, Finished
from .assertion import Assertion


class Test(ABC):
    """
    An abstract test consuming the artifacts of a `clintest.solver.Solver` in order to compute an
    `clintest.outcome.Outcome`.
    """

    def on_model(self, _model: Model) -> bool:
        """
        Consume a `clingo.model.Model` and possibly alter the current outcome of this test.

        Parameters
        ----------
        model
            The `clingo.model.Model` to consume.

        Returns
        -------
        Whether further models a needed to decide this test.
        """

        return True

    def on_unsat(self, lower_bound: Sequence[int]) -> None:
        """
        Consume a `lower_bound` during optimization and possibly alter the current outcome of this
        test.

        Parameters
        ----------
        lower_bound
            The lower bound.
        """

    def on_core(self, core: Sequence[int]) -> None:
        """
        Consume an unsat `core` and possibly alter the current outcome of this test.

        Parameters
        ----------
        core
            The unsat core.
        """

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        """
        Consume the solving statistics and possibly alter the current outcome of this test.

        Parameters
        ----------
        step
            The step statistics.

        accumulated
            The accumulated statistics.
        """

    @abstractmethod
    def on_finish(self, result: SolveResult) -> None:
        """
        Consume the final solve result and possibly alter the current outcome of this test.

        This should be the last `on_*`-method ever called on a test.
        Afterwards the outcome must be certain.

        Parameters
        ----------
        result
            The `clingo.solving.SolveResult`.
        """

    @abstractmethod
    def outcome(self) -> Outcome:
        """
        Returns the current `Outcome` of this test.

        Returns
        -------
        The current outcome of this test.
        """

    def assert_(self) -> None:
        """
        Assert the outcome of this test to be certainly true.
        Raise an `AssertionError` if the test is either incomplete or has failed.
        """

        if not self.outcome().is_certainly_true():
            msg = "The following test "
            msg += ["is incomplete.", "has failed."][self.outcome().is_certain()]
            msg += os.linesep
            msg += indent(str(self), 4 * " ")

            raise AssertionError(msg)


class True_(Test):
    """
    The test which always succeeds.

    Parameters
    ----------
    lazy
        Whether this test should be lazy, i.e., not consume any models.
    """

    def __init__(self, lazy: bool = True) -> None:
        self.__outcome = Outcome(True, lazy)

    def __repr__(self):
        name = self.__class__.__name__
        outcome = repr(self.__outcome)
        return f"{name}(__outcome={outcome})"

    def __str__(self):
        return f"[{self.__outcome}] {self.__class__.__name__}"

    def on_model(self, _model: Model) -> bool:
        return not self.__outcome.is_certain()

    def on_finish(self, result: SolveResult) -> None:
        self.__outcome = Outcome(True, True)

    def outcome(self) -> Outcome:
        return self.__outcome


class False_(Test):
    """
    The test which always failes.

    Parameters
    ----------
    lazy
        Whether this test should be lazy, i.e., not consume any models.
    """

    def __init__(self, lazy: bool = True) -> None:
        self.__outcome = Outcome(False, lazy)

    def __repr__(self):
        name = self.__class__.__name__
        outcome = repr(self.__outcome)
        return f"{name}(__outcome={outcome})"

    def __str__(self):
        return f"[{self.__outcome}] {self.__class__.__name__}"

    def on_model(self, _model: Model) -> bool:
        return not self.__outcome.is_certain()

    def on_finish(self, result: SolveResult) -> None:
        self.__outcome = Outcome(False, True)

    def outcome(self) -> Outcome:
        return self.__outcome


class Recording:
    """
    A recording of the calls to the `on_*`-methods of a `Test`.
    This class is mainly used inside of `Record`.
    """

    def __init__(self, entries: Optional[Sequence[Dict[str, Any]]] = None):
        if entries is None:
            entries = []
        self.__entries = list(entries)

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__entries})"

    def __str__(self):
        def fmt(entry):
            result = f"[{entry['__outcome']}] {entry['__f']}"
            if entry['__f'] == "on_model":
                result += os.linesep + 4 * " " + entry['str(model)']
            return result

        width = len(str(len(self.__entries) - 1))
        return os.linesep.join((
            f"{(width - len(str(i))) * ' '}{i}: {fmt(entry)}"
            for i, entry in enumerate(self.__entries)
        ))

    def __eq__(self, other):
        # pylint: disable=protected-access
        return self.__entries == other.__entries

    def amend(self, changes: Dict[str, Any]):
        """
        Update the last entry of this encoding.

        Parameters
        ----------
        changes
            The changes.
        """

        self.__entries[-1].update(changes)

    def append(self, entry: Dict[str, Any]):
        """
        Append a new entry at the end of this recording.

        Parameters
        ----------
        entry
            The entry.
        """

        self.__entries.append(entry)

    def subsumes(self, other) -> bool:
        """
        Determine whether this recording subsumes another recording.

        Parameters
        ----------
        other
            The other recording.
        """

        # pylint: disable=protected-access
        return len(self.__entries) == len(other.__entries) and all(
            all(item in other_entry.items() for item in self_entry.items())
            for self_entry, other_entry in zip(self.__entries, other.__entries)
        )


class Record(Test):
    """
    A test that behaves identical to a given other `test` but records any call to one of it
    `on_*`-methods. This can be very helpful for debugging.

    Parameters
    ----------
    test
        A `Test` that determines how this test should behave.
    """

    def __init__(self, test: Test = True_(lazy = False)):
        self.test: Test = test
        self.recording: Recording = Recording([{
            "__f": "__init__",
            "__outcome": self.outcome(),
        }])

    def __repr__(self):
        name = self.__class__.__name__
        test = repr(self.test)
        recording = repr(self.recording)
        return f"{name}(test={test}, recording={recording})"

    def __str__(self):
        return os.linesep.join([
            f"[{self.outcome()}] {self.__class__.__name__}",
            f"    test: {indent(str(self.test), 4 * ' ')[4:]}",
            "    recording:",
            indent(str(self.recording), 8 * " "),
        ])

    def on_model(self, model: Model) -> bool:
        self.recording.append({
            "__f": "on_model",
            "str(model)": str(model),
        })
        result = self.test.on_model(model)
        self.recording.amend({
            "__result": result,
            "__outcome": self.outcome(),
        })
        return result

    def on_unsat(self, lower_bound: Sequence[int]) -> None:
        self.recording.append({
            "__f": "on_unsat",
            "lower_bound": lower_bound,
        })
        self.test.on_unsat(lower_bound)
        self.recording.amend({"__outcome": self.outcome()})

    def on_core(self, core: Sequence[int]) -> None:
        self.recording.append({
            "__f": "on_core",
            "core": core,
        })
        self.test.on_core(core)
        self.recording.amend({"__outcome": self.outcome()})

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:
        self.recording.append({
            "__f": "on_statistics",
            "step": step,
            "accumulated": accumulated,
        })
        self.test.on_statistics(step, accumulated)
        self.recording.amend({"__outcome": self.outcome()})

    def on_finish(self, result: SolveResult) -> None:
        self.recording.append({
            "__f": "on_finish",
            "result": result,
        })
        self.test.on_finish(result)
        self.recording.amend({"__outcome": self.outcome()})

    def outcome(self) -> Outcome:
        return self.test.outcome()


class Assert(Test):
    """
    A test that asserts certain properties about the `clingo.model.Model`s of a program. This test
    can be highly costumized using a `clintest.quantifier.Quantifier` and a
    `clintest.assertion.Assertion`.

    Parameters
    ----------
    quantifier
        The `clintest.quantifier.Quantifier` used with this test.

    assertion
        The `clintest.assertion.Assertion` used with this test.
    """

    def __init__(self, quantifier: Quantifier, assertion: Assertion) -> None:
        self.__quantifier = quantifier
        self.__assertion = assertion

    def __repr__(self):
        name = self.__class__.__name__
        quantifier = repr(self.__quantifier)
        assertion = repr(self.__assertion)
        return f"{name}({quantifier}, {assertion})"

    def __str__(self):
        return os.linesep.join([
            f"[{self.outcome()}] {self.__class__.__name__}",
            f"    quantifier: {self.__quantifier}",
            f"    assertion:  {self.__assertion}",
        ])

    def on_model(self, model: Model) -> bool:
        if not self.__quantifier.outcome().is_certain():
            self.__quantifier.consume(self.__assertion.holds_for(model))

        return not self.__quantifier.outcome().is_certain()

    def on_finish(self, result: SolveResult) -> None:
        self.__quantifier = Finished(self.__quantifier)

    def outcome(self) -> Outcome:
        return self.__quantifier.outcome()


class Not(Test):
    """
    The negation of a given test.
    This test failes if `operand` succeeds and vice versa.

    Parameters
    ----------
    operand
        The `Test` to be negated.
    """

    def __init__(self, operand: Test) -> None:
        self.__operand = operand

    def __repr__(self):
        name = self.__class__.__name__
        operand = repr(self.__operand)
        return f"{name}({operand})"

    def __str__(self):
        return os.linesep.join([
            f"[{self.outcome()}] {self.__class__.__name__}",
            f"    operand: {indent(str(self.__operand), 4 * ' ')[4:]}",
        ])

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
    """
    The conjunction of a list given tests.
    This test succeeds if all `args` succeed.

    Parameters
    ----------
    args
        The `Test`s to be combined.

    short_circuit
        Whether this test should employ short circuit optimization, i.e., abort all remaining tests
        once the outcome of a test is certainly false.

    ignore_certain
        Whether this test should employ the ignore certain optimization, i.e., not send artifacts
        to test that are already certain.
    """

    def __init__(
        self,
        *args: Test,
        short_circuit: bool = True,
        ignore_certain: bool = True
    ) -> None:
        self.__operands = list(args)
        self.__short_circuit = short_circuit
        self.__ignore_certain = ignore_certain

        self.__ongoing = list(args)
        self.__outcome = Outcome(True, False)

        def call_operand(_operand: Test) -> None:
            pass

        self.__on_whatever(call_operand)

    def __repr__(self):
        name = self.__class__.__name__

        operands = ", ".join(repr(operand) for operand in self.__operands)
        short_circuit = repr(self.__short_circuit)
        ignore_certain = repr(self.__ignore_certain)

        ongoing = repr(self.__ongoing)
        outcome = repr(self.__outcome)

        return (
            f"{name}("
            f"{operands}, "
            f"short_circuit={short_circuit}, "
            f"ignore_certain={ignore_certain}, "
            f"__ongoing={ongoing}, "
            f"__outcome={outcome})"
        )

    def __str__(self):
        if self.__operands:
            operands = ""
            width = len(str(len(self.__operands) - 1))
            for i, operand in enumerate(self.__operands):
                i = str(i)
                operands += os.linesep
                operands += (width - len(i)) * " "
                operands += [" ", "*"][operand in self.__ongoing]
                operands += f"{i}: {operand}"
            operands = indent(operands, 8 * ' ')
        else:
            operands = " <none>"

        return os.linesep.join([
            f"[{self.outcome()}] {self.__class__.__name__} ",
            f"    operands:{operands}",
            f"    short_circuit:  {self.__short_circuit}",
            f"    ignore_certain: {self.__ignore_certain}",
        ])

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
        self.__outcome = Outcome(self.__outcome.current_value(), not bool(still_ongoing))

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

        ignore_certain_bck = self.__ignore_certain
        self.__ignore_certain = True
        self.__on_whatever(call_operand)
        self.__ignore_certain = ignore_certain_bck

        assert not self.__ongoing
        assert self.__outcome.is_certain()

    def outcome(self) -> Outcome:
        return self.__outcome


class Or(Test):
    """
    The disjunction of a list given tests.
    This test succeeds if any `args` succeed.

    Parameters
    ----------
    args
        The `Test`s to be combined.

    short_circuit
        Whether this test should employ short circuit optimization, i.e., abort all remaining tests
        once the outcome of a test is certainly true.

    ignore_certain
        Whether this test should employ the ignore certain optimization, i.e., not send artifacts
        to test that are already certain.
    """

    def __init__(
        self,
        *args: Test,
        short_circuit: bool = True,
        ignore_certain: bool = True
    ) -> None:
        self.__operands = list(args)
        self.__short_circuit = short_circuit
        self.__ignore_certain = ignore_certain

        self.__ongoing = list(args)
        self.__outcome = Outcome(False, False)

        def call_operand(_operand: Test) -> None:
            pass

        self.__on_whatever(call_operand)

    def __repr__(self):
        name = self.__class__.__name__

        operands = ", ".join(repr(operand) for operand in self.__operands)
        short_circuit = repr(self.__short_circuit)
        ignore_certain = repr(self.__ignore_certain)

        ongoing = repr(self.__ongoing)
        outcome = repr(self.__outcome)

        return (
            f"{name}("
            f"{operands}, "
            f"short_circuit={short_circuit}, "
            f"ignore_certain={ignore_certain}, "
            f"__ongoing={ongoing}, "
            f"__outcome={outcome})"
        )

    def __str__(self):
        if self.__operands:
            operands = ""
            width = len(str(len(self.__operands) - 1))
            for i, operand in enumerate(self.__operands):
                i = str(i)
                operands += os.linesep
                operands += (width - len(i)) * " "
                operands += [" ", "*"][operand in self.__ongoing]
                operands += f"{i}: {operand}"
            operands = indent(operands, 8 * ' ')
        else:
            operands = " <none>"

        return os.linesep.join([
            f"[{self.outcome()}] {self.__class__.__name__} ",
            f"    operands:{operands}",
            f"    short_circuit:  {self.__short_circuit}",
            f"    ignore_certain: {self.__ignore_certain}",
        ])

    def __on_whatever(self, call_operand: Callable[[Test], None]) -> bool:
        still_ongoing = []

        for operand in self.__ongoing:
            call_operand(operand)

            if operand.outcome().is_certainly_true():
                if self.__short_circuit:
                    self.__ongoing = []
                    self.__outcome = Outcome(True, True)
                    return False
                else:
                    self.__outcome = Outcome(True, False)

            if not (self.__ignore_certain and operand.outcome().is_certain()):
                still_ongoing.append(operand)

        self.__ongoing = still_ongoing
        self.__outcome = Outcome(self.__outcome.current_value(), not bool(still_ongoing))

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

        ignore_certain_bck = self.__ignore_certain
        self.__ignore_certain = True
        self.__on_whatever(call_operand)
        self.__ignore_certain = ignore_certain_bck

        assert not self.__ongoing
        assert self.__outcome.is_certain()

    def outcome(self) -> Outcome:
        return self.__outcome
