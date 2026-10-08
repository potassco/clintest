"""The abstract class [`Test`][clintest.test.Test] and off-the-shelf test implementations."""

import os
from abc import ABC, abstractmethod
from textwrap import indent
from typing import Any, Callable, Dict, Optional, Sequence, override

from clingo.statistics import StatisticsMap

from .assertion import Assertion
from .outcome import Outcome
from .protocol import Model, PersistedModel, PersistedSolveResult, SolveResult
from .quantifier import Finished, Quantifier


class Test(ABC):
    """An abstract test consuming solver artifacts to compute an outcome.

    Artifacts are provided by a [`Solver`][clintest.solver.Solver] to compute an [`Outcome`][clintest.outcome.Outcome].

    Tests accumulate state as solver callbacks are consumed; solving does not reset that state.
    Use a fresh test instance for each independent solve.
    Inspect the result with [`Test.outcome`][clintest.test.Test.outcome], or check that it is certainly true with [`Test.assert_`][clintest.test.Test.assert_].
    """

    def on_model(self, _model: Model) -> bool:
        """Consume `_model` and possibly alter the current outcome of this test.

        Args:
            _model: The model to consume when updating this test's outcome.

        Returns:
            Whether further models are needed to decide this test.
        """
        return True

    def on_unsat(self, lower_bound: Sequence[int]) -> None:  # noqa: B027
        """Consume `lower_bound` during optimization and possibly alter the current outcome of this test.

        Args:
            lower_bound: The lower bound.
        """

    def on_core(self, core: Sequence[int]) -> None:  # noqa: B027
        """Consume the unsat core `core` and possibly alter the current outcome of this test.

        Args:
            core: The unsat core.
        """

    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:  # noqa: B027
        """Consume `step` and `accumulated` statistics and possibly alter the current outcome of this test.

        Args:
            step: The step statistics.
            accumulated: The accumulated statistics.
        """

    @abstractmethod
    def on_finish(self, result: SolveResult) -> None:
        """Consume the final solve result `result` and possibly alter the current outcome of this test.

        This should be the last `on_*`-method ever called on a test.
        Afterwards the outcome must be certain.

        Args:
            result: The final solve status used to complete this test.
        """

    @abstractmethod
    def outcome(self) -> Outcome:
        """Return the current [`Outcome`][clintest.outcome.Outcome] of this test.

        Returns:
            The current outcome of this test.
        """

    def assert_(self) -> None:
        """Assert the outcome of this test to be certainly true.

        This checks the current outcome; it does not run a solver or finish an incomplete test.

        Raises:
            AssertionError: If the test is either incomplete or has failed.
        """
        if not self.outcome().is_certainly_true():
            msg = "The following test "
            msg += ["is incomplete.", "has failed."][self.outcome().is_certain()]
            msg += os.linesep
            msg += indent(str(self), 4 * " ")

            raise AssertionError(msg)


class True_(Test):
    """The test which always succeeds."""

    def __init__(self, lazy: bool = True) -> None:
        """Initialize the test with the laziness setting `lazy`.

        Args:
            lazy: Whether this test should be lazy, i.e., not consume any models.
        """
        self.__outcome = Outcome(True, lazy)

    def __repr__(self):
        name = self.__class__.__name__
        outcome = repr(self.__outcome)
        return f"{name}(__outcome={outcome})"

    def __str__(self):
        return f"[{self.__outcome}] {self.__class__.__name__}"

    @override
    def on_model(self, _model: Model) -> bool:  # noqa: D102
        return not self.__outcome.is_certain()

    @override
    def on_finish(self, result: SolveResult) -> None:  # noqa: D102
        self.__outcome = Outcome(True, True)

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__outcome


class False_(Test):
    """The test which always fails."""

    def __init__(self, lazy: bool = True) -> None:
        """Initialize the test with the laziness setting `lazy`.

        Args:
            lazy: Whether this test should be lazy, i.e., not consume any models.
        """
        self.__outcome = Outcome(False, lazy)

    def __repr__(self):
        name = self.__class__.__name__
        outcome = repr(self.__outcome)
        return f"{name}(__outcome={outcome})"

    def __str__(self):
        return f"[{self.__outcome}] {self.__class__.__name__}"

    @override
    def on_model(self, _model: Model) -> bool:  # noqa: D102
        return not self.__outcome.is_certain()

    @override
    def on_finish(self, result: SolveResult) -> None:  # noqa: D102
        self.__outcome = Outcome(False, True)

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__outcome


