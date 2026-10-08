from collections.abc import Hashable
from functools import partial

import pytest

from clintest.assertion import Contains
from clintest.protocol import PersistedModel
from clintest.quantifier import All, Any, Exact, First, Last
from clintest.solver import Clingo
from clintest.test import And, Assert, False_, Not, Or, Record, Recording, True_

SOLVER = Clingo("0", "a. {b}.")

ENTRIES = {
    "i": {"__f": "__init__"},
    "m(a)": {"__f": "on_model", "model": PersistedModel.from_str("a").modify(number=1)},
    "m(b,a)": {"__f": "on_model", "model": PersistedModel.from_str("b a").modify(number=2)},
    "s": {"__f": "on_statistics"},
    "f": {"__f": "on_finish"},
}


@pytest.mark.parametrize(
    ("test", "outcome", "recording"),
    [
        pytest.param(Assert(All(), Contains("a")), "T!", "i m(a) m(b,a) s f", id="all contains a = T!"),
        pytest.param(Assert(All(), Contains("b")), "F!", "i m(a) s f", id="all contains b = F!"),
        pytest.param(Assert(Any(), Contains("a")), "T!", "i m(a) s f", id="any contains a = T!"),
        pytest.param(Assert(Any(), Contains("b")), "T!", "i m(a) m(b,a) s f", id="any contains b = T!"),
        pytest.param(Assert(Any(), Contains("c")), "F!", "i m(a) m(b,a) s f", id="any contains c = F!"),
        pytest.param(Assert(First(), Contains("a")), "T!", "i m(a) s f", id="first contains a = T!"),
        pytest.param(Assert(First(), Contains("b")), "F!", "i m(a) s f", id="first contains b = F!"),
        pytest.param(Assert(Last(), Contains("a")), "T!", "i m(a) m(b,a) s f", id="last contains a = T!"),
        pytest.param(Assert(Last(), Contains("b")), "T!", "i m(a) m(b,a) s f", id="last contains b = T!"),
        pytest.param(Assert(Last(), Contains("c")), "F!", "i m(a) m(b,a) s f", id="last contains c = F!"),
        pytest.param(Assert(Exact(0), Contains("a")), "F!", "i m(a) s f", id="exact(0) contains a = F!"),
        pytest.param(Assert(Exact(1), Contains("a")), "F!", "i m(a) m(b,a) s f", id="exact(1) contains a = F!"),
        pytest.param(Assert(Exact(2), Contains("a")), "T!", "i m(a) m(b,a) s f", id="exact(2) contains a = T!"),
        pytest.param(Assert(Exact(0), Contains("b")), "F!", "i m(a) m(b,a) s f", id="exact(0) contains b = F!"),
        pytest.param(Assert(Exact(1), Contains("b")), "T!", "i m(a) m(b,a) s f", id="exact(1) contains b = T!"),
        pytest.param(Assert(Exact(2), Contains("b")), "F!", "i m(a) m(b,a) s f", id="exact(2) contains b = F!"),
        pytest.param(True_(), "T!", "i", id="true = T!"),
        pytest.param(True_(lazy=False), "T!", "i m(a) m(b,a) s f", id="true(lazy=False) = T!"),
        pytest.param(False_(), "F!", "i", id="false = F!"),
        pytest.param(False_(lazy=False), "F!", "i m(a) m(b,a) s f", id="false(lazy=False) = F!"),
        pytest.param(And(), "T!", "i", id="and() = T!"),
        pytest.param(Or(), "F!", "i", id="or() = F!"),
    ],
)
def test_solve(test, outcome, recording):
    record = Record(test)
    SOLVER.solve(record)
    assert str(record.outcome()) == outcome
    assert Recording([ENTRIES[entry] for entry in recording.split()]).subsumes(record.recording)


