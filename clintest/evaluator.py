from abc import ABC, abstractmethod


class EvaluatorResult:
    def __init__(self, result, evaluator, missing=[], overload=[], additional=None):

        self.evalutor = evaluator

        if result == True:
            self.result = ResultType.PASS
        elif result == False:
            self.result = ResultType.FAIL
        else:
            self.result = result

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
        if len(self.missing) > 0 and (len(self.missing) == len(self.overload)):
            mem = 'Missing (-) and overload (+) symbols\n'
            found = False
            for i in range(len(self.missing)):
                if self.missing[i] or self.overload[i]:
                    mem += f"Model {i+1}:\n"
                if self.missing[i]:
                    found = True
                    for m in self.missing[i]:
                        mem += f"\t - {m}\n"
                if self.overload[i]:
                    found = True
                    for o in self.overload[i]:
                        mem += f"\t + {o}\n"

            if found:
                ret += mem

        if self.additional:
            ret += self.additional

        return ret


class ResultType(enumerate):
    PASS = "PASS"
    FAIL = "FAIL"
    IGNORED = "IGNORED"
    UNKNOWN = "UNKNOWN"



class Evaluator(ABC):
    def __init__(self, name, function, argument):
        self.name = name
        self.function = function
        self.argument = argument

        # result
        self.n_call = 0
        self.result = ResultType.UNKNOWN

        # evaluatorresult variables
        self.additional_info = None
        self.missing = []
        self.overload = []

        # on
        self._on_model = None
        self._on_finish = None

    def on_model(self):
        return self._on_model

    def on_finish(self):
        return self._on_finish

    def __call__(self, result):
        self.call(result)
        self.n_call += 1
        return self


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

    @abstractmethod
    def call(self, result):
        pass



class SAT(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)
        self._on_finish = True

    def call(self, result):
        if not(self.argument ^ result.satisfiable):
            self.result = ResultType.PASS
        else :
            self.result = ResultType.FAIL 

class TrueInAll(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)
        self._on_model = True

        self.local_result = True
        
    def call(self, result):
        ret = True
        missing = []
        self.overload.append(None)

        for a in self.argument:
            a_found = False
            for m in result.symbols():
                a_found = a_found or (a == m.__str__())

            if not a_found:
                missing.append(a)
            ret = ret and a_found

        self.missing.append(missing)
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
        self._on_model = True

    def call(self, result):
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
