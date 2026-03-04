from clingo.symbol import parse_term
from clingo.control import Control
from clintest.model import PersistedModel


def test_persisted_model():
    ctl = Control(["0"])
    ctl.add("base", [], "1 { a; b } 1. #show b/0. #show c : a.")
    ctl.ground([("base", [])])

    expected = [
        PersistedModel(
            number=1,
            symbols={
                "atoms": [parse_term("b")],
                "terms": [],
                "shown": [parse_term("b")],
                "theory": [],
            },
        ),
        PersistedModel(
            number=2,
            symbols={
                "atoms": [parse_term("a")],
                "terms": [parse_term("c")],
                "shown": [parse_term("c")],
                "theory": [],
            },
        ),
    ]

    with ctl.solve(yield_=True) as handle:
        for clingo_model, expected_model in zip(handle, expected, strict=True):
            persisted_model = PersistedModel.of(clingo_model)

            assert persisted_model == expected_model

            assert clingo_model.cost == expected_model.cost
            assert clingo_model.number == expected_model.number
            assert clingo_model.optimality_proven == expected_model.optimality_proven
            assert clingo_model.priority == expected_model.priority
            assert clingo_model.type == expected_model.type

            assert list(clingo_model.symbols(atoms=True)) == expected_model.symbols(atoms=True)
            assert list(clingo_model.symbols(terms=True)) == expected_model.symbols(terms=True)
            assert list(clingo_model.symbols(shown=True)) == expected_model.symbols(shown=True)
            assert list(clingo_model.symbols(theory=True)) == expected_model.symbols(theory=True)