@pytest.mark.parametrize(
    ("composite", "operands", "outcome", "recording", "operand_recordings"),
    [
        pytest.param(Not, [False_()], "T!", "i", ["i"], id="not F = T!"),
        pytest.param(Not, [True_()], "F!", "i", ["i"], id="not T = F!"),
        pytest.param(And, [False_(), False_()], "F!", "i", ["i", "i"], id="F and F = F!"),
        pytest.param(And, [False_(), True_()], "F!", "i", ["i", "i"], id="F and T = F!"),
        pytest.param(And, [True_(), False_()], "F!", "i", ["i", "i"], id="T and F = F!"),
        pytest.param(And, [True_(), True_()], "T!", "i", ["i", "i"], id="T and T = T!"),
        pytest.param(
            And,
            [Assert(Any(), Contains("a")), Assert(Any(), Contains("b"))],
            "T!",
            "i m(a) m(b,a) s f",
            ["i m(a)", "i m(a) m(b,a)"],
            id="any contains a and any contains b = T!",
        ),
        pytest.param(
            partial(And, ignore_certain=False),
            [Assert(Any(), Contains("a")), Assert(Any(), Contains("b"))],
            "T!",
            "i m(a) m(b,a) s f",
            ["i m(a) m(b,a) s f", "i m(a) m(b,a) s f"],
            id="any contains a and(ignore_certain=False) any contains b = T!",
        ),
        pytest.param(
            And,
            [Assert(All(), Contains("b")), Assert(All(), Contains("a"))],
            "F!",
            "i m(a) s f",
            ["i m(a)", "i"],
            id="all contains b and all contains a = F!",
        ),
        pytest.param(
            partial(And, short_circuit=False),
            [Assert(All(), Contains("b")), Assert(All(), Contains("a"))],
            "F!",
            "i m(a) m(b,a) s f",
            ["i m(a)", "i m(a) m(b,a) s f"],
            id="all contains b and(short_circuit=False) all contains a = F!",
        ),
        pytest.param(Or, [False_(), False_()], "F!", "i", ["i", "i"], id="F or F = F!"),
        pytest.param(Or, [False_(), True_()], "T!", "i", ["i", "i"], id="F or T = T!"),
        pytest.param(Or, [True_(), False_()], "T!", "i", ["i", "i"], id="T or F = T!"),
        pytest.param(Or, [True_(), True_()], "T!", "i", ["i", "i"], id="T or T = T!"),
        pytest.param(
            Or,
            [Not(Assert(Any(), Contains("a"))), Not(Assert(Any(), Contains("b")))],
            "F!",
            "i m(a) m(b,a) s f",
            ["i m(a)", "i m(a) m(b,a)"],
            id="not any contains a or not any contains b = F!",
        ),
        pytest.param(
            partial(Or, ignore_certain=False),
            [Not(Assert(Any(), Contains("a"))), Not(Assert(Any(), Contains("b")))],
            "F!",
            "i m(a) m(b,a) s f",
            ["i m(a) m(b,a) s f", "i m(a) m(b,a) s f"],
            id="not any contains a or(ignore_certain=False) not any contains b = F!",
        ),
        pytest.param(
            Or,
            [Not(Assert(All(), Contains("b"))), Not(Assert(All(), Contains("a")))],
            "T!",
            "i m(a) s f",
            ["i m(a)", "i"],
            id="not all contains b or not all contains a = T!",
        ),
        pytest.param(
            partial(Or, short_circuit=False),
            [Not(Assert(All(), Contains("b"))), Not(Assert(All(), Contains("a")))],
            "T!",
            "i m(a) m(b,a) s f",
            ["i m(a)", "i m(a) m(b,a) s f"],
            id="not all contains b or(short_circuit=False) not all contains a = T!",
        ),
    ],
)
def test_solve_composite(composite, operands, outcome, recording, operand_recordings):
    operand_records = [Record(operand) for operand in operands]
    record = Record(composite(*operand_records))
    SOLVER.solve(record)
    assert str(record.outcome()) == outcome
    assert Recording([ENTRIES[entry] for entry in recording.split()]).subsumes(record.recording)
    for operand_recording, operand_record in zip(operand_recordings, operand_records, strict=True):
        assert Recording([ENTRIES[entry] for entry in operand_recording.split()]).subsumes(operand_record.recording)


@pytest.mark.parametrize(
    ("test", "message"),
    [
        pytest.param(False_(), ["The following test has failed.", "    [F!] False_"], id="F!"),
        pytest.param(True_(lazy=False), ["The following test is incomplete.", "    [T?] True_"], id="T?"),
        pytest.param(False_(lazy=False), ["The following test is incomplete.", "    [F?] False_"], id="F?"),
    ],
)
def test_assert_raises(test, message):
    with pytest.raises(AssertionError) as error:
        test.assert_()
    assert str(error.value).splitlines() == message


def test_assert_passes():
    True_().assert_()


def test_recording_equality():
    entries = [ENTRIES["i"], ENTRIES["m(a)"]]
    assert Recording(entries) == Recording(entries)
    assert Recording(entries) != Recording(entries[:1])
    assert Recording(entries) != entries


def test_recording_unhashable():
    assert not isinstance(Recording(), Hashable)
