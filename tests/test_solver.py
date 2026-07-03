import pytest

from clintest.assertion import Contains
from clintest.protocol import PersistedModel, PersistedSolveResult
from clintest.quantifier import Any
from clintest.solver import Clingo
from clintest.test import Assert, Record, Recording


@pytest.mark.parametrize(
    "solver, test, recording",
    [
        (
            Clingo("0", "a :- not a."),
            None,
            Recording(
                [
                    {"__f": "__init__"},
                    {"__f": "on_statistics"},
                    {
                        "__f": "on_finish",
                        "result": PersistedSolveResult(
                            exhausted=True, interrupted=False, satisfiable=False, unsatisfiable=True
                        ),
                    },
                    {"__f": "on_core"},
                ]
            ),
        ),
        (
            Clingo("0", "a. {b}."),
            None,
            Recording(
                [
                    {"__f": "__init__"},
                    {"__f": "on_model", "model": PersistedModel.from_str("a").modify(number=1)},
                    {"__f": "on_model", "model": PersistedModel.from_str("b a").modify(number=2)},
                    {"__f": "on_statistics"},
                    {
                        "__f": "on_finish",
                        "result": PersistedSolveResult(
                            exhausted=True, interrupted=False, satisfiable=True, unsatisfiable=False
                        ),
                    },
                ]
            ),
        ),
        (
            Clingo("0", "a. {b}."),
            Assert(Any(), Contains("a")),
            Recording(
                [
                    {"__f": "__init__"},
                    {"__f": "on_model", "model": PersistedModel.from_str("a").modify(number=1)},
                    {"__f": "on_statistics"},
                    {
                        "__f": "on_finish",
                        "result": PersistedSolveResult(
                            exhausted=False, interrupted=False, satisfiable=True, unsatisfiable=False
                        ),
                    },
                ]
            ),
        ),
    ],
)
def test_solver(solver, test, recording):
    test = Record(test)
    solver.solve(test)
    assert recording.subsumes(test.recording)
