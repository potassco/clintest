import pytest
from clingo import Control

from clintest.assertion import And, Contains, Equals, Equivalent, False_, Implies, Not, Or, SubsetOf, SupersetOf, True_


@pytest.fixture
def frame():
    ctl = Control(["0"])
    ctl.add("base", [], "a. b.")
    ctl.ground([("base", [])])

    def test(positive, negative):
        for model in ctl.solve(yield_=True):
            for assertion in positive:
                assert assertion.holds_for(model)
            for assertion in negative:
                assert not assertion.holds_for(model)

    return test


def test_contains(frame):
    frame(
        [
            Contains("a"),
            Contains("b"),
        ],
        [
            Contains("c"),
        ],
    )


def test_equals(frame):
    frame(
        [
            Equals({"a", "b"}),
        ],
        [
            Equals({"a"}),
            Equals({"a", "b", "c"}),
        ],
    )


def test_subsetof(frame):
    frame(
        [
            SubsetOf({"a", "b"}),
            SubsetOf({"a", "b", "c"}),
        ],
        {
            SubsetOf({"a"}),
        },
    )


def test_supersetof(frame):
    frame(
        [
            SupersetOf({"a"}),
            SupersetOf({"a", "b"}),
        ],
        {
            SupersetOf({"a", "b", "c"}),
        },
    )


def test_true(frame):
    frame([True_()], [])


def test_false(frame):
    frame([], [False_()])


def test_not(frame):
    frame([Not(False_())], [Not(True_())])


def test_and(frame):
    frame(
        [
            And(),
            And(True_(), True_()),
        ],
        [
            And(True_(), False_()),
            And(False_(), True_()),
            And(False_(), False_()),
        ],
    )


def test_or(frame):
    frame(
        [
            Or(True_(), True_()),
            Or(True_(), False_()),
            Or(False_(), True_()),
        ],
        [
            Or(),
            Or(False_(), False_()),
        ],
    )


def test_implies(frame):
    frame(
        [
            Implies(False_(), False_()),
            Implies(False_(), True_()),
            Implies(True_(), True_()),
        ],
        [
            Implies(True_(), False_()),
        ],
    )


def test_equivalent(frame):
    frame(
        [
            Equivalent(),
            Equivalent(False_()),
            Equivalent(True_()),
            Equivalent(False_(), False_()),
            Equivalent(True_(), True_()),
        ],
        [
            Equivalent(False_(), True_()),
            Equivalent(True_(), False_()),
        ],
    )
