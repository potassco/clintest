import pytest

from clintest.assertion import And, Contains, Equals, Equivalent, False_, Implies, Not, Or, SubsetOf, SupersetOf, True_
from clintest.protocol import PersistedModel

MODEL = PersistedModel.from_str("a b")


@pytest.mark.parametrize(
    ("assertion", "model", "holds"),
    [
        pytest.param(Contains("a"), MODEL, True, id="a b contains a = T"),
        pytest.param(Contains("b"), MODEL, True, id="a b contains b = T"),
        pytest.param(Contains("c"), MODEL, False, id="a b contains c = F"),
        pytest.param(Equals({"a", "b"}), MODEL, True, id="a b equals a b = T"),
        pytest.param(Equals({"a"}), MODEL, False, id="a b equals a = F"),
        pytest.param(Equals({"a", "b", "c"}), MODEL, False, id="a b equals a b c = F"),
        pytest.param(SubsetOf({"a", "b"}), MODEL, True, id="a b subsetof a b = T"),
        pytest.param(SubsetOf({"a"}), MODEL, False, id="a b subsetof a = F"),
        pytest.param(SubsetOf({"a", "b", "c"}), MODEL, True, id="a b subsetof a b c = T"),
        pytest.param(SupersetOf({"a", "b"}), MODEL, True, id="a b supersetof a b = T"),
        pytest.param(SupersetOf({"a"}), MODEL, True, id="a b supersetof a = T"),
        pytest.param(SupersetOf({"a", "b", "c"}), MODEL, False, id="a b supersetof a b c = F"),
        pytest.param(True_(), MODEL, True, id="true = T"),
        pytest.param(False_(), MODEL, False, id="false = F"),
        pytest.param(Not(False_()), MODEL, True, id="not F = T"),
        pytest.param(Not(True_()), MODEL, False, id="not T = F"),
        pytest.param(And(), MODEL, True, id="and() = T"),
        pytest.param(And(False_(), False_()), MODEL, False, id="F and F = F"),
        pytest.param(And(False_(), True_()), MODEL, False, id="F and T = F"),
        pytest.param(And(True_(), False_()), MODEL, False, id="T and F = F"),
        pytest.param(And(True_(), True_()), MODEL, True, id="T and T = T"),
        pytest.param(Or(), MODEL, False, id="or() = F"),
        pytest.param(Or(False_(), False_()), MODEL, False, id="F or F = F"),
        pytest.param(Or(False_(), True_()), MODEL, True, id="F or T = T"),
        pytest.param(Or(True_(), False_()), MODEL, True, id="T or F = T"),
        pytest.param(Or(True_(), True_()), MODEL, True, id="T or T = T"),
        pytest.param(Implies(False_(), False_()), MODEL, True, id="F implies F = T"),
        pytest.param(Implies(False_(), True_()), MODEL, True, id="F implies T = T"),
        pytest.param(Implies(True_(), False_()), MODEL, False, id="T implies F = F"),
        pytest.param(Implies(True_(), True_()), MODEL, True, id="T implies T = T"),
        pytest.param(Equivalent(), MODEL, True, id="equivalent() = T"),
        pytest.param(Equivalent(False_()), MODEL, True, id="equivalent(F) = T"),
        pytest.param(Equivalent(True_()), MODEL, True, id="equivalent(T) = T"),
        pytest.param(Equivalent(False_(), False_()), MODEL, True, id="F equivalent F = T"),
        pytest.param(Equivalent(False_(), True_()), MODEL, False, id="F equivalent T = F"),
        pytest.param(Equivalent(True_(), False_()), MODEL, False, id="T equivalent F = F"),
        pytest.param(Equivalent(True_(), True_()), MODEL, True, id="T equivalent T = T"),
    ],
)
def test_holds_for(assertion, model, holds):
    assert assertion.holds_for(model) == holds
