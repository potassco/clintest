# pylint: disable=import-outside-toplevel

# TODO: Rewrite all these tests with the new Recording

def assert_execution_3(test):
    assert len(test.artifacts) == 3
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_statistics"
    assert test.artifacts[2]["__f"] == "on_finish"


def assert_execution_4(test):
    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[1]["str(model)"] == "b a"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"


def test_assert_all():
    from clintest.solver import Clingo
    from clintest.test import Assert, Inspect
    from clintest.quantifier import All
    from clintest.assertion import Contains

    solver = Clingo("0", "a. {b}.")

    test = Inspect(Assert(All(), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()
    assert_execution_4(test)

    test = Inspect(Assert(All(), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()
    assert_execution_3(test)


def test_assert_any():
    from clintest.solver import Clingo
    from clintest.test import Assert, Inspect
    from clintest.quantifier import Any
    from clintest.assertion import Contains

    solver = Clingo("0", "a. {b}.")

    test = Inspect(Assert(Any(), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()
    assert_execution_3(test)

    test = Inspect(Assert(Any(), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()
    assert_execution_4(test)

    test = Inspect(Assert(Any(), Contains("c")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()
    assert_execution_4(test)


def test_assert_exact():
    from clintest.solver import Clingo
    from clintest.test import Assert, Inspect
    from clintest.quantifier import Exact
    from clintest.assertion import Contains

    solver = Clingo("0", "a. {b}.")

    test = Inspect(Assert(Exact(0), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()
    assert_execution_3(test)

    test = Inspect(Assert(Exact(1), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()
    assert_execution_4(test)

    test = Inspect(Assert(Exact(2), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()
    assert_execution_4(test)

    test = Inspect(Assert(Exact(0), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()
    assert_execution_4(test)

    test = Inspect(Assert(Exact(1), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()
    assert_execution_4(test)

    test = Inspect(Assert(Exact(2), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()
    assert_execution_4(test)


def test_true():
    from clintest.solver import Clingo
    from clintest.test import True_, Inspect

    solver = Clingo("0", "a. {b}.")

    test = Inspect(True_())
    solver.solve(test)

    assert test.outcome().is_certainly_true()
    assert_execution_3(test)

    test = Inspect(True_(lazy = False))
    solver.solve(test)

    assert test.outcome().is_certainly_true()
    assert_execution_4(test)


def test_false():
    from clintest.solver import Clingo
    from clintest.test import False_, Inspect

    solver = Clingo("0", "a. {b}.")

    test = Inspect(False_())
    solver.solve(test)

    assert test.outcome().is_certainly_false()
    assert_execution_3(test)

    test = Inspect(False_(lazy = False))
    solver.solve(test)

    assert test.outcome().is_certainly_false()
    assert_execution_4(test)


def test_not():
    from clintest.solver import Clingo
    from clintest.test import False_, True_, Not, Inspect

    solver = Clingo("0", "a. {b}.")

    inner = Inspect(False_())
    outer = Inspect(Not(inner))
    solver.solve(outer)

    assert outer.outcome().is_certainly_true()
    assert_execution_3(inner)
    assert_execution_3(outer)

    inner = Inspect(False_(lazy = False))
    outer = Inspect(Not(inner))
    solver.solve(outer)

    assert outer.outcome().is_certainly_true()
    assert_execution_4(inner)
    assert_execution_4(outer)

    inner = Inspect(True_())
    outer = Inspect(Not(inner))
    solver.solve(outer)

    assert outer.outcome().is_certainly_false()
    assert_execution_3(inner)
    assert_execution_3(outer)

    inner = Inspect(True_(lazy = False))
    outer = Inspect(Not(inner))
    solver.solve(outer)

    assert outer.outcome().is_certainly_false()
    assert_execution_4(inner)
    assert_execution_4(outer)

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
