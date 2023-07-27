# pylint: disable=import-outside-toplevel
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=duplicate-code


def test_clingo():
    from clintest.solver import Clingo
    from clintest.test import Record, Recording

    solver = Clingo("0", "a.")
    test = Record()

    solver.solve(test)
    assert Recording([
        {'__f': '__init__'},
        {'__f': 'on_model', 'str(model)': 'a'},
        {'__f': 'on_statistics'},
        {'__f': 'on_finish'},
    ]).subsumes(test.recording)
