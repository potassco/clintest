from ast import Return
import json as JSON
from .utils import *
from .solver import *
from .evaluator import *



class Test:
    def __init__(self, name:str, folder:str='./'):
        self.name = name
        self.folder = folder
        self.solvers = []
        self.containers:List[EvaluatorContainer] = []

    def from_json(json:dict,folder:str='./'):
        test = Test(json['name'],folder=folder)
        confs = createConfigurations(json['solver'])
        for c in confs:
            c['folder'] = folder
            s = Solver.from_json(c)
            evs = []
            for e in json['evaluator']:
                evs.append(Evaluator.from_json(e))
            test.containers.append(EvaluatorContainer(evs))
            test.solvers.append(s)
        return test
    
    def run(self):
        for solver,ec in zip(self.solvers,self.containers):
            solver.run(ec)

    def get_result(self,verbosity:int):
        ret = ''
        for solver,ec in zip(self.solvers,self.containers):
            for result in  ec.conclude():
                ret += result.to_str(verbosity)
        return ret