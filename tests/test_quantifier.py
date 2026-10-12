import pytest

from clintest.quantifier import (
    All,
    And,
    Any,
    Exact,
    Finished,
    First,
    Greater,
    GreaterEqual,
    Last,
    Less,
    LessEqual,
    Not,
    Or,
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
        pytest.param(Not(All()), "TF", "F? F? T!", id="not(all) TF"),
        pytest.param(Not(Any()), "FT", "T? T? F!", id="not(any) FT"),
        pytest.param(Not(Last()), "TF", "T? F? T?", id="not(last) TF"),
        pytest.param(And(), "T", "T! T!", id="and() T"),
        pytest.param(And(All(), Any()), "TF", "F? T? F!", id="and(all, any) TF"),
        pytest.param(
            And(GreaterEqual(2), LessEqual(3)),
            "TTTT",
            "F? F? T? T? F!",
            id="and(greaterequal(2), lessequal(3)) TTTT",
        ),
        pytest.param(And(Any(), GreaterEqual(2)), "TT", "F? F? T!", id="and(any, greaterequal(2)) TT"),
        pytest.param(Or(), "T", "F! F!", id="or() T"),
        pytest.param(Or(First(), Last()), "FT", "F? F? T?", id="or(first, last) FT"),
        pytest.param(Or(Exact(0), GreaterEqual(2)), "TTF", "T? F? T! T!", id="or(exact(0), greaterequal(2)) TTF"),
        pytest.param(Or(First(), Exact(0)), "FT", "T? T? F!", id="or(first, exact(0)) FT"),
        pytest.param(
            Not(And(GreaterEqual(1), LessEqual(1))),
            "TT",
            "T? F? T!",
            id="not(and(greaterequal(1), lessequal(1))) TT",
        ),
        pytest.param(Finished(And(All(), Any())), "F", "F! F!", id="finished(and(all, any)) F"),
    ],
)
def test_consume(quantifier, values, outcomes):
    actual = [quantifier.outcome()] + [quantifier.consume(value == "T") for value in values]
    assert " ".join(map(str, actual)) == outcomes


@pytest.mark.parametrize(
    "combine",
    [
        pytest.param(Not, id="not"),
        pytest.param(lambda operand: And(operand, All()), id="and"),
        pytest.param(lambda operand: Or(operand, All()), id="or"),
    ],
)
def test_consume_skips_certain_operands(combine):
    operand = Exact(0)
    quantifier = combine(operand)
    quantifier.consume(True)
    quantifier.consume(True)
    assert repr(operand) == "Exact(0, __state=1)"
