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


def test_less():
    from clintest.quantifier import Less
    quantifier = Less(2)

    assert quantifier.outcome().as_tuple() == (True, False)

    input = 4 * [False, True]
    output = [quantifier.consume(value).as_tuple() for value in input]

    assert output == [
        (True, False),
        (True, False),
        (True, False),
        (False, True),
        (False, True),
        (False, True),
        (False, True),
        (False, True),
    ]


def test_less_equal():
    from clintest.quantifier import LessEqual
    quantifier = LessEqual(2)

    assert quantifier.outcome().as_tuple() == (True, False)

    input = 4 * [False, True]
    output = [quantifier.consume(value).as_tuple() for value in input]

    assert output == [
        (True, False),
        (True, False),
        (True, False),
        (True, False),
        (True, False),
        (False, True),
        (False, True),
        (False, True),
    ]


def test_greater():
    from clintest.quantifier import Greater
    quantifier = Greater(2)

    assert quantifier.outcome().as_tuple() == (False, False)

    input = 4 * [False, True]
    output = [quantifier.consume(value).as_tuple() for value in input]

    assert output == [
        (False, False),
        (False, False),
        (False, False),
        (False, False),
        (False, False),
        (True, True),
        (True, True),
        (True, True),
    ]


def test_greater_equal():
    from clintest.quantifier import GreaterEqual
    quantifier = GreaterEqual(2)

    assert quantifier.outcome().as_tuple() == (False, False)

    input = 4 * [False, True]
    output = [quantifier.consume(value).as_tuple() for value in input]

    assert output == [
        (False, False),
        (False, False),
        (False, False),
        (True, True),
        (True, True),
        (True, True),
        (True, True),
        (True, True),
    ]
