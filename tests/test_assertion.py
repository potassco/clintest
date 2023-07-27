# pylint: disable=import-outside-toplevel
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name


from clingo import Control
import pytest


@pytest.fixture
def frame():
    ctl = Control(["0"])
    ctl.add("base", [], "a. b.")
    ctl.ground([("base", [])])

    def test(positive, negative):
        for model in ctl.solve(yield_=True):
            for assertion in positive:
                assert     assertion.holds_for(model)
            for assertion in negative:
                assert not assertion.holds_for(model)

    return test


def test_contains(frame):
    from clintest.assertion import Contains
    frame([
        Contains("a"),
        Contains("b"),
    ], [
        Contains("c"),
    ])


def test_equals(frame):
    from clintest.assertion import Equals
    frame([
        Equals({"a", "b"}),
    ], [
        Equals({"a"}),
        Equals({"a", "b", "c"}),
    ])


def test_subsetof(frame):
    from clintest.assertion import SubsetOf
    frame([
        SubsetOf({"a", "b"}),
        SubsetOf({"a", "b", "c"}),
    ], {
        SubsetOf({"a"}),
    })


def test_supersetof(frame):
    from clintest.assertion import SupersetOf
    frame([
        SupersetOf({"a"}),
        SupersetOf({"a", "b"}),
    ], {
        SupersetOf({"a", "b", "c"}),
    })


def test_true(frame):
    from clintest.assertion import True_
    frame([True_()], [])


def test_false(frame):
    from clintest.assertion import False_
    frame([], [False_()])


def test_not(frame):
    from clintest.assertion import Not, True_, False_
    frame([Not(False_())], [Not(True_())])


def test_and(frame):
    from clintest.assertion import And, True_, False_
    frame([
        And(),
        And(True_(), True_()),
    ], [
        And(True_(), False_()),
        And(False_(), True_()),
        And(False_(), False_()),
    ])


def test_or(frame):
    from clintest.assertion import Or, True_, False_
    frame([
        Or(True_(), True_()),
        Or(True_(), False_()),
        Or(False_(), True_()),
    ], [
        Or(),
        Or(False_(), False_()),
    ])
