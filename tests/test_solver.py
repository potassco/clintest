import pytest

from clintest.assertion import Contains
from clintest.protocol import PersistedModel, PersistedSolveResult
from clintest.quantifier import Any
from clintest.solver import Clingo, Iterate
from clintest.test import Assert, Record, Recording, True_


@pytest.mark.parametrize(
    ("solver", "test", "recording"),
    [
        pytest.param(
            Clingo("0", "a :- not a."),
            True_(lazy=False),
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
            id="clingo(a :- not a.) true(lazy=False)",
        ),
        pytest.param(
            Clingo("0", "a. {b}."),
            True_(lazy=False),
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
            id="clingo(a. {b}.) true(lazy=False)",
        ),
        pytest.param(
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
            id="clingo(a. {b}.) any contains a",
        ),
        pytest.param(
            Iterate([]),
            True_(lazy=False),
            Recording(
                [
                    {"__f": "__init__"},
                    {
                        "__f": "on_finish",
                        "result": PersistedSolveResult(
                            exhausted=True, interrupted=False, satisfiable=False, unsatisfiable=True
                        ),
                    },
                ]
            ),
            id="iterate() true(lazy=False)",
        ),
        pytest.param(
            Iterate(
                [
                    PersistedModel.from_str("a").modify(number=1),
                    PersistedModel.from_str("b a").modify(number=2),
                ]
            ),
            True_(lazy=False),
            Recording(
                [
                    {"__f": "__init__"},
                    {"__f": "on_model", "model": PersistedModel.from_str("a").modify(number=1)},
                    {"__f": "on_model", "model": PersistedModel.from_str("b a").modify(number=2)},
                    {
                        "__f": "on_finish",
                        "result": PersistedSolveResult(
                            exhausted=True, interrupted=False, satisfiable=True, unsatisfiable=False
                        ),
                    },
                ]
            ),
            id="iterate(a, b a) true(lazy=False)",
        ),
        pytest.param(
            Iterate(
                [
                    PersistedModel.from_str("a").modify(number=1),
                    PersistedModel.from_str("b a").modify(number=2),
                ]
            ),
            Assert(Any(), Contains("a")),
            Recording(
                [
                    {"__f": "__init__"},
                    {"__f": "on_model", "model": PersistedModel.from_str("a").modify(number=1)},
                    {
                        "__f": "on_finish",
                        "result": PersistedSolveResult(
                            exhausted=False, interrupted=False, satisfiable=True, unsatisfiable=False
                        ),
                    },
                ]
            ),
            id="iterate(a, b a) any contains a",
        ),
    ],
)
def test_solver(solver, test, recording):
    test = Record(test)
    solver.solve(test)
    assert recording.subsumes(test.recording)
