import pytest

from clintest.outcome import Outcome


@pytest.mark.parametrize(
    ("value", "certain", "certainly_false", "certainly_true"),
    [
        pytest.param(False, False, False, False, id="F?"),
        pytest.param(False, True, True, False, id="F!"),
        pytest.param(True, False, False, False, id="T?"),
        pytest.param(True, True, False, True, id="T!"),
    ],
)
def test_outcome(value, certain, certainly_false, certainly_true):
    outcome = Outcome(value, certain)

    assert outcome.current_value() == value
    assert outcome.is_certain() == certain
    assert outcome.is_certainly_false() == certainly_false
    assert outcome.is_certainly_true() == certainly_true

    assert outcome.as_tuple() == (value, certain)