class Recording:
    """A recording of the calls to the `on_*`-methods of a [`Test`][clintest.test.Test].

    This class is mainly used inside of [`Record`][clintest.test.Record].
    """

    def __init__(self, entries: Optional[Sequence[Dict[str, Any]]] = None):
        """Initialize the recording with `entries` or an empty sequence."""
        if entries is None:
            entries = []
        self.__entries = list(entries)

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.__entries})"

    def __str__(self):
        def fmt(entry):
            result = f"[{entry['__outcome']}] {entry['__f']}"
            if entry["__f"] == "on_model":
                result += os.linesep + 4 * " " + str(entry["model"])
            return result

        width = len(str(len(self.__entries) - 1))
        return os.linesep.join(
            (f"{(width - len(str(i))) * ' '}{i}: {fmt(entry)}" for i, entry in enumerate(self.__entries))
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Recording) and self.__entries == other.__entries

    def __hash__(self):
        return hash(self.__entries)

    def amend(self, changes: Dict[str, Any]):
        """Update the last entry of this recording with `changes`.

        Args:
            changes: The changes.
        """
        self.__entries[-1].update(changes)

    def append(self, entry: Dict[str, Any]):
        """Append `entry` at the end of this recording.

        Args:
            entry: The entry.
        """
        self.__entries.append(entry)

    def subsumes(self, other: "Recording") -> bool:
        """Determine whether this recording subsumes `other`.

        Args:
            other: The other recording.

        Returns:
            Whether each entry contains all items in the corresponding entry of `other`.
        """
        return len(self.__entries) == len(other.__entries) and all(
            all(item in other_entry.items() for item in self_entry.items())
            for self_entry, other_entry in zip(self.__entries, other.__entries, strict=True)
        )


class Record(Test):
    """A test that behaves identically to a given `test` but records every call to one of its `on_*`-methods.

    This can be very helpful for debugging.
    """

    def __init__(self, test: Test | None = None):
        """Initialize the recording test with the wrapped `test`.

        Args:
            test: The wrapped test whose behavior should be recorded.
        """
        self.test: Test = test if test is not None else True_(lazy=False)
        self.recording: Recording = Recording(
            [
                {
                    "__f": "__init__",
                    "__outcome": self.outcome(),
                }
            ]
        )

    def __repr__(self):
        name = self.__class__.__name__
        test = repr(self.test)
        recording = repr(self.recording)
        return f"{name}(test={test}, recording={recording})"

    def __str__(self):
        return os.linesep.join(
            [
                f"[{self.outcome()}] {self.__class__.__name__}",
                f"    test: {indent(str(self.test), 4 * ' ')[4:]}",
                "    recording:",
                indent(str(self.recording), 8 * " "),
            ]
        )

    @override
    def on_model(self, model: Model) -> bool:  # noqa: D102
        self.recording.append(
            {
                "__f": "on_model",
                "model": PersistedModel.of(model),
            }
        )
        result = self.test.on_model(model)
        self.recording.amend(
            {
                "__result": result,
                "__outcome": self.outcome(),
            }
        )
        return result

    @override
    def on_unsat(self, lower_bound: Sequence[int]) -> None:  # noqa: D102
        self.recording.append(
            {
                "__f": "on_unsat",
                "lower_bound": lower_bound,
            }
        )
        self.test.on_unsat(lower_bound)
        self.recording.amend({"__outcome": self.outcome()})

    @override
    def on_core(self, core: Sequence[int]) -> None:  # noqa: D102
        self.recording.append(
            {
                "__f": "on_core",
                "core": core,
            }
        )
        self.test.on_core(core)
        self.recording.amend({"__outcome": self.outcome()})

    @override
    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:  # noqa: D102
        self.recording.append(
            {
                "__f": "on_statistics",
                "step": step,
                "accumulated": accumulated,
            }
        )
        self.test.on_statistics(step, accumulated)
        self.recording.amend({"__outcome": self.outcome()})

    @override
    def on_finish(self, result: SolveResult) -> None:  # noqa: D102
        self.recording.append(
            {
                "__f": "on_finish",
                "result": PersistedSolveResult.of(result),
            }
        )
        self.test.on_finish(result)
        self.recording.amend({"__outcome": self.outcome()})

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.test.outcome()


