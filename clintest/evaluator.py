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

        self.missing = []
        self.overload = []

        self.additional = additional

    def __bool__(self):
        if self.result == ResultType.FAIL:
            return False
        else:
            return True

    def __str__(self):
        ret =  f"Testing {self.evalutor.name}\n"
        ret += f"Function \t: {self.evalutor.function}\n"
        ret += f"Arguments \t: {self.evalutor.argument}\n"

        ret += f"Result  \t: {self.result}\n"
        if len(self.missing) > 0 and len(self.missing) == len(self.overload):
            mem = 'Missing (-) and overload (+) symbols\n'
            found = False
            for i in range(len(self.missing)):
                if self.missing[i]:
                    found = True
                    mem += f"Model {i+1} :"
                    for m in self.missing[i]:
                        mem += f"\t-\t {m}\n"
                if self.overload[i]:
                    found = True
                    for o in self.overload[i]:
                        mem += f"\t+\t {o}\n"

            if found:
                ret += mem + "\n"

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

    def get_type(json):
        return self.type

    @abstractmethod
    def __call__(self, result):
        pass

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
        self.type = "on_finish"

    def __call__(self, result):
        return EvaluatorResult(not(self.argument ^ result.satisfiable),self)


class TrueInAll(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)
        self.type = "on_model"

    def __call__(self, result):
        print(result)


evaluator_dict = {
    'is_sat' : SAT,
    'trueinall' : TrueInAll
}