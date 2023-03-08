from clintest.outcome import Outcome

def test_certain_true():
    outcome = Outcome(True, True)
    assert     outcome.current_value()
    assert     outcome.is_certain()
    assert     outcome.as_tuple() == (True, True)
    assert     outcome.is_certainly_true()
    assert not outcome.is_certainly_false()

def test_uncertain_true():
    outcome = Outcome(True, False)
    assert     outcome.current_value()
    assert not outcome.is_certain()
    assert     outcome.as_tuple() == (True, False)
    assert not outcome.is_certainly_true()
    assert not outcome.is_certainly_false()

def test_uncertain_false():
    outcome = Outcome(False, False)
    assert not outcome.current_value()
    assert not outcome.is_certain()
    assert     outcome.as_tuple() == (False, False)
    assert not outcome.is_certainly_true()
    assert not outcome.is_certainly_false()


def test_certain_false():
    outcome = Outcome(False, True)
    assert not outcome.current_value()
    assert     outcome.is_certain()
    assert     outcome.as_tuple() == (False, True)
    assert not outcome.is_certainly_true()
    assert     outcome.is_certainly_false()
