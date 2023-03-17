# pylint: disable=import-outside-toplevel


def test_assert_all():
    from clintest.solver import Clingo
    from clintest.test import Assert, Inspect
    from clintest.quantifier import All
    from clintest.assertion import Contains

    solver = Clingo("0", "a. {b}.")

    test = Inspect(Assert(All(), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[1]["str(model)"] == "b a"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"

    test = Inspect(Assert(All(), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()

    assert len(test.artifacts) == 3
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_statistics"
    assert test.artifacts[2]["__f"] == "on_finish"


def test_assert_any():
    from clintest.solver import Clingo
    from clintest.test import Assert, Inspect
    from clintest.quantifier import Any
    from clintest.assertion import Contains

    solver = Clingo("0", "a. {b}.")

    test = Inspect(Assert(Any(), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()

    assert len(test.artifacts) == 3
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_statistics"
    assert test.artifacts[2]["__f"] == "on_finish"

    test = Inspect(Assert(Any(), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[1]["str(model)"] == "b a"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"

    test = Inspect(Assert(Any(), Contains("c")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[1]["str(model)"] == "b a"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"


def test_assert_exact():
    from clintest.solver import Clingo
    from clintest.test import Assert, Inspect
    from clintest.quantifier import Exact
    from clintest.assertion import Contains

    solver = Clingo("0", "a. {b}.")

    test = Inspect(Assert(Exact(0), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()

    assert len(test.artifacts) == 3
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_statistics"
    assert test.artifacts[2]["__f"] == "on_finish"

    test = Inspect(Assert(Exact(1), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[1]["str(model)"] == "b a"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"

    test = Inspect(Assert(Exact(2), Contains("a")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[1]["str(model)"] == "b a"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"

    test = Inspect(Assert(Exact(0), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[1]["str(model)"] == "b a"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"

    test = Inspect(Assert(Exact(1), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_true()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[1]["str(model)"] == "b a"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"

    test = Inspect(Assert(Exact(2), Contains("b")))
    solver.solve(test)

    assert test.outcome().is_certainly_false()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[1]["str(model)"] == "b a"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"


def test_true():
    from clintest.solver import Clingo
    from clintest.test import True_, Inspect

    solver = Clingo("0", "{a}.")

    test = Inspect(True_())
    solver.solve(test)

    assert test.outcome().is_certainly_true()

    assert len(test.artifacts) == 3
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[1]["__f"] == "on_statistics"
    assert test.artifacts[2]["__f"] == "on_finish"

    test = Inspect(True_(lazy_evaluation = False))
    solver.solve(test)

    assert test.outcome().is_certainly_true()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"


def test_false():
    from clintest.solver import Clingo
    from clintest.test import False_, Inspect

    solver = Clingo("0", "{a}.")

    test = Inspect(False_())
    solver.solve(test)

    assert test.outcome().is_certainly_false()

    assert len(test.artifacts) == 3
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[1]["__f"] == "on_statistics"
    assert test.artifacts[2]["__f"] == "on_finish"

    test = Inspect(False_(lazy_evaluation = False))
    solver.solve(test)

    assert test.outcome().is_certainly_false()

    assert len(test.artifacts) == 4
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[1]["__f"] == "on_model"
    assert test.artifacts[2]["__f"] == "on_statistics"
    assert test.artifacts[3]["__f"] == "on_finish"
