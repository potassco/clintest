if __name__ == "__main__":
    # TODO

    from .solver import Clingo
    from .assessment import Sat

    assessment = Sat()

    solver = Clingo(arguments=["0"], program="a.")
    solver.solve(assessment)

    print(assessment)
