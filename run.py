from clintest import TrueInOne, TrueInAll
import clingo
from clintest import Evaluator, ResultType, EvaluatorContainer


class SAT(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)

    def on_finish(self, result):
        if not(self.argument ^ result.satisfiable):
            self.result = ResultType.SUCCESS
        else:
            self.result = ResultType.FAIL


ec = EvaluatorContainer([
    SAT("color.lp is satisfiable", 'SAT', True),
    TrueInAll("Testing true in all", "trueinall", ["assign(1,red)"]),
    TrueInOne("Testing true in one", "trueinone", ["assign(5,blue)"])
])


ctl = clingo.Control('0')
ctl.load('./examples/color/color.lp')
ctl.ground([("base", [])])
ctl.solve(on_finish=ec.on_finish, on_model=ec.on_model)


for result in ec.conclude():
    print(result)
