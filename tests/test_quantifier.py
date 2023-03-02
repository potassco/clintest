# pylint: disable=import-outside-toplevel


def test_all():
    from clintest.quantifier import All
    quantifier = All()

    input = 2 * [True, False]
    output = list(quantifier.consume_all(input))

    assert output == [
        (True, True),
        (False, False),
        (False, False),
        (False, False),
    ]


def test_any():
    from clintest.quantifier import Any
    quantifier = Any()

    input = 2 * [False, True]
    output = list(quantifier.consume_all(input))

    assert output == [
        (False, True),
        (True, False),
        (True, False),
        (True, False),
    ]

def test_exact():
    from clintest.quantifier import Exact
    quantifier = Exact(2)

    input = 4 * [False, True]
    output = list(quantifier.consume_all(input))

    assert output == [
        (False, True),
        (False, True),
        (False, True),
        (True, True),
        (True, True),
        (False, False),
        (False, False),
        (False, False),
    ]
