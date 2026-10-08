import pytest

from clintest.outcome import Outcome


@pytest.mark.parametrize(
    ("value", "certain", "certainly_false", "certainly_true", "str_", "repr_"),
    [
        pytest.param(False, False, False, False, "F?", "Outcome(False, False)", id="F?"),
        pytest.param(False, True, True, False, "F!", "Outcome(False, True)", id="F!"),
        pytest.param(True, False, False, False, "T?", "Outcome(True, False)", id="T?"),
        pytest.param(True, True, False, True, "T!", "Outcome(True, True)", id="T!"),
    ],
)
def test_methods(value, certain, certainly_false, certainly_true, str_, repr_):
    outcome = Outcome(value, certain)

    assert outcome.current_value() == value
    assert outcome.is_certain() == certain
    assert outcome.is_certainly_false() == certainly_false
    assert outcome.is_certainly_true() == certainly_true

    assert outcome == Outcome(value, certain)
    assert hash(outcome) == hash(Outcome(value, certain))

    assert outcome.as_tuple() == (value, certain)
    assert outcome != (value, certain)

    assert str(outcome) == str_
    assert outcome != str_

    assert repr(outcome) == repr_
    assert outcome != repr_


def test_distinct():
    outcomes = [Outcome(value, certain) for value in (False, True) for certain in (False, True)]
    assert len(set(outcomes)) == len(outcomes)
