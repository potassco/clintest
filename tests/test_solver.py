import pytest

from clintest.assertion import Contains
from clintest.protocol import PersistedModel, PersistedSolveResult
from clintest.quantifier import Any
from clintest.solver import Clingo, Iterate
from clintest.test import Assert, Record, Recording, True_

MODELS = [
    PersistedModel.from_str("a").modify(number=1),
    PersistedModel.from_str("b a").modify(number=2),
]

ENTRIES = {
    "i": {"__f": "__init__"},
    "m(a)": {"__f": "on_model", "model": PersistedModel.from_str("a").modify(number=1)},
    "m(b,a)": {"__f": "on_model", "model": PersistedModel.from_str("b a").modify(number=2)},
    "s": {"__f": "on_statistics"},
    "c": {"__f": "on_core"},
    "f(e,u)": {
        "__f": "on_finish",
        "result": PersistedSolveResult(exhausted=True, interrupted=False, satisfiable=False, unsatisfiable=True),
    },
    "f(e,s)": {
        "__f": "on_finish",
        "result": PersistedSolveResult(exhausted=True, interrupted=False, satisfiable=True, unsatisfiable=False),
    },
    "f(s)": {
        "__f": "on_finish",
        "result": PersistedSolveResult(exhausted=False, interrupted=False, satisfiable=True, unsatisfiable=False),
    },
}


@pytest.mark.parametrize(
    ("solver", "test", "recording"),
    [
        pytest.param(
            Clingo("0", "a :- not a."),
            True_(lazy=False),
            "i s f(e,u) c",
            id="clingo(a :- not a.) true(lazy=False)",
        ),
        pytest.param(
            Clingo("0", "a. {b}."),
            True_(lazy=False),
            "i m(a) m(b,a) s f(e,s)",
            id="clingo(a. {b}.) true(lazy=False)",
        ),
        pytest.param(
            Clingo("0", "a. {b}."),
            Assert(Any(), Contains("a")),
            "i m(a) s f(s)",
            id="clingo(a. {b}.) any contains a",
        ),
        pytest.param(Iterate([]), True_(lazy=False), "i f(e,u)", id="iterate() true(lazy=False)"),
        pytest.param(Iterate(MODELS), True_(lazy=False), "i m(a) m(b,a) f(e,s)", id="iterate(a, b a) true(lazy=False)"),
        pytest.param(Iterate(MODELS), Assert(Any(), Contains("a")), "i m(a) f(s)", id="iterate(a, b a) any contains a"),
    ],
)
def test_solver(solver, test, recording):
    record = Record(test)
    solver.solve(record)
    assert Recording([ENTRIES[entry] for entry in recording.split()]).subsumes(record.recording)
