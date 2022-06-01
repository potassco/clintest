if __name__ == "__main__":
    import colorama
    colorama.init()

    # TODO

    from .solver import Clingo
    from .assessment import Any, Sat

    assessment = Any([Sat(), Any([Sat()])])

    solver = Clingo(arguments=["0"], program="a.")
    solver.solve(assessment)

    print(assessment)
