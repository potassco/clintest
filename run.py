from clintest import TrueInOne, TrueInAll
import clingo
from clintest import Evaluator, ResultType, EvaluatorWrapper, evaluator_dict


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

evaluator_dict['is_sat'] = SAT

wrp = EvaluatorWrapper(
    [evaluator_dict[e['function']].from_json(e) for e in tests])
    
# Or

wrp = EvaluatorWrapper([
    SAT("color.lp is satisfiable", 'is_sat', True),
    TrueInAll("Testing true in all", "trueinall", ["assign(1,red)"]),
    TrueInOne("Testing true in one", "trueinone", ["assign(5,blue)"])
])


ctl = clingo.Control('0')
ctl.load('./examples/color/color.lp')
ctl.ground([("base", [])])
ctl.solve(on_finish=wrp.on_finish, on_model=wrp.on_model)

for r in wrp.retrieve_result():
    print(r)
