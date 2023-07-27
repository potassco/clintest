# pylint: disable=import-outside-toplevel
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name


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


def test_and(solver, recording_no_model):
    from clintest.test import False_, True_, And, Record

    inner = [Record(test) for test in [False_(), False_()]]
    outer = Record(And(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_false()
    assert recording_no_model.subsumes(outer.recording)
    assert recording_no_model.subsumes(inner[0].recording)
    assert recording_no_model.subsumes(inner[1].recording)

    inner = [Record(test) for test in [False_(), True_()]]
    outer = Record(And(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_false()
    assert recording_no_model.subsumes(outer.recording)
    assert recording_no_model.subsumes(inner[0].recording)
    assert recording_no_model.subsumes(inner[1].recording)

    inner = [Record(test) for test in [True_(), False_()]]
    outer = Record(And(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_false()
    assert recording_no_model.subsumes(outer.recording)
    assert recording_no_model.subsumes(inner[0].recording)
    assert recording_no_model.subsumes(inner[1].recording)

    inner = [Record(test) for test in [True_(), True_()]]
    outer = Record(And(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_true()
    assert recording_no_model.subsumes(outer.recording)
    assert recording_no_model.subsumes(inner[0].recording)
    assert recording_no_model.subsumes(inner[1].recording)


def test_and_ignore_certain(solver, recording_two_models):
    from clintest.test import And, Assert, Record, Recording
    from clintest.assertion import Contains
    from clintest.quantifier import Any

    inner = [Record(test) for test in [
        Assert(Any(), Contains("a")),
        Assert(Any(), Contains("b"))
    ]]
    outer = Record(And(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_true()
    assert recording_two_models.subsumes(outer.recording)
    assert Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'},
    ]).subsumes(inner[0].recording)
    assert Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'},
        {'__f': 'on_model', 'str(model)': 'b a'},
    ]).subsumes(inner[1].recording)

    inner = [Record(test) for test in [
        Assert(Any(), Contains("a")),
        Assert(Any(), Contains("b"))
    ]]
    outer = Record(And(*inner, ignore_certain=False))
    solver.solve(outer)
    assert outer.outcome().is_certainly_true()
    assert recording_two_models.subsumes(outer.recording)
    assert recording_two_models.subsumes(inner[0].recording)
    assert recording_two_models.subsumes(inner[1].recording)


def test_and_short_circuit(solver, recording_one_model, recording_two_models):
    from clintest.test import And, Assert, Record, Recording
    from clintest.assertion import Contains
    from clintest.quantifier import All

    inner = [Record(test) for test in [
        Assert(All(), Contains('b')),
        Assert(All(), Contains('a'))
    ]]
    outer = Record(And(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_false()
    assert recording_one_model.subsumes(outer.recording)
    assert Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'}
    ]).subsumes(inner[0].recording)
    assert Recording([
        {'__f': '__init__'},
    ]).subsumes(inner[1].recording)

    inner = [Record(test) for test in [
        Assert(All(), Contains('b')),
        Assert(All(), Contains('a'))
    ]]
    outer = Record(And(*inner, short_circuit=False))
    solver.solve(outer)
    assert outer.outcome().is_certainly_false()
    assert recording_two_models.subsumes(outer.recording)
    assert Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'}
    ]).subsumes(inner[0].recording)
    assert recording_two_models.subsumes(inner[1].recording)


def test_or(solver, recording_no_model):
    from clintest.test import False_, True_, Or, Record

    inner = [Record(test) for test in [False_(), False_()]]
    outer = Record(Or(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_false()
    assert recording_no_model.subsumes(outer.recording)
    assert recording_no_model.subsumes(inner[0].recording)
    assert recording_no_model.subsumes(inner[1].recording)

    inner = [Record(test) for test in [False_(), True_()]]
    outer = Record(Or(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_true()
    assert recording_no_model.subsumes(outer.recording)
    assert recording_no_model.subsumes(inner[0].recording)
    assert recording_no_model.subsumes(inner[1].recording)

    inner = [Record(test) for test in [True_(), False_()]]
    outer = Record(Or(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_true()
    assert recording_no_model.subsumes(outer.recording)
    assert recording_no_model.subsumes(inner[0].recording)
    assert recording_no_model.subsumes(inner[1].recording)

    inner = [Record(test) for test in [True_(), True_()]]
    outer = Record(Or(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_true()
    assert recording_no_model.subsumes(outer.recording)
    assert recording_no_model.subsumes(inner[0].recording)
    assert recording_no_model.subsumes(inner[1].recording)


def test_or_ignore_certain(solver, recording_two_models):
    from clintest.test import Assert, Not, Or, Record, Recording
    from clintest.assertion import Contains
    from clintest.quantifier import Any

    inner = [Record(test) for test in [
        Not(Assert(Any(), Contains("a"))),
        Not(Assert(Any(), Contains("b")))
    ]]
    outer = Record(Or(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_false()
    assert recording_two_models.subsumes(outer.recording)
    assert Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'},
    ]).subsumes(inner[0].recording)
    assert Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'},
        {'__f': 'on_model', 'str(model)': 'b a'},
    ]).subsumes(inner[1].recording)

    inner = [Record(test) for test in [
        Not(Assert(Any(), Contains("a"))),
        Not(Assert(Any(), Contains("b")))
    ]]
    outer = Record(Or(*inner, ignore_certain=False))
    solver.solve(outer)
    assert outer.outcome().is_certainly_false()
    assert recording_two_models.subsumes(outer.recording)
    assert recording_two_models.subsumes(inner[0].recording)
    assert recording_two_models.subsumes(inner[1].recording)


def test_or_short_circuit(solver, recording_one_model, recording_two_models):
    from clintest.test import Assert, Or, Not, Record, Recording
    from clintest.assertion import Contains
    from clintest.quantifier import All

    inner = [Record(test) for test in [
        Not(Assert(All(), Contains('b'))),
        Not(Assert(All(), Contains('a')))
    ]]
    outer = Record(Or(*inner))
    solver.solve(outer)
    assert outer.outcome().is_certainly_true()
    assert recording_one_model.subsumes(outer.recording)
    assert Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'}
    ]).subsumes(inner[0].recording)
    assert Recording([
        {'__f': '__init__'},
    ]).subsumes(inner[1].recording)

    inner = [Record(test) for test in [
        Not(Assert(All(), Contains('b'))),
        Not(Assert(All(), Contains('a')))
    ]]
    outer = Record(Or(*inner, short_circuit=False))
    solver.solve(outer)
    assert outer.outcome().is_certainly_true()
    assert recording_two_models.subsumes(outer.recording)
    assert Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'}
    ]).subsumes(inner[0].recording)
    assert recording_two_models.subsumes(inner[1].recording)
