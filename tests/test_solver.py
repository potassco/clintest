# pylint: disable=import-outside-toplevel


def test_clingo():
    from clintest.solver import Clingo
    from clintest.test import Inspect

    solver = Clingo("0", "a.")
    test = Inspect()

    solver.solve(test)

    assert len(test.artifacts) == 3
    assert test.artifacts[0]["__f"] == "on_model"
    assert test.artifacts[0]["str(model)"] == "a"
    assert test.artifacts[1]["__f"] == "on_statistics"
    assert test.artifacts[2]["__f"] == "on_finish"
