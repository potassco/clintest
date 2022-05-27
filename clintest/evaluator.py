from abc import ABC
from typing import List
from .model import *
import inspect
import sys

class UnknownResult(Exception):
    pass




class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    ORANGE = '\33]93m'
    RESET = '\033[0m'


class ResultType(enumerate):
    SUCCESS = f"{style.GREEN}SUCCESS{style.RESET}"
    FAIL = f"{style.RED}FAIL{style.RESET}"
    IGNORED = f"IGNORED"
    UNKNOWN = f"{style.ORANGE}UNKNOWN{style.RESET}"


class EvaluatorResult:
    def __init__(self, result, evaluator):
        self.evaluator = evaluator
        self.solver = None

        if result == True:
            self.result = ResultType.SUCCESS
        elif result == False:
            self.result = ResultType.FAIL
        else:
            self.result = result

        if result == ResultType.UNKNOWN:
            raise UnknownResult

        self.ret = dict()

    def add_header(self, priority=1):
        self.ret[priority] = [f"--- Testing {self.evaluator.name} : {self.result}\n"]
        return self

    def add_evaluator_info(self,priority=2):
        if not priority in self.ret:
            self.ret[priority] = []
        self.ret[priority].append(f"Function \t: {self.evaluator.function}\n")
        self.ret[priority].append(f"Arguments \t: {self.evaluator.argument}\n")
        return self

    def add_missing_overload(self, missing=None, overload=None, priority=3):
        if (missing is None) and (overload is None):
            return self
        elif not (missing is None) and (overload is None):
            overload = {}
        elif (missing is None) and (not overload is None):
            missing = {}

        keys = sorted((*missing.keys(), *overload.keys()))
        mem = 'Missing (-) and overload (+) symbols\n'
        found = False
        for k in keys:
            if k in missing or k in overload:
                mem += f"Mdl {k}:"
            if k in missing:
                found = True
                for m in missing[k]:
                    mem += f"\t - {m}\n"
            if k in overload:
                found = True
                for o in overload[k]:
                    mem += f"\t + {o}\n"

        if found:
            if priority in self.ret:
                self.ret[priority].append(mem)
            else:
                self.ret[priority] = [mem]

        return self

    def add_info(self, info, priority=4):
        if info:
            if priority in self.ret:
                self.ret[priority].append(info)
            else:
                self.ret[priority] = [info]
            return self

    def add_custom(self, custom, priority):
        if priority in self.ret:
            self.ret[priority].append(custom)
        else:
            self.ret[priority] = [custom]

        return self

    def to_str(self,priority=0):
        ret = ""
        keys = sorted(list(self.ret.keys()))
        for k in keys:
            if k<=priority or priority==0:
                for e in self.ret[k]:
                    ret += e
        return ret


class Evaluator(ABC):
    evaluator_dict = {}

    def __init__(self, name, function, argument) -> None:
        self.name = name
        self.function = function
        self.argument = argument

        # result
        self.result = ResultType.UNKNOWN

    def on_model(self, result) -> None:
        pass

    def on_finish(self, result) -> None:
        pass

    def conclude(self) -> EvaluatorResult:
        ret = EvaluatorResult(self.result, self)
        ret.add_header()
        ret.add_evaluator_info()
        return ret

    def done(self) -> bool:
        if self.result == ResultType.UNKNOWN:
            return False
        else:
            return True

    def from_json(json):
        return Evaluator.evaluator_dict[json['function']](
            name=json["name"],
            function=json['function'],
            argument=json['argument']
        )


class EvaluatorContainer:
    def __init__(self, evaluators: List[Evaluator] = []) -> None:
        self.evaluators = evaluators
        self._did_conclude = False

    def on_model(self, result):
        for e in self.evaluators:
            e.on_model(Model(result))

    def on_finish(self, result):
        for e in self.evaluators:
            e.on_finish(result)

    def conclude(self):
        return [e.conclude() for e in self.evaluators]








class SAT(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)

    def on_finish(self, result):
        if not(self.argument ^ result.satisfiable):
            self.result = ResultType.SUCCESS
        else:
            self.result = ResultType.FAIL


class TrueInAll(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)
        self.local_result = True
        self.missing = {}

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
        if self.local_result == True:
            self.result = ResultType.SUCCESS
        else:
            self.result = ResultType.FAIL
        ret = super().conclude()
        return ret.add_missing_overload(self.missing)


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
            self.result = ResultType.SUCCESS

    def conclude(self) -> EvaluatorResult:
        if self.result == ResultType.UNKNOWN:
            self.result = ResultType.FAIL
        return super().conclude()



for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj):
        if issubclass(obj,Evaluator):
            Evaluator.evaluator_dict[name] = obj
