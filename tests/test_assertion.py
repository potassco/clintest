# pylint: disable=import-outside-toplevel
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


def test_true(frame):
    from clintest.assertion import True_
    frame([True_()], [])


def test_false(frame):
    from clintest.assertion import False_
    frame([], [False_()])


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


def test_superset(frame):
    from clintest.assertion import SupersetOf
    frame([
        SupersetOf({"a"}),
        SupersetOf({"a", "b"}),
    ], {
        SupersetOf({"a", "b", "c"}),
    })