class Context(Test):
    """A test that behaves identically to a given `test` but permits changes to its string representation.

    This can be helpful to create human-readable error messages.
    """

    def __init__(
        self,
        test: Test,
        str_: Callable[[Test], str] = str,
        repr_: Callable[[Test], str] = repr,
    ):
        """Initialize the wrapper with `test` and the representation functions `str_` and `repr_`.

        Args:
            test: The wrapped test whose representations should be customized.
            str_: The function used to produce `test`'s string representation.
            repr_: The function used to produce `test`'s debugging representation.
        """
        self.test: Test = test
        self.__str = str_
        self.__repr = repr_

    def __repr__(self):
        return self.__repr(self.test)

    def __str__(self):
        return self.__str(self.test)

    @override
    def on_model(self, model: Model) -> bool:  # noqa: D102
        return self.test.on_model(model)

    @override
    def on_unsat(self, lower_bound: Sequence[int]) -> None:  # noqa: D102
        self.test.on_unsat(lower_bound)

    @override
    def on_core(self, core: Sequence[int]) -> None:  # noqa: D102
        self.test.on_core(core)

    @override
    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:  # noqa: D102
        self.test.on_statistics(step, accumulated)

    @override
    def on_finish(self, result: SolveResult) -> None:  # noqa: D102
        self.test.on_finish(result)

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.test.outcome()


class Assert(Test):
    """A test that asserts certain properties about the models of a program.

    This test can be highly customized using a [`Quantifier`][clintest.quantifier.Quantifier] and an [`Assertion`][clintest.assertion.Assertion].
    """

    def __init__(self, quantifier: Quantifier, assertion: Assertion) -> None:
        """Initialize the test with `quantifier` and `assertion`.

        Args:
            quantifier: The rule used to aggregate assertion results across models.
            assertion: The property to check for each model.
        """
        self.__quantifier = quantifier
        self.__assertion = assertion

    def __repr__(self):
        name = self.__class__.__name__
        quantifier = repr(self.__quantifier)
        assertion = repr(self.__assertion)
        return f"{name}({quantifier}, {assertion})"

    def __str__(self):
        return os.linesep.join(
            [
                f"[{self.outcome()}] {self.__class__.__name__}",
                f"    quantifier: {self.__quantifier}",
                f"    assertion:  {self.__assertion}",
            ]
        )

    @override
    def on_model(self, model: Model) -> bool:  # noqa: D102
        if not self.__quantifier.outcome().is_certain():
            self.__quantifier.consume(self.__assertion.holds_for(model))

        return not self.__quantifier.outcome().is_certain()

    @override
    def on_finish(self, result: SolveResult) -> None:  # noqa: D102
        self.__quantifier = Finished(self.__quantifier)

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__quantifier.outcome()


class Not(Test):
    """The negation of a given test.

    This test fails if `operand` succeeds and vice versa.
    """

    def __init__(self, operand: Test) -> None:
        """Initialize the negation with `operand`.

        Args:
            operand: The test whose outcome should be negated.
        """
        self.__operand = operand

    def __repr__(self):
        name = self.__class__.__name__
        operand = repr(self.__operand)
        return f"{name}({operand})"

    def __str__(self):
        return os.linesep.join(
            [
                f"[{self.outcome()}] {self.__class__.__name__}",
                f"    operand: {indent(str(self.__operand), 4 * ' ')[4:]}",
            ]
        )

    @override
    def on_model(self, model: Model) -> bool:  # noqa: D102
        return self.__operand.on_model(model)

    @override
    def on_unsat(self, lower_bound: Sequence[int]) -> None:  # noqa: D102
        self.__operand.on_unsat(lower_bound)

    @override
    def on_core(self, core: Sequence[int]) -> None:  # noqa: D102
        self.__operand.on_core(core)

    @override
    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:  # noqa: D102
        self.__operand.on_statistics(step, accumulated)

    @override
    def on_finish(self, result: SolveResult) -> None:  # noqa: D102
        self.__operand.on_finish(result)

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        outcome = self.__operand.outcome()
        return Outcome(not outcome.current_value(), outcome.is_certain())


