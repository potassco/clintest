import pytest

from clintest.quantifier import (
    All,
    Any,
    Exact,
    Finished,
    First,
    Greater,
    GreaterEqual,
    Last,
    Less,
    LessEqual,
)


@pytest.mark.parametrize(
    ("quantifier", "values", "outcomes"),
    [
        pytest.param(All(), "TFTF", "T? T? F! F! F!", id="all TFTF"),
        pytest.param(Any(), "FTFT", "F? F? T! T! T!", id="any FTFT"),
        pytest.param(First(), "FT", "F? F! F!", id="first FT"),
        pytest.param(First(), "TF", "F? T! T!", id="first TF"),
        pytest.param(Last(), "FT", "F? F? T?", id="last FT"),
        pytest.param(Last(), "TF", "F? T? F?", id="last TF"),
        pytest.param(Exact(0), "FT", "T? T? F!", id="exact(0) FT"),
        pytest.param(Exact(2), "FTFTFTFT", "F? F? F? F? T? T? F! F! F!", id="exact(2) FTFTFTFT"),
        pytest.param(Less(0), "F", "F! F!", id="less(0) F"),
        pytest.param(Less(2), "FTFTFTFT", "T? T? T? T? F! F! F! F! F!", id="less(2) FTFTFTFT"),
        pytest.param(LessEqual(0), "FT", "T? T? F!", id="lessequal(0) FT"),
        pytest.param(LessEqual(2), "FTFTFTFT", "T? T? T? T? T? T? F! F! F!", id="lessequal(2) FTFTFTFT"),
        pytest.param(Greater(-1), "F", "T! T!", id="greater(-1) F"),
        pytest.param(Greater(2), "FTFTFTFT", "F? F? F? F? F? F? T! T! T!", id="greater(2) FTFTFTFT"),
        pytest.param(GreaterEqual(0), "F", "T! T!", id="greaterequal(0) F"),
        pytest.param(GreaterEqual(2), "FTFTFTFT", "F? F? F? F? T! T! T! T! T!", id="greaterequal(2) FTFTFTFT"),
        pytest.param(Finished(All()), "FT", "T! T! T!", id="finished(all) FT"),
        pytest.param(Finished(Any()), "TF", "F! F! F!", id="finished(any) TF"),
    ],
)
def test_consume(quantifier, values, outcomes):
    actual = [quantifier.outcome()] + [quantifier.consume(value == "T") for value in values]
    assert " ".join(map(str, actual)) == outcomes
