from clintest.protocol import PersistedModel


def test_clingo():
    from clintest.solver import Clingo
    from clintest.test import Record, Recording

    solver = Clingo("0", "a.")
    test = Record()

    solver.solve(test)
    assert Recording(
        [
            {"__f": "__init__"},
            {"__f": "on_model", "model": PersistedModel.from_str("a").modify(number=1)},
            {"__f": "on_statistics"},
            {"__f": "on_finish"},
        ]
    ).subsumes(test.recording)
