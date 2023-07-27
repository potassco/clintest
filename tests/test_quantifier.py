# pylint: disable=import-outside-toplevel
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-builtin


def test_all():
    from clintest.quantifier import All
    quantifier = All()

    assert quantifier.outcome().as_tuple() == (True, False)

    input = 2 * [True, False]
    output = [quantifier.consume(value).as_tuple() for value in input]

    assert output == [
        (True, False),
        (False, True),
        (False, True),
        (False, True),
    ]


def test_any():
    from clintest.quantifier import Any
    quantifier = Any()

    assert quantifier.outcome().as_tuple() == (False, False)

    input = 2 * [False, True]
    output = [quantifier.consume(value).as_tuple() for value in input]

    assert output == [
        (False, False),
        (True, True),
        (True, True),
        (True, True),
    ]

def test_exact():
    from clintest.quantifier import Exact
    quantifier = Exact(2)

    assert quantifier.outcome().as_tuple() == (False, False)

    input = 4 * [False, True]
    output = [quantifier.consume(value).as_tuple() for value in input]

    assert output == [
        (False, False),
        (False, False),
        (False, False),
        (True, False),
        (True, False),
        (False, True),
        (False, True),
        (False, True),
    ]
