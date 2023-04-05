# pylint: disable=import-outside-toplevel

import pytest


@pytest.fixture
def solver():
    from clintest.solver import Clingo
    return Clingo("0", "a. {b}.")


@pytest.fixture
def recording_no_model():
    from clintest.test import Recording
    return Recording([
        {'__f': '__init__'},
    ])


@pytest.fixture
def recording_one_model():
    from clintest.test import Recording
    return Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'},
        {'__f': 'on_statistics'},
        {'__f': 'on_finish'},
    ])


@pytest.fixture
def recording_two_models():
    from clintest.test import Recording
    return Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'},
        {'__f': 'on_model', 'str(model)': 'b a'},
        {'__f': 'on_statistics'},
        {'__f': 'on_finish'},
    ])


def test_assert_all(solver, recording_one_model, recording_two_models):
    from clintest.test import Assert, Record
    from clintest.quantifier import All
    from clintest.assertion import Contains

    test = Record(Assert(All(), Contains("a")))
    solver.solve(test)
    assert test.outcome().is_certainly_true()
    assert recording_two_models.subsumes(test.recording)

    test = Record(Assert(All(), Contains("b")))
    solver.solve(test)
    assert test.outcome().is_certainly_false()
    assert recording_one_model.subsumes(test.recording)


def test_assert_any(solver, recording_one_model, recording_two_models):
    from clintest.test import Assert, Record
    from clintest.quantifier import Any
    from clintest.assertion import Contains

    test = Record(Assert(Any(), Contains("a")))
    solver.solve(test)
    assert test.outcome().is_certainly_true()
    assert recording_one_model.subsumes(test.recording)

    test = Record(Assert(Any(), Contains("b")))
    solver.solve(test)
    assert test.outcome().is_certainly_true()
    assert recording_two_models.subsumes(test.recording)

    test = Record(Assert(Any(), Contains("c")))
    solver.solve(test)
    assert test.outcome().is_certainly_false()
    assert recording_two_models.subsumes(test.recording)


def test_assert_exact(solver, recording_one_model, recording_two_models):
    from clintest.test import Assert, Record
    from clintest.quantifier import Exact
    from clintest.assertion import Contains

    test = Record(Assert(Exact(0), Contains("a")))
    solver.solve(test)
    assert test.outcome().is_certainly_false()
    assert recording_one_model.subsumes(test.recording)

    test = Record(Assert(Exact(1), Contains("a")))
    solver.solve(test)
    assert test.outcome().is_certainly_false()
    recording_two_models.subsumes(test.recording)

    test = Record(Assert(Exact(2), Contains("a")))
    solver.solve(test)
    assert test.outcome().is_certainly_true()
    recording_two_models.subsumes(test.recording)

    test = Record(Assert(Exact(0), Contains("b")))
    solver.solve(test)
    assert test.outcome().is_certainly_false()
    recording_two_models.subsumes(test.recording)

    test = Record(Assert(Exact(1), Contains("b")))
    solver.solve(test)
    assert test.outcome().is_certainly_true()
    recording_two_models.subsumes(test.recording)

    test = Record(Assert(Exact(2), Contains("b")))
    solver.solve(test)
    assert test.outcome().is_certainly_false()
    recording_two_models.subsumes(test.recording)


def test_true(solver, recording_no_model, recording_two_models):
    from clintest.test import True_, Record

    test = Record(True_())
    solver.solve(test)
    assert test.outcome().is_certainly_true()
    assert recording_no_model.subsumes(test.recording)

    test = Record(True_(lazy = False))
    solver.solve(test)
    assert test.outcome().is_certainly_true()
    assert recording_two_models.subsumes(test.recording)


def test_false(solver, recording_no_model, recording_two_models):
    from clintest.test import False_, Record

    test = Record(False_())
    solver.solve(test)
    assert test.outcome().is_certainly_false()
    assert recording_no_model.subsumes(test.recording)

    test = Record(False_(lazy = False))
    solver.solve(test)
    assert test.outcome().is_certainly_false()
    assert recording_two_models.subsumes(test.recording)


def test_not(solver, recording_no_model):
    from clintest.test import False_, True_, Not, Record

    inner = Record(False_())
    outer = Record(Not(inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_true()
    assert recording_no_model.subsumes(inner.recording)
    assert recording_no_model.subsumes(outer.recording)

    inner = Record(True_())
    outer = Record(Not(inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_false()
    assert recording_no_model.subsumes(inner.recording)
    assert recording_no_model.subsumes(outer.recording)


# TODO: Write tests for And and Or and remove the following!
def test_issue():
    from clintest.solver import Clingo
    from clintest.test import And, Assert
    from clintest.quantifier import Any, Exact
    from clintest.assertion import Contains, Not, True_

    solver = Clingo("0", "a. {b}.")

    test = And(
        Assert(Exact(2), True_()),
        Assert(Any(), Contains("b")),
        Assert(Any(), Not(Contains("b")))
    )

    solver.solve(test)

    assert test.outcome().is_certainly_true()