class And(Test):
    """The conjunction of a list of given tests.

    This test succeeds if all `args` succeed.
    """

    def __init__(self, *args: Test, short_circuit: bool = True, ignore_certain: bool = True) -> None:
        """Initialize the conjunction with `args`, `short_circuit`, and `ignore_certain`.

        Args:
            *args: The tests to combine.
            short_circuit: Whether this test should employ short circuit optimization, i.e., abort all remaining tests once the outcome of a test is certainly false.
            ignore_certain: Whether this test should employ the ignore certain optimization, i.e., not send artifacts to test that are already certain.
        """
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
                i_str = str(i)
                operands += os.linesep
                operands += (width - len(i_str)) * " "
                operands += [" ", "*"][operand in self.__ongoing]
                operands += f"{i_str}: {operand}"
            operands = indent(operands, 8 * " ")
        else:
            operands = " <none>"

        return os.linesep.join(
            [
                f"[{self.outcome()}] {self.__class__.__name__} ",
                f"    operands:{operands}",
                f"    short_circuit:  {self.__short_circuit}",
                f"    ignore_certain: {self.__ignore_certain}",
            ]
        )

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

    @override
    def on_model(self, model: Model) -> bool:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_model(model)

        return self.__on_whatever(call_operand)

    @override
    def on_unsat(self, lower_bound: Sequence[int]) -> None:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_unsat(lower_bound)

        self.__on_whatever(call_operand)

    @override
    def on_core(self, core: Sequence[int]) -> None:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_core(core)

        self.__on_whatever(call_operand)

    @override
    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_statistics(step, accumulated)

        self.__on_whatever(call_operand)

    @override
    def on_finish(self, result: SolveResult) -> None:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_finish(result)

        ignore_certain_bck = self.__ignore_certain
        self.__ignore_certain = True
        self.__on_whatever(call_operand)
        self.__ignore_certain = ignore_certain_bck

        assert not self.__ongoing  # noqa: S101
        assert self.__outcome.is_certain()  # noqa: S101

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__outcome


class Or(Test):
    """The disjunction of a list of given tests.

    This test succeeds if any `args` succeed.
    """

    def __init__(self, *args: Test, short_circuit: bool = True, ignore_certain: bool = True) -> None:
        """Initialize the disjunction with `args`, `short_circuit`, and `ignore_certain`.

        Args:
            *args: The tests to combine.
            short_circuit: Whether this test should employ short circuit optimization, i.e., abort all remaining tests once the outcome of a test is certainly true.
            ignore_certain: Whether this test should employ the ignore certain optimization, i.e., not send artifacts to test that are already certain.
        """
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
                i_str = str(i)
                operands += os.linesep
                operands += (width - len(i_str)) * " "
                operands += [" ", "*"][operand in self.__ongoing]
                operands += f"{i_str}: {operand}"
            operands = indent(operands, 8 * " ")
        else:
            operands = " <none>"

        return os.linesep.join(
            [
                f"[{self.outcome()}] {self.__class__.__name__} ",
                f"    operands:{operands}",
                f"    short_circuit:  {self.__short_circuit}",
                f"    ignore_certain: {self.__ignore_certain}",
            ]
        )

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

    @override
    def on_model(self, model: Model) -> bool:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_model(model)

        return self.__on_whatever(call_operand)

    @override
    def on_unsat(self, lower_bound: Sequence[int]) -> None:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_unsat(lower_bound)

        self.__on_whatever(call_operand)

    @override
    def on_core(self, core: Sequence[int]) -> None:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_core(core)

        self.__on_whatever(call_operand)

    @override
    def on_statistics(self, step: StatisticsMap, accumulated: StatisticsMap) -> None:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_statistics(step, accumulated)

        self.__on_whatever(call_operand)

    @override
    def on_finish(self, result: SolveResult) -> None:  # noqa: D102
        def call_operand(operand: Test) -> None:
            operand.on_finish(result)

        ignore_certain_bck = self.__ignore_certain
        self.__ignore_certain = True
        self.__on_whatever(call_operand)
        self.__ignore_certain = ignore_certain_bck

        assert not self.__ongoing  # noqa: S101
        assert self.__outcome.is_certain()  # noqa: S101

    @override
    def outcome(self) -> Outcome:  # noqa: D102
        return self.__outcome
