# pylint: disable=import-outside-toplevel


def test_assert_all():
    from clintest.solver import Clingo
    from clintest.test import Assert
    from clintest.quantifier import All
    from clintest.assertion import Contains

    solver = Clingo("0", "a. {b}.")

    positive = Assert(All(), Contains("a"))
    negative = Assert(All(), Contains("b"))

    solver.solve(positive)
    solver.solve(negative)

    assert positive.outcome().is_certainly_true()
    assert negative.outcome().is_certainly_false()


def test_assert_any():
    from clintest.solver import Clingo
    from clintest.test import Assert
    from clintest.quantifier import Any
    from clintest.assertion import Contains

    solver = Clingo("0", "a. {b}.")

    positive = Assert(Any(), Contains("b"))
    negative = Assert(Any(), Contains("c"))

    solver.solve(positive)
    solver.solve(negative)

    assert positive.outcome().is_certainly_true()
    assert negative.outcome().is_certainly_false()


def test_assert_exact():
    from clintest.solver import Clingo
    from clintest.test import Assert
    from clintest.quantifier import Exact
    from clintest.assertion import Contains

    solver = Clingo("0", "a. {b}.")

    positive = Assert(Exact(1), Contains("b"))
    negative = Assert(Exact(2), Contains("b"))

    solver.solve(positive)
    solver.solve(negative)

    assert positive.outcome().is_certainly_true()
    assert negative.outcome().is_certainly_false()


def test_true():
    from clintest.solver import Clingo
    from clintest.test import True_

    solver = Clingo("0", "")
    test = True_()

    solver.solve(test)
    assert test.outcome().is_certainly_true()


def test_false():
    from clintest.solver import Clingo
    from clintest.test import False_

    solver = Clingo("0", "")
    test = False_()

    solver.solve(test)
    assert test.outcome().is_certainly_false()
