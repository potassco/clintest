from clintest.outcome import Outcome


def test_false_immutable():
    outcome = Outcome(False, False)
    assert not outcome.current_value()
    assert not outcome.is_mutable()
    assert     outcome.as_tuple() == (False, False)
    assert not outcome.is_immutably_true()
    assert     outcome.is_immutably_false()


def test_false_mutable():
    outcome = Outcome(False, True)
    assert not outcome.current_value()
    assert     outcome.is_mutable()
    assert     outcome.as_tuple() == (False, True)
    assert not outcome.is_immutably_true()
    assert not outcome.is_immutably_false()


def test_true_immutable():
    outcome = Outcome(True, False)
    assert     outcome.current_value()
    assert not outcome.is_mutable()
    assert     outcome.as_tuple() == (True, False)
    assert     outcome.is_immutably_true()
    assert not outcome.is_immutably_false()


def test_true_mutable():
    outcome = Outcome(True, True)
    assert     outcome.current_value()
    assert     outcome.is_mutable()
    assert     outcome.as_tuple() == (True, True)
    assert not outcome.is_immutably_true()
    assert not outcome.is_immutably_false()
