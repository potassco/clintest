from clintest.quantifier import All, Any, Exact, Greater, GreaterEqual, Less, LessEqual


def test_all():
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
