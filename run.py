from clintest import TrueInOne, TrueInAll
import clingo
from clintest import Evaluator, ResultType, evaluator_dict, EvaluatorContainer


class SAT(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)

    def on_finish(self, result):
        if not(self.argument ^ result.satisfiable):
            self.result = ResultType.PASS
        else:
            self.result = ResultType.FAIL

# Creating a json

tests = [
    {
        "name": "color.lp is satisfiable",
        "function": "is_sat",
        "argument": True
    }, {
        "name": "Testing true in all",
        "function": "trueinall",
        "argument": ["assign(1,red)"]
    }, {
        "name": "Testing true in one",
        "function": "trueinone",
        "argument": ["assign(5,blue)"]
    }
]

evaluator_dict['is_sat'] = SAT # Considering th

ec = EvaluatorContainer(
    [Evaluator.from_json(e) for e in tests])
    
# Or

ec = EvaluatorContainer([
    SAT("color.lp is satisfiable", 'is_sat', True),
    TrueInAll("Testing true in all", "trueinall", ["assign(1,red)"]),
    TrueInOne("Testing true in one", "trueinone", ["assign(5,blue)"])
])


ctl = clingo.Control('0')
ctl.load('./examples/color/color.lp')
ctl.ground([("base", [])])
ctl.solve(on_finish=ec.on_finish, on_model=ec.on_model)


for result in ec.conclude():
    print(result)
