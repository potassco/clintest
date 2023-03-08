# pylint: disable=import-outside-toplevel
# pylint: disable=redefined-builtin


def test_all():
    from clintest.quantifier import All
    quantifier = All()

    input = 2 * [True, False]
    output = [quantifier.consume(value).as_tuple() for value in input]

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
    output = [quantifier.consume(value).as_tuple() for value in input]

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
    output = [quantifier.consume(value).as_tuple() for value in input]

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
