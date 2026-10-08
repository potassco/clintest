import pytest

from clintest.quantifier import All, Any, Exact, Greater, GreaterEqual, Less, LessEqual


@pytest.mark.parametrize(
    ("quantifier", "values", "outcomes"),
    [
        pytest.param(All(), "TFTF", "T? T? F! F! F!", id="all TFTF"),
        pytest.param(Any(), "FTFT", "F? F? T! T! T!", id="any FTFT"),
        pytest.param(Exact(2), "FTFTFTFT", "F? F? F? F? T? T? F! F! F!", id="exact(2) FTFTFTFT"),
        pytest.param(Less(2), "FTFTFTFT", "T? T? T? T? F! F! F! F! F!", id="less(2) FTFTFTFT"),
        pytest.param(LessEqual(2), "FTFTFTFT", "T? T? T? T? T? T? F! F! F!", id="lessequal(2) FTFTFTFT"),
        pytest.param(Greater(2), "FTFTFTFT", "F? F? F? F? F? F? T! T! T!", id="greater(2) FTFTFTFT"),
        pytest.param(GreaterEqual(2), "FTFTFTFT", "F? F? F? F? T! T! T! T! T!", id="greaterequal(2) FTFTFTFT"),
    ],
)
def test_consume(quantifier, values, outcomes):
    actual = [quantifier.outcome()] + [quantifier.consume(value == "T") for value in values]
    assert " ".join(map(str, actual)) == outcomes
