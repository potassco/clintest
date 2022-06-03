from clintest.assessment import Sat, Unsat
from clintest.solver import Clingo

def test_satisfiable():
    solver = Clingo(arguments=["0"], program="")

    sat = Sat()
    unsat = Unsat()

    solver.solve(sat)
    solver.solve(unsat)

    assert sat.conclusion
    assert not unsat.conclusion

def test_unsatisfiable():
    solver = Clingo(arguments=["0"], program=":-.")

    sat = Sat()
    unsat = Unsat()

    solver.solve(sat)
    solver.solve(unsat)

    assert not sat.conclusion
    assert unsat.conclusion
