if __name__ == "__main__":
    import colorama
    colorama.init()

    # TODO

    from .assessment import Any, All, Sat, Unsat
    from .solver import Clingo

    assessment = All([Any([Sat(), Unsat()])])

    solver = Clingo(arguments=["0"], program=":-.")
    solver.solve(assessment)

    print(assessment)
