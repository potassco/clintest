from abc import ABC, abstractmethod


class UnknownResult(Exception):
    pass

class ResultType(enumerate):
    PASS = "PASS"
    FAIL = "FAIL"
    IGNORED = "IGNORED"
    UNKNOWN = "UNKNOWN"

class EvaluatorResult:
    def __init__(self, result, evaluator, missing=[], overload=[], additional=None):

        self.evalutor = evaluator

        if result == True:
            self.result = ResultType.PASS
        elif result == False:
            self.result = ResultType.FAIL
        else:
            self.result = result

        if result == ResultType.UNKNOWN :
            raise UnknownResult


        self.missing = missing
        self.overload = overload

        self.additional = additional

        self.solver = None


    def add_solver(self, solver):
        self.solver = solver

    def __str__(self):
        ret = f"Testing {self.evalutor.name}\n"
        if self.solver:
            ret += f"solver : {str(self.solver)}"
        ret += f"Function \t: {self.evalutor.function}\n"
        ret += f"Arguments \t: {self.evalutor.argument}\n"
        ret += f"Result  \t: {self.result}\n"
        if len(self.missing.keys()) > 0 or len(self.overload.keys()) > 0 :
            mem = 'Missing (-) and overload (+) symbols\n'
            found = False
            keys = (*self.missing.keys(),*self.overload.keys())
            print(self.missing)
            for k in keys:
                if k in self.missing or k in self.overload:
                    mem += f"Model {k}:\n"
                if k in self.missing:
                    found = True
                    for m in self.missing[k]:
                        mem += f"\t - {m}\n"
                if  k in self.overload:
                    found = True
                    for o in self.overload[k]:
                        mem += f"\t + {o}\n"

            if found:
                ret += mem

        if self.additional:
            ret += self.additional

        return ret






class Evaluator(ABC):
    def __init__(self, name, function, argument):
        self.name = name
        self.function = function
        self.argument = argument

        # result
        self.result = ResultType.UNKNOWN

        # evaluatorresult variables
        self.additional_info = None
        self.missing = {}
        self.overload = {}


    def on_model(self,result):
        pass

    def on_finish(self,result):
        pass

    def conclude(self) -> EvaluatorResult:
        return EvaluatorResult(
            self.result,
            self,
            self.missing,
            self.overload,
            self.additional_info
        )


    def done(self):
        if self.result == ResultType.UNKNOWN : return False
        else : return True


    @classmethod
    def from_json(cls, json):
        return cls(
            name=json["name"],
            function=json['function'],
            argument=json['argument']
        )




class SAT(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)

    def on_finish(self, result):
        if not(self.argument ^ result.satisfiable):
            self.result = ResultType.PASS
        else :
            self.result = ResultType.FAIL 

class TrueInAll(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)
        self.local_result = True
        
    def on_model(self, result):
        ret = True
        missing = []

        for a in self.argument:
            a_found = False
            for m in result.symbols():
                a_found = a_found or (a == m.__str__())

            if not a_found:
                missing.append(a)

            ret = ret and a_found
        if missing:
            self.missing[result.number] = missing

        self.local_result = self.local_result and ret
        if not self.local_result:
            self.result = ResultType.FAIL

    def conclude(self) -> EvaluatorResult:
        if self.local_result == True :
            self.result = ResultType.PASS
        else :
            self.result = ResultType.FAIL
        return super().conclude()




class TrueInOne(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)

    def on_model(self, result):
        nb_found = 0
        for a in self.argument:
            for m in result.symbols():
                if (a == m.__str__()):
                    nb_found += 1

        if nb_found == len(self.argument):
            self.result = ResultType.PASS

    def conclude(self) -> EvaluatorResult:
        if self.result == ResultType.UNKNOWN:
            self.result = ResultType.FAIL
        return super().conclude()




evaluator_dict = {
    'is_sat': SAT,
    'trueinall': TrueInAll,
    'trueinone': TrueInOne
}
