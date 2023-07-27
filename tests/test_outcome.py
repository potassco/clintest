# pylint: disable=import-outside-toplevel
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


def test_false_uncertain():
    from clintest.outcome import Outcome
    outcome = Outcome(False, False)

    assert not outcome.current_value()
    assert not outcome.is_certain()
    assert     outcome.as_tuple() == (False, False)
    assert not outcome.is_certainly_false()
    assert not outcome.is_certainly_true()


def test_false_certain():
    from clintest.outcome import Outcome
    outcome = Outcome(False, True)

    assert not outcome.current_value()
    assert     outcome.is_certain()
    assert     outcome.as_tuple() == (False, True)
    assert     outcome.is_certainly_false()
    assert not outcome.is_certainly_true()


def test_true_uncertain():
    from clintest.outcome import Outcome
    outcome = Outcome(True, False)

    assert     outcome.current_value()
    assert not outcome.is_certain()
    assert     outcome.as_tuple() == (True, False)
    assert not outcome.is_certainly_false()
    assert not outcome.is_certainly_true()


def test_true_certain():
    from clintest.outcome import Outcome
    outcome = Outcome(True, True)

    assert     outcome.current_value()
    assert     outcome.is_certain()
    assert     outcome.as_tuple() == (True, True)
    assert not outcome.is_certainly_false()
    assert     outcome.is_certainly_true()
